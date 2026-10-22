from datetime import datetime

from src.decorators import frontend
from src.enums.order_status import OrderStatus
from src.schemas.base import BaseSchema


class Money(BaseSchema):
    currency_code: str
    value: str


class OrderItem(BaseSchema):
    name: str
    quantity: int
    unit_amount: Money | None = None


class OrderCustomer(BaseSchema):
    name: str
    email: str


class ShippingAddress(BaseSchema):
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    region: str | None = None
    postal_code: str | None = None
    country_code: str | None = None


class ProviderOrderDetails(BaseSchema):
    id: str
    create_time: datetime
    items: list[OrderItem]
    total: Money | None = None
    customer: OrderCustomer
    shipping_address: ShippingAddress | None = None


@frontend
class OrderDetails(ProviderOrderDetails):
    record_id: int
    status: OrderStatus
