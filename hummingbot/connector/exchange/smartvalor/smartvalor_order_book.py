from typing import Dict, Optional

from hummingbot.core.data_type.order_book_message import OrderBookMessageType, OrderBookMessage

from hummingbot.connector.exchange.smartvalor.smartvalor_order_book_message import SmartvalorOrderBookMessage
from hummingbot.core.data_type.order_book import OrderBook


class SmartvalorOrderBook(OrderBook):

    @classmethod
    def snapshot_message_from_exchange(cls,
                                       msg: Dict[str, any],
                                       timestamp: float,
                                       metadata: Optional[Dict] = None) -> OrderBookMessage:
        if metadata:
            msg.update(metadata)

        return SmartvalorOrderBookMessage(message_type=OrderBookMessageType.SNAPSHOT,
                                          content=msg,
                                          timestamp=timestamp)

    @classmethod
    def diff_message_from_exchange(cls, msg: Dict[str, any], timestamp: Optional[float] = None,
                                   metadata: Optional[Dict] = None) -> OrderBookMessage:
        if metadata:
            msg.update(metadata)
        return SmartvalorOrderBookMessage(OrderBookMessageType.DIFF, content=msg, timestamp=timestamp)

    @classmethod
    def trade_message_from_exchange(cls, msg: Dict[str, any], metadata: Optional[Dict] = None):
        if metadata:
            msg.update(metadata)
        msg.update({
            "exchange_order_id": msg.get("tradeId"),
            "trade_type": msg.get("type"),
            "price": msg.get("price"),
            "amount": msg.get("baseVolume"),
        })
        return SmartvalorOrderBookMessage(OrderBookMessageType.TRADE, content=msg, timestamp=msg["timestamp"])
