#!/usr/bin/env python

import asyncio
import logging
import time

import aiohttp

from typing import List, Dict, Any

import pandas as pd

from hummingbot.logger import HummingbotLogger

from hummingbot.core.data_type.order_book_message import OrderBookMessage

from hummingbot.connector.exchange.smartvalor.smartvalor_order_book import SmartvalorOrderBook
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_row import OrderBookRow
from hummingbot.core.data_type.order_book_tracker_data_source import OrderBookTrackerDataSource
import hummingbot.connector.exchange.smartvalor.smartvalor_contants as constants


class SmartvalorOrderBookDataSource(OrderBookTrackerDataSource):

    def __init__(self, trading_pairs: List[str] = None):
        super().__init__(trading_pairs)
        self._trading_pairs: List[str] = trading_pairs
        self._last_trade_timestamp = time.gmtime()


    @classmethod
    def logger(cls) -> HummingbotLogger:
        global _logger
        if _logger is None:
            _logger = logging.getLogger(__name__)
        return _logger

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

    async def get_snapshot(self, client: aiohttp.ClientSession, trading_pair: str) -> Dict[str, Any]:
        """
        Fetches order book snapshot for a particular trading pair from the exchange REST API.
        :param client:
        :param trading_pair:
        :return:
        """

    async def get_new_order_book(self, trading_pair: str) -> OrderBook:
        async with aiohttp.ClientSession() as client:
            response = await client.get(f"{constants.API_URL}/v1/orderbook/{trading_pair.replace('-', '_')}&depth=100")
            data: Dict[str, Any] = await response.json()
            order_book = OrderBook()
            bids: List[List[float]] = data["bids"]
            asks: List[List[float]] = data["asks"]
            timestamp = data["timestamp"]
            bids_row = list(map(lambda row: OrderBookRow(row[0], row[1], timestamp), bids))
            asks_row = list(map(lambda row: OrderBookRow(row[0], row[1], timestamp), asks))
            order_book.apply_snapshot(bids_row, asks_row, timestamp)
            return order_book

    async def listen_for_order_book_diffs(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        pass  # SmartValor does not use DIFF, it sticks to using SNAPSHOT

    async def listen_for_order_book_snapshots(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        while True:
            try:
                # trading_pairs: List[str] = await self.get_trading_pairs()
                async with aiohttp.ClientSession() as client:
                    for trading_pair in self._trading_pairs:
                        try:
                            response = await client.get(f"{constants.API_URL}/v1/orderbook/{trading_pair.replace('-', '_')}&depth=100")
                            data: Dict[str, Any] = await response.json()
                            snapshot_msg: OrderBookMessage = SmartvalorOrderBook.snapshot_message_from_exchange(data, data["timestamp"])
                            output.put_nowait(snapshot_msg)
                            self.logger().debug(f"Saved order book snapshot for {trading_pair}")
                            await asyncio.sleep(5)
                        except asyncio.CancelledError:
                            raise
                        except Exception:
                            self.logger().error("Unexpected error.", exc_info=True)
                            await asyncio.sleep(5)
                    this_hour: pd.Timestamp = pd.Timestamp.utcnow().replace(minute=0, second=0, microsecond=0)
                    next_hour: pd.Timestamp = this_hour + pd.Timedelta(hours=1)
                    delta: float = next_hour.timestamp() - time.time()
                    await asyncio.sleep(delta)
            except asyncio.CancelledError:
                raise
            except Exception:
                self.logger().error("Unexpected error.", exc_info=True)
            await asyncio.sleep(5.0)

    async def listen_for_trades(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        while True:
            try:
                # trading_pairs: List[str] = await self.get_trading_pairs()
                async with aiohttp.ClientSession() as client:
                    for trading_pair in self._trading_pairs:
                        try:
                            response = await client.get(f"{constants.API_URL}/v1/trades/{trading_pair.replace('-', '_')}&depth=100")
                            data: List[Any] = await response.json()
                            valid_trades = list(filter(lambda x: x['timestamp'] > self._last_trade_timestamp, data))
                            for trade in valid_trades:
                                snapshot_msg: OrderBookMessage = SmartvalorOrderBook.trade_message_from_exchange(trade, trade["timestamp"])
                                output.put_nowait(snapshot_msg)
                                self.logger().debug(f"Sent Trade with id {trade['tradeId']}")
                            max_timestamp = max(list(map(lambda x: x['timestamp'], valid_trades)))
                            self._last_trade_timestamp = max_timestamp
                            await asyncio.sleep(5)
                        except asyncio.CancelledError:
                            raise
                        except Exception:
                            self.logger().error("Unexpected error.", exc_info=True)
                            await asyncio.sleep(5)
                    this_hour: pd.Timestamp = pd.Timestamp.utcnow().replace(minute=0, second=0, microsecond=0)
                    next_hour: pd.Timestamp = this_hour + pd.Timedelta(hours=1)
                    delta: float = next_hour.timestamp() - time.time()
                    await asyncio.sleep(delta)
            except asyncio.CancelledError:
                raise
            except Exception:
                self.logger().error("Unexpected error.", exc_info=True)
            await asyncio.sleep(5.0)
