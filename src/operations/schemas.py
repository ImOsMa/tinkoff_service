from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class AccountOperation(BaseModel):
    currency: str
    date: datetime
    id: str
    instrument_type: str
    payment: float
    price: float
    quantity: int
    type: str


class AccountPortfolio(BaseModel):
    total_amount_shares: float
    total_amount_currencies: float
    expected_yield: float


class PositionsSecurities(BaseModel):
    figi: str
    blocked_position: int
    balance: int


class AccountPositions(BaseModel):
    money: float
    blocked: float
    securities: List[PositionsSecurities]


class WithdrawLimits(BaseModel):
    money: float
    blocked: float


class LastPrice(BaseModel):
    figi: str
    price: float
    time: datetime


class Trade(BaseModel):
    figi: str
    direction: str
    price: str
    quantity: int
    time: datetime


class Order(BaseModel):
    price: float
    quantity: int


class OrderBook(BaseModel):
    figi: str
    depth: int
    bids: List[Order]
    asks: List[Order]
    last_price: float
    close_price: float
    limit_up: float
    limit_down: float
