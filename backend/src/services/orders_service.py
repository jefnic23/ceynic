from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import col, select
from src.database import ASYNC_SESSION_DEPENDENCY
from src.enums.order_status import SOLD_ORDER_STATUSES, OrderStatus
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.account_settings import AccountSettings
from src.models.order import Order, OrderOut
from src.models.order_product import OrderProduct
from src.models.product import Product
from src.schemas.create_order_out import CreateOrderOut
from src.schemas.order_details import OrderDetails
from src.schemas.payment_result import OrderActionResult
from src.schemas.product_for_order import ProductForOrder
from src.services.base.payment_processor_base import PaymentProcessorBase
from src.services.factories.payment_processor_factory import PaymentProcessorFactory


class OrdersService:
    def __init__(
        self,
        session: ASYNC_SESSION_DEPENDENCY,
        payment_processor_factory: Annotated[PaymentProcessorFactory, Depends()],
    ):
        self._session = session
        self._payment_processor_factory = payment_processor_factory

    async def get_all(self, storefront_id: int) -> list[OrderOut]:
        statement = (
            select(Order)
            .where(Order.storefront_id == storefront_id, Order.status != OrderStatus.CREATED.value)
            .order_by(Order.create_time.desc())
        )
        results = await self._session.exec(statement=statement)
        return results.all()

    async def get_order(self, storefront_id: int, order_id: str) -> OrderDetails:
        order = await self._get_order_by_external_id(storefront_id, order_id)
        if order.status == OrderStatus.CREATED.value:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        details = await self._processor_for_order(order).get_order_details(storefront_id, order_id)
        return OrderDetails.model_validate({**details.model_dump(), "record_id": order.id, "status": order.status})

    async def create_order(
        self,
        storefront_id: int,
        product_ids: list[int],
    ) -> CreateOrderOut:
        if not product_ids or len(product_ids) != len(set(product_ids)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product(s) not found")
        products = await self._get_checkout_products(storefront_id, product_ids)
        # This check is provisional: only authorization locks products until the order is recorded.
        await self._ensure_products_unsold(storefront_id, product_ids)
        payment_processor, processor_name = await self._processor_for_storefront(storefront_id)
        result = await payment_processor.create_order(storefront_id, products)
        # Record the provider before approval; CREATED drafts do not reserve products.
        order = Order(
            order_id=result.order_id,
            authorization_id=None,
            capture_id=None,
            status=OrderStatus.CREATED.value,
            create_time=datetime.now(UTC),
            storefront_id=storefront_id,
            payment_processor=processor_name,
        )
        self._session.add(order)
        await self._session.flush()
        for product in products:
            self._session.add(OrderProduct(order_id=order.id, product_id=product.id))
        await self._session.commit()
        return result

    async def authorize_payment(
        self,
        storefront_id: int,
        order_id: str,
        product_ids: list[int],
    ) -> OrderActionResult:
        if not product_ids or len(product_ids) != len(set(product_ids)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid products")

        order = await self._get_order_by_external_id(storefront_id, order_id)
        if order.status != OrderStatus.CREATED.value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already authorized")

        saved_products = await self._session.exec(
            select(OrderProduct.product_id).where(OrderProduct.order_id == order.id)
        )
        if set(saved_products.all()) != set(product_ids):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order products do not match")

        await self._lock_available_products(storefront_id, product_ids)
        products = await self._get_checkout_products(storefront_id, product_ids)
        response = await self._processor_for_order(order).authorize_order(storefront_id, order_id, products)
        order.authorization_id = response.id
        order.status = OrderStatus.PENDING.value
        order.create_time = response.create_time or datetime.now(UTC)
        try:
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            current = await self._get_order_by_external_id(storefront_id, order_id)
            if current.status != OrderStatus.CREATED.value:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already authorized") from error
            raise
        return OrderActionResult(order_id=order_id, status=OrderStatus.PENDING)

    async def reauthorize_payment(self, storefront_id: int, order_id: int) -> OrderActionResult:
        order = await self._require_order(storefront_id, order_id)
        self._require_status(order, OrderStatus.PENDING)
        product_ids = await self._session.exec(select(OrderProduct.product_id).where(OrderProduct.order_id == order.id))
        await self._lock_available_products(storefront_id, product_ids.all(), excluded_order_id=order.id)
        response = await self._processor_for_order(order).reauthorize_payment(storefront_id, order.authorization_id)
        order.authorization_id = response.id
        await self._session.commit()
        return OrderActionResult(order_id=order.order_id, status=OrderStatus.PENDING)

    async def void_payment(self, storefront_id: int, order_id: int) -> OrderActionResult:
        order = await self._require_order(storefront_id, order_id)
        self._require_status(order, OrderStatus.PENDING)
        await self._processor_for_order(order).void_payment(storefront_id, order.authorization_id)
        order.status = OrderStatus.VOIDED.value
        await self._session.commit()
        return OrderActionResult(order_id=order.order_id, status=OrderStatus.VOIDED)

    async def capture_payment(self, storefront_id: int, order_id: int) -> OrderActionResult:
        order = await self._require_order(storefront_id, order_id)
        self._require_status(order, OrderStatus.PENDING)
        response = await self._processor_for_order(order).capture_payment(storefront_id, order.authorization_id)
        order.capture_id = response.id
        order.status = OrderStatus.COMPLETED.value
        await self._session.commit()
        return OrderActionResult(order_id=order.order_id, status=OrderStatus.COMPLETED)

    async def refund_payment(self, storefront_id: int, order_id: int) -> OrderActionResult:
        order = await self._require_order(storefront_id, order_id)
        self._require_status(order, OrderStatus.COMPLETED)
        if order.capture_id is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order has no capture")
        await self._processor_for_order(order).refund_payment(storefront_id, order.capture_id)
        order.status = OrderStatus.REFUNDED.value
        await self._session.commit()
        return OrderActionResult(order_id=order.order_id, status=OrderStatus.REFUNDED)

    # region Private Methods

    async def _get_checkout_products(self, storefront_id: int, product_ids: list[int]) -> list[ProductForOrder]:
        results = await self._session.exec(
            select(Product).where(Product.storefront_id == storefront_id, col(Product.id).in_(product_ids))
        )
        products = results.all()
        if len(products) != len(product_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product(s) not found")
        return [ProductForOrder.model_validate(product) for product in products]

    async def _lock_available_products(
        self, storefront_id: int, product_ids: list[int], excluded_order_id: int | None = None
    ) -> None:
        if not product_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid products")
        # Lock rows in a stable order and hold them until the status change is
        # committed, preventing concurrent authorizations from selling twice.
        for product_id in sorted(product_ids):
            locked = await self._session.exec(
                select(Product.id)
                .where(Product.id == product_id, Product.storefront_id == storefront_id)
                .with_for_update()
            )
            if locked.one_or_none() is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product(s) not found")

        await self._ensure_products_unsold(storefront_id, product_ids, excluded_order_id)

    async def _ensure_products_unsold(
        self, storefront_id: int, product_ids: list[int], excluded_order_id: int | None = None
    ) -> None:
        statement = (
            select(OrderProduct.product_id)
            .join(Order, Order.id == OrderProduct.order_id)
            .where(col(OrderProduct.product_id).in_(product_ids))
            .where(Order.storefront_id == storefront_id, col(Order.status).in_(SOLD_ORDER_STATUSES))
        )
        if excluded_order_id is not None:
            statement = statement.where(Order.id != excluded_order_id)
        sold = await self._session.exec(statement.limit(1))
        if sold.first() is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product is sold")

    async def _get_order_by_external_id(self, storefront_id: int, order_id: str) -> Order:
        result = await self._session.exec(
            select(Order).where(Order.storefront_id == storefront_id, Order.order_id == order_id)
        )
        order = result.one_or_none()
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    async def _require_order(self, storefront_id: int, order_id: int) -> Order:
        result = await self._session.exec(
            select(Order).where(Order.storefront_id == storefront_id, Order.id == order_id).with_for_update()
        )
        order = result.one_or_none()
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    async def _processor_for_storefront(self, storefront_id: int) -> tuple[PaymentProcessorBase, str]:
        result = await self._session.exec(
            select(AccountSettings.payment_processor).where(AccountSettings.storefront_id == storefront_id)
        )
        processor_name = result.one_or_none()
        if processor_name is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No payment processor selected")
        return self._resolve_processor(processor_name), processor_name

    def _processor_for_order(self, order: Order) -> PaymentProcessorBase:
        return self._resolve_processor(order.payment_processor)

    def _resolve_processor(self, processor_name: str) -> PaymentProcessorBase:
        try:
            processor = PaymentProcessorEnum(processor_name)
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment processor unavailable") from error
        return self._payment_processor_factory.get_payment_processor(processor)

    @staticmethod
    def _require_status(order: Order, required: OrderStatus) -> None:
        if order.status != required.value or (required == OrderStatus.PENDING and not order.authorization_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order is not in the required state")

    # endregion
