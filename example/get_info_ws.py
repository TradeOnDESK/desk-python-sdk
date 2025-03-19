from datetime import datetime
from pathlib import Path
import sys
from time import sleep
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root)+'/src')

from constants import NETWORK

from desk.info import Info
from desk.types import MarkPriceSubscription, OrderbookSubscription, TradeSubscription
from desk.enum import Subscription, MarketSymbol

def get_info_ws():
    info = Info(network=NETWORK, skip_ws=False)

    subscription1: TradeSubscription = {"type": Subscription.TRADE, "symbol": MarketSymbol.BTCUSD}
    subscription_id1 = info.subscribe(subscription1, lambda x: print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] trade: ", x['data']))

    subscription2: OrderbookSubscription = {"type": Subscription.ORDERBOOK, "symbol": MarketSymbol.BTCUSD}
    subscription_id2 = info.subscribe(subscription2, lambda x: print("orderbook: ", x['data']))

    subscription3: MarkPriceSubscription = {"type": Subscription.MARK_PRICE}
    subscription_id3 = info.subscribe(subscription3, lambda x: print("markprice: ", x['data']))

    sleep(10)

    info.unsubscribe(subscription1, subscription_id1)
    info.unsubscribe(subscription2, subscription_id2)
    info.unsubscribe(subscription3, subscription_id3)

    sleep(10)

    info.disconnect_websocket()

if __name__ == "__main__":
    get_info_ws()
