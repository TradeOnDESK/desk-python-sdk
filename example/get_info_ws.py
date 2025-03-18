from datetime import datetime
from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root)+'/src')

from constants import NETWORK

from desk.info import Info
from desk.types import MarkPriceSubscription, OrderbookSubscription, TradeSubscription

def get_info_ws():
    info = Info(network=NETWORK, skip_ws=False)

    subscription1: TradeSubscription = {"type": "tradesV2", "symbol": "BTCUSD"}
    info.subscribe(subscription1, lambda x: print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] trade: ", x['data']))

    subscription2: OrderbookSubscription = {"type": "l2BookV2", "symbol": "BTCUSD"}
    info.subscribe(subscription2, lambda x: print("orderbook: ", x['data']))

    subscription3: MarkPriceSubscription = {"type": "markPricesV2"}
    info.subscribe(subscription3, lambda x: print("markprice: ", x['data']))

if __name__ == "__main__":
    get_info_ws()
