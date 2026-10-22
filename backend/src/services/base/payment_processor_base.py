from abc import ABC, abstractmethod
from datetime import datetime

from src.schemas.create_order_out import CreateOrderOut
from src.schemas.order_details import ProviderOrderDetails
from src.schemas.payment_result import AuthorizationResult, PaymentResult
from src.schemas.product_for_order import ProductForOrder


class PaymentProcessorBase(ABC):
    @abstractmethod
    async def get_order_details(self, storefront_id: int, order_id: str) -> ProviderOrderDetails:
        pass

    @abstractmethod
    async def create_order(self, storefront_id: int, products: list[ProductForOrder]) -> CreateOrderOut:
        pass

    @abstractmethod
    async def authorize_order(
        self, storefront_id: int, order_id: str, products: list[ProductForOrder]
    ) -> AuthorizationResult:
        pass

    @abstractmethod
    async def reauthorize_payment(self, storefront_id: int, authorization_id: str) -> AuthorizationResult:
        pass

    @abstractmethod
    async def void_payment(self, storefront_id: int, authorization_id: str) -> None:
        pass

    @abstractmethod
    async def capture_payment(
        self, storefront_id: int, authorization_id: str, request_id: str, requested_at: datetime
    ) -> PaymentResult:
        pass

    @abstractmethod
    async def get_capture_result(self, storefront_id: int, capture_id: str) -> PaymentResult:
        pass

    @abstractmethod
    async def refund_payment(
        self, storefront_id: int, capture_id: str, request_id: str, requested_at: datetime
    ) -> PaymentResult:
        pass

    @abstractmethod
    async def get_refund_result(self, storefront_id: int, refund_id: str) -> PaymentResult:
        pass
