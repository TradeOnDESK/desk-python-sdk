from typing import Literal, TypedDict, Union, List, Tuple, Dict, Optional

TradeSubscription = TypedDict(
    "TradeSubscription", {"type": Literal["tradesV2"], "symbol": str})
OrderbookSubscription = TypedDict("OrderbookSubscription", {
                                  "type": Literal["l2BookV2"], "symbol": str})
MarkPriceSubscription = TypedDict("MarkPriceSubscription", {
                                  "type": Literal["markPricesV2"]})
IndexPriceSubscription = TypedDict("IndexPriceSubscription", {
                                   "type": Literal["indexPricesV2"]})

Subscription = Union[TradeSubscription, OrderbookSubscription,
                     MarkPriceSubscription, IndexPriceSubscription]

StreamMessage = TypedDict("StreamMessage", {
    "type": str
})

OrderbookData = TypedDict("OrderbookData", {
    "bids": List[Tuple[str, str]],
    "asks": List[Tuple[str, str]]
})

OrderbookStreamMessage = TypedDict("OrderbookStreamMessage", {
    "type": str,
    "symbol": str,
    "data": OrderbookData
})

TradeData = TypedDict("TradeData", {
    "price": str,
    "quantity": str,
    "side": str
})

TradeStreamMessage = TypedDict("TradeStreamMessage", {
    "type": str,
    "symbol": str,
    "data": TradeData
})

MarkPriceData = TypedDict("MarkPriceData", {
    "symbol": str,
    "mark_price": str,
    "index_price": str
})

MarkPricesMessage = TypedDict("MarkPricesMessage", {
    "type": str,
    "data": List[MarkPriceData]
})

MarkPricesResponseV2 = TypedDict("MarkPricesResponseV2", {
    "symbol": str,
    "markPrice": str,
    "indexPrice": str
})

ParsedMarkPricesMessage = TypedDict("ParsedMarkPricesMessage", {
    "type": str,
    "data": List[MarkPricesResponseV2]
})

CollateralPriceData = TypedDict("CollateralPriceData", {
    "collateral_id": str,
    "asset": str,
    "price": str
})

CollateralPricesMessage = TypedDict("CollateralPricesMessage", {
    "type": str,
    "data": List[CollateralPriceData]
})

CollateralPricesResponseV2 = TypedDict("CollateralPricesResponseV2", {
    "collateralId": str,
    "asset": str,
    "price": str
})

CollateralPricesV2 = Dict[str, CollateralPricesResponseV2]

ParsedCollateralPricesMessage = TypedDict("ParsedCollateralPricesMessage", {
    "type": str,
    "data": List[CollateralPricesV2]
})

# Define the necessary enum-like literals
OrderSideTypeV2 = Literal["BUY", "SELL"]
OrderType = Literal[
    "Limit",
    "Market",
    "Stop",
    "StopMarket",
    "TakeProfit",
    "TakeProfitMarket"
]
Hex = str  # Assuming Hex is just a string type in Python

TimeInForce = Literal["GTC", "FOK", "IOC", "PostOnly"]

OrderRequestV2 = TypedDict("OrderRequestV2", {
    "symbol": str,
    "broker_id": str,
    "subaccount": Hex,
    "amount": str,
    "price": str,
    "side": OrderSideTypeV2,
    "order_type": OrderType,
    "nonce": str,
    "reduce_only": Optional[bool],
    "trigger_price": Optional[str],
    "is_conditional_order": Optional[bool],
    "time_in_force": Optional[TimeInForce]
}, total=False)  # total=False makes all fields optional

CancelOrderRequestV2 = TypedDict("CancelOrderRequestV2", {
    "symbol": str,
    "subaccount": Hex,
    "order_digest": Hex,
    "nonce": str,
    "is_conditional_order": bool
})

# If not already defined, add OrderSide type
OrderSide = Literal["Long", "Short"]  # Assuming these are the values, adjust if different

CreatePlaceOrderFn = TypedDict("CreatePlaceOrderFn", {
    "amount": str,
    "price": str,
    "side": OrderSide,
    "symbol": str,  # MarketInfo['symbol'] in TS becomes just str in Python
    "orderType": OrderType,
    "reduceOnly": Optional[bool],
    "triggerPrice": Optional[str]
})  # total=False makes reduceOnly and triggerPrice optional

CancelOrderFn = TypedDict("CancelOrderFn", {
    "symbol": str,
    "orderDigest": Hex,
    "isConditionalOrder": bool
})

WsMessage = Union[CollateralPricesMessage, MarkPricesMessage, OrderbookStreamMessage,
                  ParsedCollateralPricesMessage, ParsedMarkPricesMessage, StreamMessage, TradeStreamMessage]
