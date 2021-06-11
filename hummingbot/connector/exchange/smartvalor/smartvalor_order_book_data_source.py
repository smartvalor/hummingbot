#!/usr/bin/env python

import asyncio
import aiohttp

from typing import List, Dict, Any
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_tracker_data_source import OrderBookTrackerDataSource
import hummingbot.connector.exchange.smartvalor.smartvalor_contants as constants


class SmartvalorOrderBookDataSource(OrderBookTrackerDataSource):

    def __init__(self, trading_pairs: List[str] = None):
        super().__init__(trading_pairs)
        self._trading_pairs: List[str] = trading_pairs

    @staticmethod
    async def fetch_trading_pairs() -> List[str]:
        async with aiohttp.ClientSession() as client:
            async with client.get(f"{constants.API_URL}/instruments", timeout=10) as response:
                if response.status == 200:
                    try:
                        data: List[Dict[str, Any]] = await response.json()
                        return list(map(lambda a: a["product1"]["isoCode"] + "-" + a["product2"]["isoCode"], data))
                    except Exception:
                        pass
                        # do nothing
                return []

    @classmethod
    async def get_last_traded_prices(cls, trading_pairs: List[str]) -> Dict[str, float]:
        result = {}
        async with aiohttp.ClientSession() as client:
            response = await client.get(f"{constants.API_URL}/v1/ticker")
            data: Dict[str, Any] = await response.json()
            for t_pair in trading_pairs:
                last_price = data[t_pair.replace("-", "_")]["last_price"]
                if last_price is not None:
                    result[t_pair] = last_price
        return result

    async def get_new_order_book(self, trading_pair: str) -> OrderBook:
        pass

    async def listen_for_order_book_diffs(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        pass

    async def listen_for_order_book_snapshots(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        pass

    async def listen_for_trades(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        pass
