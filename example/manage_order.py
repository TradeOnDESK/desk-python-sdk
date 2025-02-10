from pathlib import Path
import sys
from time import sleep

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/src')

from desk.exchange import Exchange  # noqa
from desk.info import Info  # noqa
from desk import auth  # noqa
from desk.enum import OrderSide, OrderType, TimeInForce, MarketSymbol  # noqa

from constants import API_URL, RPC_URL, CHAIN_ID, ACCOUNT, PRIVATE_KEY, SUB_ACCOUNT_ID


def place_order(exchange: Exchange, price: str):
    resp = exchange.place_order(
        symbol=MarketSymbol.BTCUSD,
        amount="0.001",
        price=price,
        side=OrderSide.LONG,
        order_type=OrderType.LIMIT,
        time_in_force=TimeInForce.GTC,
        wait_for_reply=True
    )
    return resp


def cancel_order(exchange: Exchange, order_digest: str):
    resp = exchange.cancel_order(
        symbol=MarketSymbol.BTCUSD,
        order_digest=order_digest,
        is_conditional_order=False,
        wait_for_reply=True
    )
    print(resp)


def main():
    jwt = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL,
                    chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=SUB_ACCOUNT_ID, api_url=API_URL)
    exchange = Exchange(auth=jwt, api_url=API_URL)

    info = Info(api_url=API_URL, skip_ws=True)

    mark_prices = info.get_mark_price()

    btc_price = float(mark_prices[0]['mark_price'])
    print("btc_price", btc_price)

    place_price = str(btc_price - 5000)
    print("place_price", place_price)
    resp = place_order(exchange, place_price)
    print(resp)
    sleep(2)
    cancel_order(exchange, resp['order_digest'])


if __name__ == "__main__":
    main()
