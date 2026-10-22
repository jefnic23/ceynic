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


class ProviderOrderItem(OrderItem):
    sku: str | None = None


class AdminOrderItem(OrderItem):
    image_url: str | None = None


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
    items: list[ProviderOrderItem]
    total: Money | None = None
    customer: OrderCustomer
    shipping_address: ShippingAddress | None = None


@frontend
class OrderConfirmation(BaseSchema):
    id: str
    status: OrderStatus
    items: list[OrderItem]
    total: Money | None = None


@frontend
class OrderDetails(ProviderOrderDetails):
    items: list[AdminOrderItem]
    record_id: int
    status: OrderStatus
