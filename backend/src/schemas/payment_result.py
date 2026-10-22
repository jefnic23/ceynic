from datetime import datetime

from src.enums.order_status import OrderStatus
from src.schemas.base import BaseSchema


class AuthorizationResult(BaseSchema):
    id: str
    create_time: datetime | None = None


class CaptureResult(BaseSchema):
    id: str


class OrderActionResult(BaseSchema):
    order_id: str
    status: OrderStatus
