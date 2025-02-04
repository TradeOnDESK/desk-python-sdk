import os
from pathlib import Path
import sys
from time import sleep
from typing import List
from dotenv import load_dotenv


path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/src')

from desk.exchange import Exchange  # noqa
from desk import auth  # noqa
from desk.types import CreatePlaceOrderFn # noqa
from desk.enum import OrderSide, OrderType, TimeInForce, MarketSymbol # noqa
from desk.info import Info # noqa

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
ACCOUNT = os.getenv("ACCOUNT")
CHAIN_ID = os.getenv("CHAIN_ID")
WS_URL = os.getenv("WS_URL")


def batch_place_order(exchange: Exchange):
    orders_list: List[CreatePlaceOrderFn] = [
        {
            "symbol": "BTCUSD",
            "amount": "0.001",
            "price": "100000",
            "side": OrderSide.LONG,
            "orderType": OrderType.LIMIT,
            "timeInForce": TimeInForce.GTC,
            "waitForReply": True
        },
        {
            "symbol": "BTCUSD",
            "amount": "0.001",
            "price": "100500",
            "side": OrderSide.LONG,
            "orderType": OrderType.LIMIT,
            "timeInForce": TimeInForce.GTC,
            "waitForReply": True
        },
        {
            "symbol": "ETHUSD",
            "amount": "0.1",
            "price": "3500",
            "side": OrderSide.LONG,
            "orderType": OrderType.LIMIT,
            "timeInForce": TimeInForce.GTC,
            "waitForReply": True
        }
    ] 
    resp = exchange.batch_place_order(orders_list)
    print(resp)
    return resp


def cancel_all_order(exchange: Exchange):
    resp = exchange.cancel_all_orders(
        wait_for_reply=True
    )
    print(resp)

def manual_cancel_all_order(exchange: Exchange, symbol: MarketSymbol):
    info = Info(skip_ws=True)
    orders =  info.get_subaccount_summary(ACCOUNT, 2)["open_orders"]
    to_cancel_orders = list(map(lambda x: {"orderDigest": x["order_digest"], "symbol": x["symbol"]}, filter(lambda x: x["symbol"] == symbol.value, orders)))

    return exchange.batch_cancel_order(to_cancel_orders)

def main():
    jwt = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL,
                    chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=2)
    exchange = Exchange(auth=jwt)
    info = Info(skip_ws=True)
    resp = batch_place_order(exchange)
    order_digests = list(map(lambda x: x["order_digest"], info.get_subaccount_summary(ACCOUNT, 2)["open_orders"]))
    print(order_digests)
    sleep(2)
    resp = manual_cancel_all_order(exchange, MarketSymbol.BTCUSD)
    print(resp)
    order_digests = list(map(lambda x: x["order_digest"], info.get_subaccount_summary(ACCOUNT, 2)["open_orders"]))
    print(order_digests)


if __name__ == "__main__":
    main()
