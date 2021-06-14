from typing import Dict, Optional, List

from hummingbot.core.data_type.order_book_row import OrderBookRow

from hummingbot.core.data_type.order_book_message import OrderBookMessage, OrderBookMessageType


class SmartvalorOrderBookMessage(OrderBookMessage):
    def __new__(
            cls,
            message_type: OrderBookMessageType,
            content: Dict[str, any],
            timestamp: Optional[float] = None,
            *args,
            **kwargs,
    ):
        if timestamp is None:
            if message_type is OrderBookMessageType.SNAPSHOT:
                raise ValueError("timestamp must not be None when initializing snapshot messages.")
            timestamp = content["timestamp"]

        return super(SmartvalorOrderBookMessage, cls).__new__(
            cls, message_type, content, timestamp=timestamp, *args, **kwargs
        )

    @property
    def update_id(self) -> int:
        return int(self.timestamp)

    @property
    def trade_id(self) -> int:
        return int(self.timestamp)

    @property
    def trading_pair(self) -> str:
        if "trading_pair" in self.content:
            return self.content["trading_pair"]

    @property
    def asks(self) -> List[OrderBookRow]:
        return list(map(lambda row: OrderBookRow(row[0], row[1], self.update_id), self.content["asks"]))

    @property
    def bids(self) -> List[OrderBookRow]:
        return list(map(lambda row: OrderBookRow(row[0], row[1], self.update_id), self.content["bids"]))
