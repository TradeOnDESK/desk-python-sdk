from pathlib import Path
import sys
from time import sleep

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/src')

from desk.exchange import Exchange  # noqa
from desk.info import Info  # noqa
from desk import auth  # noqa
from desk.enum import OrderSide, OrderType, TimeInForce, MarketSymbol  # noqa

from constants import NETWORK, RPC_URL, ACCOUNT, PRIVATE_KEY, SUB_ACCOUNT_ID


def place_order(exchange: Exchange, price: str):
    resp = exchange.place_order(
        symbol=MarketSymbol.BTCUSD,
        amount="0.003",
        price=price,
        side=OrderSide.LONG,
        order_type=OrderType.LIMIT,
        time_in_force=TimeInForce.POST_ONLY,
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
    jwt = auth.Auth(network=NETWORK, private_key=PRIVATE_KEY, rpc_url=RPC_URL, account=ACCOUNT, sub_account_id=SUB_ACCOUNT_ID)
    exchange = Exchange(network=NETWORK, auth=jwt)

    info = Info(network=NETWORK, skip_ws=True)

    mark_prices = info.get_mark_price()

    btc_price = float(mark_prices[0]['mark_price'])
    print("btc_price", btc_price)

    place_price = f"{float(btc_price) * 0.99:.1f}"
    print("place_price", place_price)
    resp = place_order(exchange, place_price)
    print(resp)
    sleep(2)
    cancel_order(exchange, resp['order_digest'])


if __name__ == "__main__":
    main()
