from fastapi import APIRouter, Depends, HTTPException, Header
from orders.schemas import *

from tinkoff.invest import (
    AccessLevel,
    AccountStatus,
    AccountType,
    Client,
    InstrumentIdType,
    TradeDirection,
    OrderType
)

router = APIRouter(
    prefix='/orders',
    tags=["Orders API"]
)


@router.post("/post_order", response_model=PostOrderResponse)
def post_order(post_order: PostOrder, token: str | None = Header(default=None),
               account_id: str | None = Header(default=None)):
    direction = {"Buy": TradeDirection.TRADE_DIRECTION_BUY,
                 "Sell": TradeDirection.TRADE_DIRECTION_SELL,
                 "Unspecified": TradeDirection.TRADE_DIRECTION_UNSPECIFIED}
    order_type = {"Unspecified": OrderType.ORDER_TYPE_UNSPECIFIED,
                  "Limit": OrderType.ORDER_TYPE_LIMIT,
                  "Market": OrderType.ORDER_TYPE_MARKET}

    with Client(token=token, app_name="islam") as client:
        order = client.orders.post_order(figi=post_order.figi, price=None,
                                         direction=direction.get(post_order.direction), account_id=account_id,
                                         order_type=order_type.get(post_order.order_type),
                                         order_id=str(datetime.utcnow().timestamp()))
        return PostOrderResponse()


@router.get("/order_state", response_model=OrderState)
def order_state(order_id: str, token: str | None = Header(default=None),
                account_id: str | None = Header(default=None)):

    with Client(token=token, app_name="islam") as client:
        order_state = client.orders.get_order_state(account_id=account_id, order_id=order_id)
        return OrderState(order_id=order_state.order_id) # add


@router.get("/get", response_model=List[OrderState])
def get_orders(token: str | None = Header(default=None),
               account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        orders = client.orders.get_orders(account_id=account_id).orders

        response = list()
        for ord in orders:
            ord_data = OrderState(order_id=ord.order_id) # add
            response.append(ord_data)
        return response


@router.post("/cancel_order", response_model=datetime)
def cancel_order(order_id: str, token: str | None = Header(default=None),
                 account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        cancel_status = client.orders.cancel_order(account_id=account_id, order_id=order_id) # check
        return cancel_status.time


@router.put("/replace_order", response_model=PostOrderResponse)
def replace_order(replace_order: ReplaceOrder, token: str | None = Header(default=None),
                  account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        direction = {"Buy": TradeDirection.TRADE_DIRECTION_BUY,
                     "Sell": TradeDirection.TRADE_DIRECTION_SELL,
                     "Unspecified": TradeDirection.TRADE_DIRECTION_UNSPECIFIED}
        order_type = {"Unspecified": OrderType.ORDER_TYPE_UNSPECIFIED,
                      "Limit": OrderType.ORDER_TYPE_LIMIT,
                      "Market": OrderType.ORDER_TYPE_MARKET}

        with Client(token=token, app_name="islam") as client:
            order = client.orders.post_order(figi=post_order.figi, price=None,
                                             direction=direction.get(post_order.direction), account_id=account_id,
                                             order_type=order_type.get(post_order.order_type),
                                             order_id=replace_order.order_id) # check
            return PostOrderResponse()


@router.post("/post_stop_order", response_model=str)
def post_stop_order(stop_order: PostStopOrder, token: str | None = Header(default=None),
                    account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        order_stop = client.stop_orders.post_stop_order(figi=stop_order.figi, account_id=account_id).stop_order_id
        return order_stop


@router.get("/get_stop_order", response_model=List[StopOrder])
def get_stop_order(token: str | None = Header(default=None),
                   account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        stop_order = client.stop_orders.get_stop_orders(account_id=account_id).stop_orders

        response = list()
        for stop_ord in stop_order:
            ord_data = StopOrder(stop_order_id=stop_ord.stop_order_id) # add
            response.append(ord_data)
        return response


@router.post("/cancel_stop_order", response_model=datetime)
def cancel_stop_order(stop_order_id: str, token: str | None = Header(default=None),
                      account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        cancel_order = client.stop_orders.cancel_stop_order(account_id=account_id, stop_order_id=stop_order_id)
        return cancel_order.time

