import json
import numpy as np
import pandas as pd
import time
import ta
import re
import matplotlib.pyplot as plt
import seaborn as sns
from binance.client import Client
from datetime import datetime
from pandas import DataFrame
from indicators.ta_fs import add_indicators_fs
import settings
from utilities import *
from min_max import get_min_max
import warnings
warnings.filterwarnings('ignore')

#settings import
client = settings.client
datainizio_1 = settings.data_inizio
datafine_1 = settings.data_fine

#datainizio
datainizio = datetime.strptime(datainizio_1,'%d.%m.%Y %H:%M:%S,%f')
datainizio = int(datainizio.timestamp()*1000)
#datafine
datafine = datetime.strptime(datafine_1,'%d.%m.%Y %H:%M:%S,%f')
datafine = int(datafine.timestamp()*1000)

candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, datainizio, datafine)
tabella = DataFrame.from_records(candles)
tabella.columns = ['DateTime','Open','High','Low','Close','Volume(Asset)','DataClose','Volume($)','9','10','11','12']
tabella['DateTime'] = pd.to_datetime(tabella['DateTime'], unit='ms')
tabella['DataClose'] = pd.to_datetime(tabella['DataClose'], unit='ms')
tabella['Open'] = tabella['Open'].astype(float)
tabella['High'] = tabella['High'].astype(float)
tabella['Low'] = tabella['Low'].astype(float)
tabella['Close'] = tabella['Close'].astype(float)
tabella['Volume(Asset)'] = tabella['Volume(Asset)'].astype(float)
tabella = tabella[['DateTime','Open','High','Low','Close','Volume(Asset)','Volume($)']]

#indicatori
tabella = add_indicators_fs(tabella)
tabella['RSI'] = round(tabella['RSI'], 0)
tabella['MFI'] = round(tabella['MFI'], 0)
tabella['MACD_diff'] = round(tabella['MACD_diff'], 0)
tabella['CMF'] = round(tabella['CMF'], 2)

header = tabella.columns

# transformation
# for i in range(7, len(tabella.columns)):
# 	tabella[header[i]] = transformer(tabella[header[i]])

sma = transformation_SMA(tabella)
tabella['SMA'] = sma

lunghezza = int(len(tabella.columns))
tabella.insert(lunghezza,'BB', 0)
tabella['BB'] = bbands(tabella)

tabella = tabella.drop('BBH', 1)
tabella = tabella.drop('BBL', 1)

rapporto = volume(tabella)
tabella['Rapporto'] = rapporto

lunghezza = int(len(tabella.columns))
tabella.insert(lunghezza,'Action','Hold')

tabella = tabella.dropna()
tabella = tabella.reset_index(drop=True)

# min max
smoothing = 3
window = 10

minmax = get_min_max(tabella, smoothing, window)
maxima = minmax[0]
minima = minmax[1]
max_index = maxima.index.tolist()
min_index = minima.index.tolist()

operation = tabella['Action'].copy()

for i in range(0,len(max_index)):
	operation[max_index[i]] = 'Sell'

for i in range(0,len(min_index)):
	operation[min_index[i]] = 'Buy'
	
tabella['Action'] = operation
last_operation = 'buy'
last_operation_index = 0

for i in range(len(operation)):
	if tabella['Action'][i] == 'Sell' and last_operation == 'buy':
		last_operation_index_t = last_operation_index
		last_operation_index = i	
		vector = optimize(last_operation_index_t, last_operation_index, tabella, 'buy')	
		tabella['Action'] = vector
		last_operation = 'sell'
		
	if tabella['Action'][i] == 'Buy' and last_operation == 'sell':
		last_operation_index_t = last_operation_index
		last_operation_index = i	
		vector = optimize(last_operation_index_t, last_operation_index, tabella, 'sell')			
		tabella['Action'] = vector
		last_operation = 'buy'

def_action = tabella['Action'].copy()

for i in range(len(operation)):
	if def_action[i] == 'Buy':
		def_action[i] = 'Hold'
	if def_action[i] == 'Sell':
		def_action[i] = 'Hold'
	if def_action[i] == 'Buy_def':
		def_action[i] = 'Buy'
	if def_action[i] == 'Sell_def':
		def_action[i] = 'Sell'

tabella['Action'] = def_action 

# inizio
datainizio_2 = date(datainizio_1)

# fine
datafine_2 = date(datafine_1)

plot = graph(tabella.loc[0:200,:])
figure_name = date_data_name_plot_fs_2(datainizio_2, datafine_2)
plot.savefig(figure_name)
	
xlsx = date_data_name_xlsx_fs_2(datainizio_2, datafine_2)
tabella.to_excel(xlsx, engine='xlsxwriter')
