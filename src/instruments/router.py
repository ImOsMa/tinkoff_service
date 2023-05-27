from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated
from instruments.schemas import *

from tinkoff.invest import (
    AccessLevel,
    AccountStatus,
    AccountType,
    Client,
    InstrumentIdType,
    InstrumentStatus
)


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

router = APIRouter(
    prefix='/user_instruments',
    tags=["User Instruments API"],

)


@router.get("/trading_schedules", response_model=List[TradeScheduleResponse])
def trading_schedules(exch: str, token: str | None = Header(default=None)):
    from_ = datetime.now() + timedelta(hours=1)
    to = from_ + timedelta(days=7)
    with Client(token, app_name="islam") as client:
        schedules = client.instruments.trading_schedules(exchange=exch, from_=from_, to=to)

        response = list()
        for sch in schedules.exchanges:
            for trading_day in sch.days:
                if not trading_day.is_trading_day:
                    response.append(
                        TradeScheduleResponse(exchange=sch.exchange, is_trading_day=trading_day.is_trading_day))
                    continue
                response.append(TradeScheduleResponse(exchange=sch.exchange, is_trading_day=trading_day.is_trading_day,
                                                      start_time=trading_day.start_time, end_time=trading_day.end_time))
        return response


@router.get("/currencies", response_model=List[AvailableCurrenciesResponse])
def currencies(token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        instrument_status_base = 1
        currencies = client.instruments.currencies(instrument_status=instrument_status_base)

        response = list()
        for instrument in currencies.instruments:
            response.append(AvailableCurrenciesResponse(
                name=instrument.name, figi=instrument.figi, ticker=instrument.ticker,
                sell_available=instrument.sell_available_flag, buy_available=instrument.buy_available_flag))
        return response


@router.get("/currency_by", response_model=AvailableCurrenciesResponse)
def currency_by(id: str, token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        instrument = client.instruments.currency_by(id_type=1, id=id).instrument
        return AvailableCurrenciesResponse(name=instrument.name, figi=instrument.figi, ticker=instrument.ticker,
                                           sell_available=instrument.sell_available_flag,
                                           buy_available=instrument.buy_available_flag)


@router.get("/share_by", response_model=AvailableShare)
def share_by(ticker: str, class_code: str, token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        inst = client.instruments.share_by(id_type=2, id=ticker, class_code=class_code).instrument
        return AvailableShare(name=inst.name, ticker=inst.ticker, figi=inst.figi, uid=inst.uid,
                              class_code=inst.class_code, exchange=inst.exchange, currency=inst.currency,
                              country_name=inst.country_of_risk_name, buy_available=inst.buy_available_flag,
                              sell_available=inst.sell_available_flag, sector=inst.sector)


@router.get("/shares", response_model=List[AvailableShare])
def shares(token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        shares = client.instruments.shares(instrument_status=1)

        response = list()
        for inst in shares.instruments:
            share = AvailableShare(name=inst.name, ticker=inst.ticker, figi=inst.figi, uid=inst.uid,
                                   class_code=inst.class_code, exchange=inst.exchange, currency=inst.currency,
                                   country_name=inst.country_of_risk_name, buy_available=inst.buy_available_flag,
                                   sell_available=inst.sell_available_flag, sector=inst.sector)
            response.append(share)
        return response


@router.get("/instrument_by", response_model=AvailableShare)
def instrument_by(figi: str, token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        inst = client.instruments.get_instrument_by(id_type=1, id=figi).instrument
        return AvailableShare(name=inst.name, ticker=inst.ticker, figi=inst.figi, uid=inst.uid,
                              class_code=inst.class_code, exchange=inst.exchange, currency=inst.currency,
                              country_name=inst.country_of_risk_name, buy_available=inst.buy_available_flag,
                              sell_available=inst.sell_available_flag)


@router.get("/dividends", response_model=List[ShareDividend])
def dividends(figi: str, token: str | None = Header(default=None)):
    from_ = datetime.now() - timedelta(days=365)
    to = datetime.now()
    with Client(token=token, app_name="islam") as client:
        dividends = client.instruments.get_dividends(figi=figi, from_=from_, to=to).dividends

        response = list()
        for div in dividends:
            close_price = float(f'{div.close_price.units}.{div.close_price.nano}')
            dividend_net = float(f'{div.dividend_net.units}.{div.dividend_net.nano}')
            share_div = ShareDividend(figi=figi, close_price=close_price, close_price_currency=div.close_price.currency,
                                      dividend_net=dividend_net, declared_date=div.declared_date)
            response.append(share_div)
        return response


@router.get("/accounts", response_model=List[Account])
def accounts(token: str | None = Header(default=None)):
    access_level = {AccessLevel.ACCOUNT_ACCESS_LEVEL_FULL_ACCESS: "Full Access",
                    AccessLevel.ACCOUNT_ACCESS_LEVEL_UNSPECIFIED: "Unspecified",
                    AccessLevel.ACCOUNT_ACCESS_LEVEL_NO_ACCESS: "No Access",
                    AccessLevel.ACCOUNT_ACCESS_LEVEL_READ_ONLY: "Read Only"}
    with Client(token=token, app_name="islam") as client:
        accounts = client.users.get_accounts().accounts

        response = list()
        for account in accounts:
            acc_data = Account(id=account.id, name=account.name, access_level=access_level.get(account.access_level),
                               opened_date=account.opened_date)
            response.append(acc_data)
        return response


@router.get("/margin_attributes", response_model=MarginAttributes)
def margin_attributes(token: str | None = Header(default=None), account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        attributes = client.users.get_margin_attributes(account_id=account_id)
        liquid_portfolio = float(f'{attributes.liquid_portfolio.units}.{attributes.liquid_portfolio.nano}')
        starting_margin = float(f'{attributes.starting_margin.units}.{attributes.starting_margin.nano}')
        minimal_margin = float(f'{attributes.minimal_margin.units}.{attributes.minimal_margin.nano}')
        corrected_margin = float(f'{attributes.corrected_margin.units}.{attributes.corrected_margin.nano}')
        return MarginAttributes(liquid_portfolio=liquid_portfolio, starting_margin=starting_margin,
                                minimal_margin=minimal_margin, corrected_margin=corrected_margin)


@router.get("/user_tariff", response_model=UserTariff)
def user_tariff(token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        tariff = client.users.get_user_tariff()
        limit_per_minute = list()
        limit_streams = list()
        for unary_limit in tariff.unary_limits:
            limit_per_minute.append(unary_limit.limit_per_minute)

        for stream_limit in tariff.stream_limits:
            limit_streams.append(stream_limit.limit)

        return UserTariff(limit_per_minute=limit_per_minute, limit_streams=limit_streams)


@router.get("/user_info", response_model=UserInfo)
def user_info(token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        info = client.users.get_info()
        return UserInfo(prem_status=info.prem_status, qual_status=info.qual_status, tariff=info.tariff)

