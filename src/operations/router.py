import time
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Header
from operations.schemas import *

from tinkoff.invest import (
    AccessLevel,
    AccountStatus,
    AccountType,
    Client,
    InstrumentIdType,
    TradeDirection,
    GenerateBrokerReportRequest
)

router = APIRouter(
    prefix='/operation_market',
    tags=["Operation Market Data API"]
)


@router.get("/operations", response_model=List[AccountOperation])
def get_operations(token: str | None = Header(default=None),
                   account_id: str | None = Header(default=None)):
    from_ = datetime.now() - timedelta(days=365)
    to = datetime.now()
    with Client(token=token, app_name="islam") as client:
        operations = client.operations.get_operations(account_id=account_id, from_=from_, to=to).operations

        response = list()
        for oper in operations:
            payment_val = float(f'{abs(oper.payment.units)}.{abs(oper.payment.nano)}')
            price_val = float(f'{abs(oper.price.units)}.{abs(oper.price.nano)}')
            oper_data = AccountOperation(currency=oper.currency, date=oper.date, id=oper.id,
                                         instrument_type=oper.instrument_type, payment=payment_val,
                                         price=price_val, quantity=oper.quantity, type=oper.type)
            response.append(oper_data)
        return response


@router.get("/portfolio", response_model=AccountPortfolio)
def get_portfolio(token: str | None = Header(default=None),
                  account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        portfolio = client.operations.get_portfolio(account_id=account_id)
        total_amount_shares = float(
            f'{abs(portfolio.total_amount_shares.units)}.{abs(portfolio.total_amount_shares.nano)}')
        total_amount_currencies = float(
            f'{abs(portfolio.total_amount_currencies.units)}.{abs(portfolio.total_amount_currencies.nano)}')
        expected_yield = float(f'{abs(portfolio.expected_yield.units)}.{abs(portfolio.expected_yield.nano)}')

        return AccountPortfolio(total_amount_shares=total_amount_shares,
                                total_amount_currencies=total_amount_currencies, expected_yield=expected_yield)


@router.get("/positions", response_model=AccountPositions)
def get_positions(token: str | None = Header(default=None),
                  account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        securities = list()
        positions = client.operations.get_positions(account_id=account_id)
        for sec in positions.securities:
            sec_data = PositionsSecurities(figi=sec.figi, blocked_position=sec.blocked, balance=sec.balance)
            securities.append(sec_data)
        money = float(f'{abs(positions.money.units)}.{abs(positions.money.nano)}')
        blocked = float(f'{abs(positions.blocked.units)}.{abs(positions.blocked.nano)}')
        return AccountPositions(money=money, blocked=blocked, securities=securities)


@router.get("/broker_report", response_model=str)
def get_broker_report(token: str | None = Header(default=None),
                      account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        from_ = datetime.now() - timedelta(days=365)
        to = datetime.now()
        request = GenerateBrokerReportRequest(account_id=account_id, from_=from_, to=to)
        report = client.operations.get_broker_report(generate_broker_report_request=request)
        return report.generate_broker_report_response.task_id


@router.get("/withdraw_limits", response_model=WithdrawLimits)
def get_withdraw_limits(token: str | None = Header(default=None),
                        account_id: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        withdraw = client.operations.get_withdraw_limits(account_id=account_id)
        money = float(f'{abs(withdraw.money.units)}.{abs(withdraw.money.nano)}')
        blocked = float(f'{abs(withdraw.blocked.units)}.{abs(withdraw.blocked.nano)}')
        return WithdrawLimits(money=money, blocked=blocked)


@router.get("/candles")
def get_candles():
    pass


@router.get("/last_prices", response_model=List[LastPrice])
def get_last_prices(figi: str, token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        last_prices = client.market_data.get_last_prices(figi=[figi])

        response = list()
        for last in last_prices.last_prices:
            price = float(f'{abs(last.price.units)}.{abs(last.price.nano)}')
            last_price_data = LastPrice(figi=last.figi, price=price, time=last.time)
            response.append(last_price_data)
        return response


@router.get("/close_prices", response_model=List[Trade])
def get_close_prices(figi: str, token: str | None = Header(default=None)):
    direction = {TradeDirection.TRADE_DIRECTION_BUY: "Buy",
                 TradeDirection.TRADE_DIRECTION_SELL: "Sell",
                 TradeDirection.TRADE_DIRECTION_UNSPECIFIED: "Unspecified"}
    with Client(token=token, app_name="islam") as client:
        from_ = datetime.now() - timedelta(minutes=30)
        to = datetime.now()
        trades = client.market_data.get_last_trades(figi=figi, from_=from_, to=to).trades

        response = list()
        for trade in trades:
            price = float(f'{abs(trade.price.units)}.{abs(trade.price.nano)}')
            trade_data = Trade(figi=trade.figi, direction=direction.get(trade.direction), price=price,
                               quantity=trade.quantity, time=trade.time)
            response.append(trade_data)
        return response


@router.get("/order_book", response_model=OrderBook)
def get_order_book(figi: str, depth: int, token: str | None = Header(default=None)):
    with Client(token=token, app_name="islam") as client:
        order_book = client.market_data.get_order_book(figi=figi, depth=depth)
        bids, asks = list(), list()

        for bid in order_book.bids:
            price = float(f'{abs(bid.price.units)}.{abs(bid.price.nano)}')
            bid_data = Order(price=price, quantity=bid.quantity)
            bids.append(bid_data)

        for ask in order_book.asks:
            price = float(f'{abs(ask.price.units)}.{abs(ask.price.nano)}')
            ask_data = Order(price=price, quantity=ask.quantity)
            asks.append(ask_data)

        last_price = float(f'{abs(order_book.last_price.price.units)}.{abs(order_book.last_price.price.nano)}')
        close_price = float(f'{abs(order_book.close_price.price.units)}.{abs(order_book.close_price.price.nano)}')
        limit_up = float(f'{abs(order_book.limit_up.price.units)}.{abs(order_book.limit_up.price.nano)}')
        limit_down = float(f'{abs(order_book.limit_down.price.units)}.{abs(order_book.limit_down.price.nano)}')

        return OrderBook(figi=order_book.figi, depth=order_book.depth, bids=bids, asks=asks, last_price=last_price,
                         close_price=close_price, limit_up=limit_up, limit_down=limit_down)


