from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class TradeScheduleResponse(BaseModel):
    exchange: str
    is_trading_day: bool
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class AvailableCurrenciesResponse(BaseModel):
    name: str
    figi: str
    ticker: str
    sell_available: bool
    buy_available: bool


class AvailableShare(BaseModel):
    name: str
    ticker: str
    figi: str
    uid: str
    class_code: str
    exchange: str
    currency: str
    country_name: str
    buy_available: bool
    sell_available: bool


class ShareDividend(BaseModel):
    figi: str
    close_price: float
    close_price_currency: str
    dividend_net: float
    declared_date: datetime


class Account(BaseModel):
    id: str
    name: str
    access_level: str
    opened_date: datetime


class MarginAttributes(BaseModel):
    liquid_portfolio: float
    starting_margin: float
    minimal_margin: float
    corrected_margin: float


class UserTariff(BaseModel):
    limit_per_minute: list
    limit_streams: list


class UserInfo(BaseModel):
    prem_status: bool
    qual_status: bool
    tariff: str
