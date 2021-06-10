import asyncio
from typing import List, Dict

from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_tracker_data_source import OrderBookTrackerDataSource


class SmartvalorOrderBookDataSource(OrderBookTrackerDataSource):

    def __init__(self, trading_pairs: List[str] = None):
        super().__init__(trading_pairs)
        self.trading_pairs = trading_pairs

    @staticmethod
    async def fetch_trading_pairs() -> List[str]:
        pass

    @classmethod
    async def get_last_traded_prices(cls, trading_pairs: List[str]) -> Dict[str, float]:
        pass

    async def get_new_order_book(self, trading_pair: str) -> OrderBook:
        pass

    async def listen_for_order_book_diffs(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        pass

    async def listen_for_order_book_snapshots(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        pass

    async def listen_for_trades(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        pass
