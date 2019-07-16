from binance.client import Client
import settings
import pandas as pd
from pandas import DataFrame
import json

client = settings.client

fees = client.get_trade_fee(symbol=settings.symbol)
info = client.get_symbol_info(settings.symbol)

fee = fees['tradeFee'][0]
fee = fee['maker']

minQty_asset = info['filters'][2]
minQty_asset = minQty_asset['minQty']

minQty_quote = info['filters'][3]
minQty_quote = minQty_quote['minNotional']


