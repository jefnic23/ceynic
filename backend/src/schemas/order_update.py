from src.database import BaseSchema
from src.enums.order_status import OrderStatus


class OrderUpdate(BaseSchema):
    authorization_id: str | None = None
    capture_id: str | None = None
    status: OrderStatus | None = None
