import base64
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.enums.payment_processor import PaymentProcessorEnum
from src.http_client import HttpClient
from src.models.account_settings import AccountSettings
from src.schemas.create_order_out import CreateOrderOut
from src.schemas.order_details import Money, OrderCustomer, ProviderOrderDetails, ProviderOrderItem, ShippingAddress
from src.schemas.payment_result import AuthorizationResult, PaymentResult, PaymentState
from src.schemas.paypal.auth_response import AuthResponse
from src.schemas.paypal.authorize_payment_response import AuthorizePaymentResponse
from src.schemas.paypal.base import Amount, Breakdown, UnitAmount
from src.schemas.paypal.create_order_payload import CreateOrderPayload
from src.schemas.paypal.create_order_response import CreateOrderResponse
from src.schemas.paypal.item import Item
from src.schemas.paypal.order_details import OrderDetails as PayPalOrderDetails
from src.schemas.paypal.payments import Authorization
from src.schemas.paypal.purchase_unit import PurchaseUnit
from src.schemas.paypal_credentials import PayPalCredentials
from src.schemas.product_for_order import ProductForOrder
from src.services.base.payment_processor_base import PaymentProcessorBase


class PayPalPaymentResponse(BaseModel):
    id: str
    status: str


class PayPalService(PaymentProcessorBase):
    """Own PayPal protocol details behind the checkout contract."""

    BASE_URL_AUTHORIZATIONS = "/v2/payments/authorizations"
    BASE_URL_CAPTURES = "/v2/payments/captures"
    BASE_URL_ORDERS = "/v2/checkout/orders"
    # Limit unknown-outcome retries to a short window; PayPal does not retain IDs indefinitely.
    _REPLAY_WINDOW = timedelta(minutes=15)
    T = TypeVar("T")

    def __init__(self, session: AsyncSession, settings: Settings, http_client: HttpClient):
        self._session: AsyncSession = session
        self._settings: Settings = settings
        self._http_client: HttpClient = http_client

        # todo: cache paypal access tokens in redis using dict[storefront_id, token]
        # token should have expiration time, so use that to determine when to get a new token
        self._access_token: str | None = None

    @property
    def _paypal_url(self) -> str:
        return self._settings.PAYPAL_BASE_URL

    async def _get_order(self, storefront_id: int, order_id: str) -> PayPalOrderDetails:
        return await self._send_request(
            storefront_id=storefront_id,
            method="GET",
            path=f"{self.BASE_URL_ORDERS}/{order_id}",
            response_model=PayPalOrderDetails,
        )

    async def get_order_details(self, storefront_id: int, order_id: str) -> ProviderOrderDetails:
        details = await self._get_order(storefront_id, order_id)
        units = details.purchase_units
        shipping = next((unit.shipping.address for unit in units if unit.shipping), None)
        amounts = [unit.amount for unit in units if unit.amount]
        if len({amount.currency_code for amount in amounts}) > 1:
            raise ValueError("Order has multiple currencies")
        total = (
            Money(
                currency_code=amounts[0].currency_code,
                value=str(sum(Decimal(amount.value) for amount in amounts)),
            )
            if amounts else None
        )
        return ProviderOrderDetails(
            id=details.id,
            create_time=details.create_time,
            items=[
                ProviderOrderItem(
                    name=item.name,
                    sku=item.sku,
                    quantity=int(item.quantity),
                    unit_amount=(
                        Money(currency_code=item.unit_amount.currency_code, value=item.unit_amount.value)
                        if item.unit_amount else None
                    ),
                )
                for unit in units
                for item in (unit.items or [])
            ],
            total=total,
            customer=OrderCustomer(
                name=" ".join(filter(None, (details.payer.name.given_name, details.payer.name.surname))),
                email=details.payer.email_address,
            ),
            shipping_address=(
                ShippingAddress(
                    address_line_1=shipping.address_line_1,
                    address_line_2=shipping.address_line_2,
                    city=shipping.admin_area_2,
                    region=shipping.admin_area_1,
                    postal_code=shipping.postal_code,
                    country_code=shipping.country_code,
                )
                if shipping else None
            ),
        )

    async def create_order(self, storefront_id: int, products: list[ProductForOrder]) -> CreateOrderOut:
        value = str(sum(product.price for product in products))

        data = CreateOrderPayload(
            purchase_units=[
                PurchaseUnit(
                    amount=Amount(value=value, breakdown=Breakdown(item_total=UnitAmount(value=value))),
                    items=[
                        Item(
                            name=product.title,
                            sku=str(product.id),
                            description=product.description,
                            unit_amount=UnitAmount(value=str(product.price)),
                            quantity=str(1),  # todo: add cart product quantity
                            # todo: add image_url
                        )
                        for product in products
                    ],
                )
            ]
        )

        response = await self._send_request(
            storefront_id=storefront_id,
            method="POST",
            path=self.BASE_URL_ORDERS,
            data=data.model_dump(mode="json"),
            response_model=CreateOrderResponse,
        )

        return CreateOrderOut(order_id=response.id)

    async def authorize_order(
        self, storefront_id: int, order_id: str, products: list[ProductForOrder]
    ) -> AuthorizationResult:
        details = await self._get_order(storefront_id, order_id)
        if details.id != order_id or details.status not in ("APPROVED", "COMPLETED"):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order is not approved")

        items = [item for unit in details.purchase_units for item in (unit.items or [])]
        if (
            len(items) != len(products)
            or {item.sku for item in items} != {str(product.id) for product in products}
            or any(item.quantity != "1" for item in items)
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order products do not match")

        if details.status == "COMPLETED":
            # Recover a remote authorization when the previous local commit failed.
            payments = details.purchase_units[0].payments
            if payments is None or not payments.authorizations:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order has no authorization")
            response = AuthorizePaymentResponse.model_validate(details)
        else:
            response = await self._send_request(
                storefront_id=storefront_id,
                method="POST",
                path=f"{self.BASE_URL_ORDERS}/{order_id}/authorize",
                response_model=AuthorizePaymentResponse,
            )
        if response.id != order_id or response.status != "COMPLETED":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order was not authorized")
        return AuthorizationResult(id=response.authorization_id, create_time=response.create_time)

    async def reauthorize_payment(self, storefront_id: int, authorization_id: str) -> AuthorizationResult:
        response = await self._send_request(
            storefront_id=storefront_id,
            method="POST",
            path=f"{self.BASE_URL_AUTHORIZATIONS}/{authorization_id}/reauthorize",
            headers={"Prefer": "return=representation"},
            response_model=Authorization,
        )

        if response.status != "CREATED":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment was not reauthorized")
        return AuthorizationResult(id=response.id, create_time=response.create_time)

    async def void_payment(self, storefront_id: int, authorization_id: str) -> None:
        details = await self._send_request(
            storefront_id=storefront_id,
            method="GET",
            path=f"{self.BASE_URL_AUTHORIZATIONS}/{authorization_id}",
            response_model=PayPalPaymentResponse,
        )
        if details.status == "VOIDED":
            return
        if details.status != "CREATED":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment cannot be voided")
        await self._send_request(
            storefront_id=storefront_id,
            method="POST",
            path=f"{self.BASE_URL_AUTHORIZATIONS}/{authorization_id}/void",
        )

    async def capture_payment(
        self, storefront_id: int, authorization_id: str, request_id: str, requested_at: datetime
    ) -> PaymentResult:
        self._require_replayable(requested_at)
        response = await self._send_request(
            storefront_id=storefront_id,
            method="POST",
            path=f"{self.BASE_URL_AUTHORIZATIONS}/{authorization_id}/capture",
            headers={"Prefer": "return=representation", "PayPal-Request-Id": request_id},
            response_model=PayPalPaymentResponse,
        )
        return self._payment_result(response)

    async def get_capture_result(self, storefront_id: int, capture_id: str) -> PaymentResult:
        response = await self._send_request(
            storefront_id=storefront_id,
            method="GET",
            path=f"{self.BASE_URL_CAPTURES}/{capture_id}",
            response_model=PayPalPaymentResponse,
        )
        return self._payment_result(response)

    async def refund_payment(
        self, storefront_id: int, capture_id: str, request_id: str, requested_at: datetime
    ) -> PaymentResult:
        self._require_replayable(requested_at)
        response = await self._send_request(
            storefront_id=storefront_id,
            method="POST",
            path=f"{self.BASE_URL_CAPTURES}/{capture_id}/refund",
            headers={"Prefer": "return=representation", "PayPal-Request-Id": request_id},
            response_model=PayPalPaymentResponse,
        )
        return self._payment_result(response)

    async def get_refund_result(self, storefront_id: int, refund_id: str) -> PaymentResult:
        response = await self._send_request(
            storefront_id=storefront_id,
            method="GET",
            path=f"/v2/payments/refunds/{refund_id}",
            response_model=PayPalPaymentResponse,
        )
        return self._payment_result(response)

    # region Private Methods

    @classmethod
    def _require_replayable(cls, requested_at: datetime) -> None:
        if datetime.now(UTC) - requested_at > cls._REPLAY_WINDOW:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Payment outcome needs manual review before retrying",
            )

    @staticmethod
    def _payment_result(response: PayPalPaymentResponse) -> PaymentResult:
        states = {
            "PENDING": PaymentState.PENDING,
            "COMPLETED": PaymentState.COMPLETED,
            "DECLINED": PaymentState.FAILED,
            "FAILED": PaymentState.FAILED,
            "CANCELLED": PaymentState.FAILED,
        }
        state = states.get(response.status)
        if state is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Unknown payment state")
        return PaymentResult(id=response.id, state=state)

    async def _get_credentials(self, storefront_id: int) -> PayPalCredentials:
        """
        Retrieve PayPal client credentials for a given storefront.

        Args:
            storefront_id (int): ID of the storefront.

        Returns:
            PayPalCredentials: Client ID and secret used for token generation.
        """

        statement = select(AccountSettings.payment_processor_settings).where(
            AccountSettings.storefront_id == storefront_id
        ).order_by(AccountSettings.id).limit(1)
        results = await self._session.exec(statement=statement)
        processor_settings = results.one_or_none()
        if processor_settings is None:
            raise ValueError(f"Account settings not found for storefront {storefront_id}")

        credentials = processor_settings.processors.get(PaymentProcessorEnum.PAYPAL.value)
        if credentials is None:
            raise ValueError(f"PayPal credentials not configured for storefront {storefront_id}")
        return PayPalCredentials.model_validate(credentials)

    async def _get_access_token(self, storefront_id: int) -> AuthResponse:
        """
        Obtain an OAuth2 access token from PayPal.

        Args:
            storefront_id (int): Storefront ID for credential scoping.

        Returns:
            AuthResponse: Contains access token and expiration info.
        """

        # todo: error handling
        paypal_credentials = await self._get_credentials(storefront_id)

        auth = base64.b64encode(f"{paypal_credentials.client_id}:{paypal_credentials.client_secret}".encode()).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth}",
        }

        data = {"grant_type": "client_credentials"}

        response = await self._http_client.post_async(
            url=f"{self._paypal_url}/v1/oauth2/token",
            data=data,
            headers=headers,
        )

        return AuthResponse(**response)

    async def _send_request(
        self,
        storefront_id: int,
        method: str,
        path: str,
        headers: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """
        Send an authenticated request to the PayPal API.

        Args:
            storefront_id (int): Storefront ID to retrieve credentials.
            method (str): HTTP method to use ("GET", "POST").
            path (str): API endpoint path.
            headers (dict, optional): Additional headers to include.
            data (dict, optional): JSON-serializable body data.
            params (dict, optional): URL query parameters.
            response_model (Type[T], optional): Pydantic model to deserialize response into.

        Returns:
            Union[T, dict]: Deserialized response or raw data.
        """

        # todo: implement redis to cache dict of storefront access_tokens
        if not self._access_token:
            auth_response = await self._get_access_token(storefront_id)
            self._access_token = auth_response.access_token

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._access_token}",
            **(headers if isinstance(headers, dict) else {}),
        }

        url = f"{self._paypal_url}{path}"

        if method.upper() == "GET":
            response_data = await self._http_client.get_async(
                url=url, headers=request_headers, params=json.dumps(params)
            )
        elif method.upper() == "POST":
            response_data = await self._http_client.post_async(
                url=url,
                headers=request_headers,
                data=json.dumps(data) if data else "{}",
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response_model:
            return response_model.model_validate(response_data)
        return response_data

    # endregion
