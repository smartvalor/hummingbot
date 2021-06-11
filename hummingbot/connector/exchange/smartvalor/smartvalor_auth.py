import hashlib
import hmac
import random
from typing import Dict


class Signature:
    def __init__(self, signature: str, nonce: int):
        self.signature = signature
        self.nonce = nonce


class SmartvalorAuth:
    def __init__(self, api_key: str, secret_key: str, identification: int):
        self._api_key = api_key
        self._secret_key = secret_key
        self._identification = identification

    def get_headers(self) -> Dict[str, str]:
        """
        Generates headers for request
        :return:
        """
        signature = self.get_signature()
        return {
            "accept": 'application/json',
            "Content-Type": 'application/json',
            "api-key": self._api_key,
            "nonce": signature.nonce,
            "signature": signature.signature,
            "identification": self._identification
        }

    def get_signature(self) -> Signature:
        nonce = random.randint(1, 100000000000000)
        message = str(nonce) + str(self._identification) + self._api_key
        signature = hmac.new(self._secret_key.encode('UTF-8'), message.encode('UTF-8'), hashlib.sha256).hexdigest()
        return Signature(signature, nonce)


