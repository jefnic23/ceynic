from typing import Annotated

from fastapi import APIRouter, Depends
from src.dependencies import CURRENT_USER_DEPENDENCY, STOREFRONT_ID_DEPENDENCY
from src.models.order import OrderOut
from src.schemas.create_order_out import CreateOrderOut
from src.schemas.create_order_request import CreateOrderRequest
from src.schemas.order_details import OrderDetails
from src.schemas.payment_result import OrderActionResult
from src.services.orders_service import OrdersService

router = APIRouter()


@router.get("/orders")
async def get_orders(
    current_user: CURRENT_USER_DEPENDENCY, orders_service: Annotated[OrdersService, Depends()]
) -> list[OrderOut]:
    return await orders_service.get_all(current_user.storefront_id)


@router.get("/orders/{order_id:str}")
async def get_order(
    order_id: str, storefront_id: STOREFRONT_ID_DEPENDENCY, orders_service: Annotated[OrdersService, Depends()]
) -> OrderDetails:
    return await orders_service.get_order(storefront_id, order_id)


@router.post("/orders")
async def create_order(
    create_order_request: CreateOrderRequest,
    storefront_id: STOREFRONT_ID_DEPENDENCY,
    orders_service: Annotated[OrdersService, Depends()],
) -> CreateOrderOut:
    return await orders_service.create_order(storefront_id=storefront_id, product_ids=create_order_request.product_ids)


@router.post("/orders/{order_id:str}/authorize")
async def authorize_payment(
    order_id: str,
    create_order_request: CreateOrderRequest,
    orders_service: Annotated[OrdersService, Depends()],
    storefront_id: STOREFRONT_ID_DEPENDENCY,
) -> OrderActionResult:
    return await orders_service.authorize_payment(
        storefront_id=storefront_id,
        order_id=order_id,
        product_ids=create_order_request.product_ids,
    )


@router.post("/orders/{id:int}/void")
async def void_authorized_payment(
    id: int, orders_service: Annotated[OrdersService, Depends()], current_user: CURRENT_USER_DEPENDENCY
) -> OrderActionResult:
    return await orders_service.void_payment(
        storefront_id=current_user.storefront_id,
        order_id=id,
    )


@router.post("/orders/{id:int}/capture")
async def capture_payment(
    id: int, orders_service: Annotated[OrdersService, Depends()], current_user: CURRENT_USER_DEPENDENCY
) -> OrderActionResult:
    return await orders_service.capture_payment(storefront_id=current_user.storefront_id, order_id=id)


@router.post("/orders/{id:int}/refund")
async def refund_payment(
    id: int, orders_service: Annotated[OrdersService, Depends()], current_user: CURRENT_USER_DEPENDENCY
) -> OrderActionResult:
    return await orders_service.refund_payment(storefront_id=current_user.storefront_id, order_id=id)
