import requests
import json
from config import dict

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'not possible to convert equal currencies {base}')
        try:
            quote_ticker = dict[quote]
        except KeyError:
            raise ConvertionException(f'cannot handle the currency {quote}')
        try:
            base_ticker = dict[base]
        except KeyError:
            raise ConvertionException(f'cannot handle the currency {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'cannot handle the amount {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[dict[base]]

        return total_base
