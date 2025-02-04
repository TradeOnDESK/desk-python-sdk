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

def get_info():
    info = Info(skip_ws=True)
    data = info.get_subaccount_summary(ACCOUNT, 2)["open_orders"]

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
