from datetime import datetime
from enum import StrEnum

from src.enums.order_status import OrderStatus
from src.schemas.base import BaseSchema


class AuthorizationResult(BaseSchema):
    id: str
    create_time: datetime | None = None


class PaymentState(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PaymentResult(BaseSchema):
    id: str
    state: PaymentState


class OrderActionResult(BaseSchema):
    order_id: str
    status: OrderStatus
