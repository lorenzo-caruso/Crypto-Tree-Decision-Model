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
from indicators.ta import add_indicators
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
tabella = add_indicators(tabella)
tabella['RSI'] = round(tabella['RSI'], 0)
tabella['MFI'] = round(tabella['MFI'], 0)
tabella['MACD_diff'] = round(tabella['MACD_diff'], 0)
header = tabella.columns

# transformation
# for i in range(7, len(tabella.columns)):
# 	tabella[header[i]] = transformer(tabella[header[i]])

# sma = transformation_SMA(tabella)
# tabella['SMA'] = sma

rapporto = volume(tabella)
tabella['Rapporto'] = rapporto

lunghezza = int(len(tabella.columns))
tabella.insert(lunghezza,'Action','Hold')

tabella = tabella.dropna()
tabella = tabella.reset_index(drop=True)

# min max - algo 
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

def_action = tabella['Action'].copy()

for i in range(len(operation)):
	if def_action[i] == 'Buy':
		def_action[i] = 'No_Hold'
	if def_action[i] == 'Sell':
		def_action[i] = 'No_Hold'

tabella['Action'] = def_action
 
# inizio
datainizio_2 = date(datainizio_1)

# fine
datafine_2 = date(datafine_1)

# class imbalance
class_imb = sns.countplot(x='Action', data=tabella) 
plt.savefig("data/class_imb.png") 

plot = graph_h_nh(tabella.loc[0:200,:])
figure_name = date_data_name_plot(datainizio_2, datafine_2)
plot.savefig(figure_name)

fig = class_imb.get_figure()
fig.savefig("data/class_imb_before.png")

count_class_0, count_class_1 = tabella['Action'].value_counts()
print(count_class_0)
print(count_class_1)
df_class_0 = tabella[tabella['Action'] == 'Hold']
df_class_1 = tabella[tabella['Action'] == 'No_Hold']

df_class_1_over = df_class_1.sample(count_class_0, replace=True)
df_test_over = pd.concat([df_class_1_over, df_class_0], axis=0)

print('Random under-sampling:')
print(df_test_over['Action'].value_counts())

tabella = df_test_over.sample(frac=1).reset_index(drop=True)

plot = graph(tabella)
figure_name = date_data_name_plot(datainizio_2, datafine_2)
plot.savefig(figure_name)

class_imb_after = sns.countplot(x='Action', data=tabella) 
plt.savefig("data/class_imb_after.png") 

xlsx = date_data_name_xlsx(datainizio_2, datafine_2)
tabella.to_excel(xlsx, engine='xlsxwriter')
