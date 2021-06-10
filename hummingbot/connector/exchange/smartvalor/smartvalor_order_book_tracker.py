from typing import Optional, List

from hummingbot.connector.exchange.smartvalor.smartvalor_order_book_data_source import SmartvalorOrderBookDataSource
from hummingbot.core.data_type.order_book_tracker import OrderBookTracker


class SmartvalorOrderBookTracker(OrderBookTracker):
    def __init__(self, trading_pairs: Optional[List[str]] = None):
        super().__init__(SmartvalorOrderBookDataSource(trading_pairs), trading_pairs)
