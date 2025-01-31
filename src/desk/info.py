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
    """Info class for DESK. 

    Args:
        skip_ws (bool): skip opening websocket connection
    """

    def __init__(self, ws_url: str = WS_URL, api_url: str = API_URL, broker: str = BROKER, skip_ws: bool = False):
        self.skip_ws = skip_ws
        if not skip_ws:
            self.ws_manager = WebSocketManager(ws_url=ws_url)
            self.ws_manager.start()

        self.api = Api(api_url=api_url)
        self.broker = broker

    def subscribe(self, subscription: Subscription, callback: Callable[[Any], None]):
        """Subscribe to websocket

        Args:
            subscription (Subscription): topic to subscribe to
            callback (Callable[[Any], None]): callback function when message is received
        """
        if self.skip_ws:
            raise Exception(
                "Cannot subscribe to websocket when skip_ws is True")
        self.ws_manager.subscribe(subscription, callback)

    def get_market_info(self):
        """Get market info for current broker

        Returns:
            [
                {
                    id: int,
                    symbol: str,
                    name: str,
                    imf: str,
                    mmf: str,
                    maker_fee: str,
                    taker_fee: str,
                    price_feed_id: int,
                    tick_size: str,
                    lot_size: str,
                    min_notional_size: str
                }
            ]
        """
        return self.api.get(f"/v2/market-info/brokers/{self.broker}")

    def get_mark_price(self):
        """Get mark price for all active markets

        Returns:
            [
                {
                    symbol: str,
                    mark_price: str,
                    index_price: str
                }
            ]
        """
        return self.api.get("/v2/mark-prices")

    def get_collaterals_info(self):
        """Get collateral info

        Returns:
            [
                {
                    asset: str,
                    collateral_id: str,
                    token_addresses: {
                        chain: str,
                        chain_id: int,
                        address: str
                    },
                    decimals: int,
                    collat_factor_bps: str,
                    borrow_factor_bps: str,
                    price_feed_id: int,
                    discount_rate_bps: str,
                    withdrawal_base_fee: str,
                    priority: int
                }
            ]
        """
        return self.api.get("/v2/collaterals")

    def get_last_trades(self, symbol: str):
        """Get last trades for a market

        Args:
            symbol (str): market symbol to get trades for

        Returns:
            [
                {
                    id: int,
                    symbol: str,
                    price: str,
                    quantity: str,
                    is_buyer_maker: bool,
                    time: int
                }
            ]
        """
        return self.api.get("/v2/trades", params={"symbol": symbol})

    def get_subaccount_summary(self, account: str, sub_account_id: int):
        """Get subaccount summary

        Args:
            account (str): evm account address
            sub_account_id (int): sub account id (max 255 but in web only display up to 5 (0 - 4))

        Returns:
            {
                open_orders: [
                    {
                        order_digest: str,
                        symbol: str,
                        side: str,
                        price: str,
                        original_quantity: str,
                        remaining_quantity: str,
                    }
                ],
                collaterals: [
                    {
                        asset: str,
                        collateral_id: str,
                        amount: str
                    }
                ],
                positions: [
                    {
                        symbol: str,
                        side: str,
                        entry_price: str,
                        amount: str
                    }
                ],
                account_margin: str,
                collateral_value: str,
                unrealized_pnl: str,
                pending_funding_fee: str,
                pending_borrowing_fee: str,
                account_imr: str,
                order_imr: str,
                position_imr: str,
                position_mmr: str
            }
        """
        sub_account = str(utils.get_sub_account(account, sub_account_id))
        return self.api.get(f"/v2/subaccount-summary/{sub_account}")