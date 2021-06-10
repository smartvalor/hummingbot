import asyncio
from collections import defaultdict, deque
from typing import Optional, List, Dict, Deque

from hummingbot.connector.exchange.smartvalor.smartvalor_auth import SmartvalorAuth
from hummingbot.connector.exchange.smartvalor.smartvalor_order_book_data_source import SmartvalorOrderBookDataSource
from hummingbot.core.data_type.order_book_message import OrderBookMessage
from hummingbot.core.data_type.order_book_tracker import OrderBookTracker
import hummingbot.connector.exchange.smartvalor.smartvalor_contants as constants

class SmartvalorOrderBookTracker(OrderBookTracker):
    def __init__(self, auth: SmartvalorAuth, trading_pairs: Optional[List[str]] = None):
        super().__init__(SmartvalorOrderBookDataSource(auth, trading_pairs), trading_pairs)
        self._order_book_diff_stream: asyncio.Queue = asyncio.Queue()
        self._order_book_snapshot_stream: asyncio.Queue = asyncio.Queue()
        self._ev_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
        self._saved_message_queues: Dict[str, Deque[OrderBookMessage]] = defaultdict(lambda: deque(maxlen=1000))
        self._auth = auth

    @property
    def exchange_name(self) -> str:
        return constants.EXCHANGE_NAME

    async def tracking_single_order_book(self, trading_pair: str):
        test = 0
