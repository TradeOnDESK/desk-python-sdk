from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root)+'/src')

from desk.info import Info
from constants import API_URL, ACCOUNT, SUB_ACCOUNT_ID

def get_info():
    info = Info(skip_ws=True, api_url=API_URL)
    data = info.get_subaccount_summary(ACCOUNT, SUB_ACCOUNT_ID)["open_orders"]

    for order in data:
        print(f"Symbol: {order['symbol']}")
        print(f"Side: {order['side']}")
        print(f"Order Type: {order['order_type']}")
        print(f"Price: {order['price']}")
        print(f"Amount: {order['original_quantity']}")
        print("-" * 50)

    print(info.get_mark_price())
    print(info.get_last_trades("BTCUSD"))
    print(info.get_collaterals_info())

if __name__ == "__main__":
    get_info()
