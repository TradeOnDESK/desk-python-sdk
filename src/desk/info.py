import os
from typing import Any, Callable
from dotenv import load_dotenv
from desk import utils
from desk.api import Api
from desk.types import Subscription
from desk.ws_manager import WebSocketManager
import requests as r

load_dotenv()

WS_URL = os.getenv("WS_URL")
API_URL = os.getenv("API_URL")
BROKER = os.getenv("BROKER")


class Info:
    def __init__(self, ws_url: str = WS_URL, api_url: str = API_URL, broker: str = BROKER, skip_ws: bool = False):
        self.skip_ws = skip_ws
        if not skip_ws:
            self.ws_manager = WebSocketManager(ws_url=ws_url)
            self.ws_manager.start()

        self.api = Api(api_url=api_url)
        self.broker = broker

    def subscribe(self, subscription: Subscription, callback: Callable[[Any], None]):
        if self.skip_ws:
            raise Exception("Cannot subscribe to websocket when skip_ws is True")
        self.ws_manager.subscribe(subscription, callback)

    def get_market_info(self):
        return self.api.get(f"/v2/market-info/brokers/{self.broker}")
    
    def get_mark_price(self):
        return self.api.get("/v2/mark-prices")
    
    def get_collaterals_info(self):
        return self.api.get("/v2/collaterals")
    
    def get_last_trades(self, symbol: str):
        return self.api.get("/v2/trades", params={"symbol": symbol})
    
    def get_subaccount_summary(self, account: str, sub_account_id: int):
        sub_account = str(utils.get_sub_account(account, sub_account_id))
        return self.api.get(f"/v2/subaccount-summary/{sub_account}")