import requests
import json
from config import keys

class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def convert(quote, base, amount: str):

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту{base}')
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать колличество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[base_ticker] * float(amount)

        return total_base