import os
from pathlib import Path
import sys
from dotenv import load_dotenv

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root)+'/src')

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
ACCOUNT = os.getenv("ACCOUNT")
CHAIN_ID = os.getenv("CHAIN_ID")
WS_URL = os.getenv("WS_URL")

from desk import auth
from desk.exchange import Exchange

def place_order(exchange: Exchange):
    resp = exchange.place_order({
        "symbol": "BTCUSD",
        "amount": "0.001",
        "price": "100000",
        "side": "Long",
        "orderType": "Limit",
        "timeInForce": "GTC"
    })
    print(resp)
    return resp

def cancel_order(exchange: Exchange, order_digest: str):
    resp = exchange.cancel_order({
        "symbol": "BTCUSD",
        "orderDigest": order_digest,
        "isConditionalOrder": False
    })
    print(resp)


def main():
    jwt = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL, chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=2)
    exchange = Exchange(auth=jwt)
    resp = place_order(exchange)
    cancel_order(exchange, resp['data']['order_digest'])

if __name__ == "__main__":
    main()
