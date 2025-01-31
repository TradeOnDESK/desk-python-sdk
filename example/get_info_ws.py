from datetime import datetime
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

from desk.info import Info
from desk.types import IndexPriceSubscription, MarkPriceSubscription, OrderbookSubscription, TradeSubscription

def get_info_ws():
    info = Info()
    subscription: IndexPriceSubscription = {"type": "indexPricesV2"}
    info.subscribe(subscription, lambda x: print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] indexprice: ", x['data'][0]))

    subscription2: TradeSubscription = {"type": "tradesV2", "symbol": "BTCUSD"}
    info.subscribe(subscription2, lambda x: print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] trade: ", x['data']))

    subscription3: OrderbookSubscription = {"type": "l2BookV2", "symbol": "BTCUSD"}
    info.subscribe(subscription3, lambda x: print("orderbook: ", x['data']))

    subscription4: MarkPriceSubscription = {"type": "markPricesV2"}
    info.subscribe(subscription4, lambda x: print("markprice: ", x['data']))

if __name__ == "__main__":
    get_info_ws()
