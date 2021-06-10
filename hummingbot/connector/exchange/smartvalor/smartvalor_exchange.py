from decimal import Decimal
from typing import List, Dict

from hummingbot.connector.exchange.smartvalor.smartvalor_auth import \
    SmartvalorAuth
from hummingbot.connector.exchange_base import ExchangeBase
from hummingbot.connector.in_flight_order_base import InFlightOrderBase
from hummingbot.core.data_type.cancellation_result import CancellationResult
from hummingbot.core.data_type.limit_order import LimitOrder
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.event.events import OrderType, TradeType, TradeFee


class SmartvalorExchange(ExchangeBase):
    """
    SmartvalorExchange connects with Smartvalor exchange (smartvalor.com) and provides basic functionality for a connector
    """

    @property
    def order_books(self) -> Dict[str, OrderBook]:
        pass

    @property
    def limit_orders(self) -> List[LimitOrder]:
        pass

    async def get_active_exchange_markets(self) -> pd.DataFrame:
        pass

    def c_stop_tracking_order(self, order_id):
        pass

    def buy(self, trading_pair: str, amount: Decimal, order_type=OrderType.MARKET, price: Decimal = s_decimal_NaN,
            **kwargs) -> str:
        pass

    def sell(self, trading_pair: str, amount: Decimal, order_type=OrderType.MARKET, price: Decimal = s_decimal_NaN,
             **kwargs) -> str:
        pass

    def cancel(self, trading_pair: str, client_order_id: str):
        pass

    def get_order_book(self, trading_pair: str) -> OrderBook:
        pass

    def get_fee(self, base_currency: str, quote_currency: str, order_type: OrderType, order_side: TradeType,
                amount: Decimal, price: Decimal = s_decimal_NaN) -> TradeFee:
        pass

    @property
    def status_dict(self) -> Dict[str, bool]:
        pass

    @property
    def ready(self) -> bool:
        pass

    @property
    def in_flight_orders(self) -> Dict[str, InFlightOrderBase]:
        pass

    async def cancel_all(self, timeout_seconds: float) -> List[CancellationResult]:
        pass

    def stop_tracking_order(self, order_id: str):
        pass

    API_URL = "api.smartvalor.com"
    EXCHANGE_NAME = "smartvalor"

    def __init__(self,
                 smartvalor_api_key: str,
                 smartvalor_secret_key: str,
                 smartvalor_identitication: str
                 ):
        super().__init__()
        self.auth = SmartvalorAuth(smartvalor_api_key, smartvalor_secret_key, smartvalor_identitication)
