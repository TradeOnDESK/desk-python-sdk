import os
from typing import Any, Callable
from dotenv import load_dotenv
from desk.types import Subscription
from desk.ws_manager import WebSocketManager

load_dotenv()

WS_URL = os.getenv("WS_URL")


class Info:
    def __init__(self, url: str = WS_URL):
        self.ws_manager = WebSocketManager(ws_url=url)
        self.ws_manager.start()

    def subscribe(self, subscription: Subscription, callback: Callable[[Any], None]):
        self.ws_manager.subscribe(subscription, callback)
