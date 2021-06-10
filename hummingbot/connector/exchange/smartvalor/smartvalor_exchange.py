from hummingbot.connector.exchange.smartvalor.smartvalor_auth import \
    SmartvalorAuth
from hummingbot.connector.exchange_base import ExchangeBase


class SmartvalorExchange(ExchangeBase):
    """
    SmartvalorExchange connects with Smartvalor exchange (smartvalor.com) and provides basic functionality for a connector
    """

    API_URL = "api.smartvalor.com"
    EXCHANGE_NAME = "smartvalor"

    def __init__(self,
                 smartvalor_api_key: str,
                 smartvalor_secret_key: str,
                 smartvalor_identitication: str
                 ):
        super().__init__()
        self.auth = SmartvalorAuth(smartvalor_api_key, smartvalor_secret_key, smartvalor_identitication)
