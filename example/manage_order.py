import os
from pathlib import Path
import sys
from time import sleep
from dotenv import load_dotenv

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/src')

from desk.exchange import Exchange  # noqa
from desk import auth  # noqa
from desk.enum import OrderSide, OrderType, TimeInForce, MarketSymbol  # noqa

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
ACCOUNT = os.getenv("ACCOUNT")
CHAIN_ID = os.getenv("CHAIN_ID")
WS_URL = os.getenv("WS_URL")


def place_order(exchange: Exchange):
    resp = exchange.place_order(
        symbol=MarketSymbol.BTCUSD,
        amount="0.001",
        price="100000",
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
                    chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=2)
    exchange = Exchange(auth=jwt)
    resp = place_order(exchange)
    sleep(2)
    cancel_order(exchange, resp['order_digest'])


if __name__ == "__main__":
    main()
