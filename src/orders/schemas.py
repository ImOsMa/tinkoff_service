from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class PostOrder(BaseModel):
    figi: str
    quantity: int
    price: Optional[float]
    direction: str
    account_id: str
    order_type: str
    order_id: str


class PostOrderResponse(BaseModel):
    order_id: str
    execution_report_status: str
    lots_requested: int
    lots_executed: int
    initial_order_price: float
    executed_order_price: float
    total_order_amount: float
    initial_commission: float
    executed_commission: float
    aci_value: float
    figi: str
    direction: str
    initial_security_price: float
    order_type: str
    message: str
    initial_order_price_pt: float


class OrderState(BaseModel):
    order_id: str
    execution_report_status: str
    lots_requested: int
    lots_executed: int
    initial_order_price: float
    executed_order_price: float
    total_order_amount: float
    initial_commission: float
    executed_commission: float
    figi: str
    direction: str
    initial_security_price: float
    service_commission: float
    currency: str
    order_type: str
    order_date: datetime


class ReplaceOrder(BaseModel):
    order_id: str
    quantity: int
    price: float
    price_type: str


class PostStopOrder(BaseModel):
    figi: str
    quantity: str
    price: Optional[float]
    stop_price: Optional[float]
    direction: str
    account_id: str
    expiration_type: str
    stop_order_type: str
    expire_date: Optional[datetime]


class StopOrder(BaseModel):
    stop_order_id: str
    lots_requested: int
    figi: str
    direction: str
    currency: str
    order_type: str
    create_date: datetime
    expiration_date: datetime
    price: float
    stop_price: float
