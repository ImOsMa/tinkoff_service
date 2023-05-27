from fastapi import APIRouter, Depends, HTTPException, Header

from tinkoff.invest import (
    AccessLevel,
    AccountStatus,
    AccountType,
    Client,
    InstrumentIdType,
)

router = APIRouter(
    prefix='/market',
    tags=["Market API"]
)


@router.get("/get_kline")
def get_kline():
    pass


@router.get("/instrument_info")
def get_instrument_info():
    pass


@router.get("/tickers")
def get_latest_price_snapshot():
    pass


@router.get("/position_info")
def get_position_info():
    pass


@router.get("/coin_info")
def change_order():
    pass
