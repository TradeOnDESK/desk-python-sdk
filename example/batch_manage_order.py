from pathlib import Path
import sys
from time import sleep
from typing import List


path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/src')

from desk.exchange import Exchange  # noqa
from desk import auth  # noqa
from desk.types import CreatePlaceOrderFn # noqa
from desk.enum import OrderSide, OrderType, TimeInForce, MarketSymbol # noqa
from desk.info import Info # noqa

from constants import API_URL, RPC_URL, CHAIN_ID, ACCOUNT, PRIVATE_KEY, SUB_ACCOUNT_ID, CRM_URL


def batch_place_order(exchange: Exchange, price_1: str, price_2: str, price_3: str):
    orders_list: List[CreatePlaceOrderFn] = [
        {
            "symbol": "BTCUSD",
            "amount": "0.001",
            "price": price_1,
            "side": OrderSide.LONG,
            "orderType": OrderType.LIMIT,
            "timeInForce": TimeInForce.GTC,
            "waitForReply": True
        },
        {
            "symbol": "BTCUSD",
            "amount": "0.001",
            "price": price_2,
            "side": OrderSide.LONG,
            "orderType": OrderType.LIMIT,
            "timeInForce": TimeInForce.GTC,
            "waitForReply": True
        },
        {
            "symbol": "ETHUSD",
            "amount": "0.1",
            "price": price_3,
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
    info = Info(api_url=API_URL, crm_url=CRM_URL, skip_ws=True)
    orders =  info.get_subaccount_summary(ACCOUNT, SUB_ACCOUNT_ID)["open_orders"]
    to_cancel_orders = list(map(lambda x: {"orderDigest": x["order_digest"], "symbol": x["symbol"]}, filter(lambda x: x["symbol"] == symbol.value, orders)))

    print(to_cancel_orders)

    return exchange.batch_cancel_order(to_cancel_orders)

def main():
    jwt = auth.Auth(api_url=API_URL, crm_url=CRM_URL, private_key=PRIVATE_KEY, rpc_url=RPC_URL,
                    chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=SUB_ACCOUNT_ID)
    exchange = Exchange(api_url=API_URL, crm_url=CRM_URL, auth=jwt)
    info = Info(api_url=API_URL, crm_url=CRM_URL, skip_ws=True)

    mark_prices = info.get_mark_price()

    btc_price = float(mark_prices[0]['mark_price'])
    print("btc_price", btc_price)

    place_price = str(btc_price - 5000)
    print("place_price", place_price)

    place_price_2 = str(btc_price - 10000)
    print("place_price_2", place_price_2)

    eth_price = float(mark_prices[1]['mark_price'])
    print("eth_price", eth_price)

    place_price_eth = str(eth_price - 500)
    print("place_price_eth", place_price_eth)

    resp = batch_place_order(exchange, place_price, place_price_2, place_price_eth)
    order_digests = list(map(lambda x: x["order_digest"], info.get_subaccount_summary(ACCOUNT, SUB_ACCOUNT_ID)["open_orders"]))
    print(order_digests)
    sleep(2)
    resp = manual_cancel_all_order(exchange, MarketSymbol.BTCUSD)
    print(resp)
    order_digests = list(map(lambda x: x["order_digest"], info.get_subaccount_summary(ACCOUNT, SUB_ACCOUNT_ID)["open_orders"]))
    print(order_digests)


if __name__ == "__main__":
    main()
