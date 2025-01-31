from typing import Literal, TypedDict, Union, List, Tuple, Dict

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


WsMessage = Union[CollateralPricesMessage, MarkPricesMessage, OrderbookStreamMessage,
                  ParsedCollateralPricesMessage, ParsedMarkPricesMessage, StreamMessage, TradeStreamMessage]
