from typing import Dict, Any

from hummingbot.connector.in_flight_order_base import InFlightOrderBase


class SmartvalorInFlightOrders(InFlightOrderBase):
    @property
    def is_done(self) -> bool:
        pass

    @property
    def is_cancelled(self) -> bool:
        pass

    @property
    def is_failure(self) -> bool:
        pass

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> InFlightOrderBase:
        pass

    def __init__(self):
        super().__init__()
