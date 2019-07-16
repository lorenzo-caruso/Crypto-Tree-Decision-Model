import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def transformer(column):
	arr = column.copy()
	array = column.copy()
	arr.sort_values(inplace=True)
	
	first = arr.quantile(0.1)
	print(first)
	second = arr.quantile(0.2)
	print(second)
	third = arr.quantile(0.3)
	print(third)
	fourth = arr.quantile(0.4)
	print(fourth)
	fifth = arr.quantile(0.5)
	print(fifth)
	six = arr.quantile(0.6)
	print(six)
	seven = arr.quantile(0.7)
	print(seven)
	eight = arr.quantile(0.8)
	print(eight)
	nine = arr.quantile(0.9)
	print(nine)

	for i in range(0,len(arr)):
		if array[i] < first:
			array[i] = 1
		elif first <= array[i] < second:
			array[i] = 2
		elif second <= array[i] < third:
			array[i] = 3
		elif third <= array[i] < fourth:
			array[i] = 4
		elif fourth <= array[i] < fifth:
			array[i] = 5
		elif fifth <= array[i] < six:
			array[i] = 6	
		elif six <= array[i] < seven:
			array[i] = 7
		elif seven <= array[i] < eight:
			array[i] = 8
		elif eight <= array[i] < nine:
			array[i] = 9
		elif array[i] >= nine:
			array[i] = 10
	
	column = array
	return column

def transformer_defined_threesolds(column):
	arr = column.copy()
	array = column.copy()
	arr.sort_values(inplace=True)
	
	first = -0.13
	second = 0.07
	third = -0.03
	fourth = 0.01
	fifth = 0.05
	six = 0.08
	seven = 0.12
	eight = 0.16
	nine = 0.22

	for i in range(0,len(arr)):
		if array[i] < first:
			array[i] = 1
		elif first <= array[i] < second:
			array[i] = 2
		elif second <= array[i] < third:
			array[i] = 3
		elif third <= array[i] < fourth:
			array[i] = 4
		elif fourth <= array[i] < fifth:
			array[i] = 5
		elif fifth <= array[i] < six:
			array[i] = 6	
		elif six <= array[i] < seven:
			array[i] = 7
		elif seven <= array[i] < eight:
			array[i] = 8
		elif eight <= array[i] < nine:
			array[i] = 9
		elif array[i] >= nine:
			array[i] = 10
	
	column = array
	return column

def transformation_SMA(column):
	small = column['Close'].rolling(30).mean()
	high = column['Close'].rolling(100).mean()
	
	sma = column['Close'].copy()
	
	for i in range(len(sma)):
		if small[i] > high[i]:
			sma[i] = 1
		else:
			sma[i] = 0
	return sma
	

def bbands(data):
	chiusura = data['Close'].copy()
	bh = data['BBH'].copy()
	bl = data['BBL'].copy()
	bb = data['BB'].copy()
	for i in range(len(data)):
		if chiusura[i] >= bh[i]:
			bb[i] = 2
		elif chiusura[i] <= bl[i]:
			bb[i] = 0		
		elif bh[i] > chiusura[i] > bl[i]:
			bb[i] = 1
	return bb
		
def date(data):
	data = str(data)
	data = data.split(" ")
	data = data[0]
	data = data.replace(".", "-")
	return(data)

def date_data_name_xlsx(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	xlsx = 'data/{}.xlsx'.format(name)
	return xlsx

def date_data_name_xlsx_2(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	xlsx = 'data/{}_albero2.xlsx'.format(name)
	return xlsx

def date_data_name_xlsx_fs(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	xlsx = 'data/{}_fs.xlsx'.format(name)
	return xlsx

def date_data_name_xlsx_fs_2(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	xlsx = 'data/{}_fs2.xlsx'.format(name)
	return xlsx
		
def date_name_xlsx(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	xlsx = 'backtest/{}.xlsx'.format(name)
	return xlsx
	
def date_name_plot(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	figure = "backtest/{}.png".format(name)
	return figure

def date_data_name_plot(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	figure = "data/{}.png".format(name)
	return figure	

def date_data_name_plot_2(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	figure = "data/{}_albero2.png".format(name)
	return figure

def date_data_name_plot_fs(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	figure = "data/{}_fs.png".format(name)
	return figure

def date_data_name_plot_fs_2(start_date, end_date):
	name = '{}_{}'.format(start_date, end_date)
	figure = "data/{}_fs2.png".format(name)
	return figure

def tree_model_name(name):
	model_name_tree = name
	model_name = "models/{}.sav".format(model_name_tree)
	return model_name
	
def graph(df):
	data = df['Close']
	buy = df.loc[df['Action'] == 'Buy'].index.values.tolist()
	sell = df.loc[df['Action'] == 'Sell'].index.values.tolist()
	fig = plt.figure(figsize = (20, 10))
	plt.plot(data , label = 'BTC/USDT', c = 'black')
	plt.plot(data , 'o', label = 'predict buy', markevery = buy, c = 'g')
	plt.plot(data , 'o', label = 'predict sell', markevery = sell, c = 'r')
	plt.legend()
	return fig

def graph_h_nh(df):
	data = df['Close']
	nh = df.loc[df['Action'] == 'No_Hold'].index.values.tolist()

	fig = plt.figure(figsize = (20, 10))
	plt.plot(data , label = 'BTC/USDT', c = 'black')
	plt.plot(data , 'o', label = 'not hold', markevery = nh, c = 'orange')

	plt.legend()
	return fig

def volume(data):
	mean = data['Volume(Asset)'].rolling(20).mean()
	lunghezza = int(len(data.columns))
	data.insert(lunghezza,'Rapporto',np.nan)
	rapporto = data['Rapporto'].copy()
	for i in range(len(data)):
		if mean[i] >= data['Volume(Asset)'][i]:
			rapporto[i] = 0
		elif mean[i] < data['Volume(Asset)'][i]:
			rapporto[i] = 1
	return rapporto

def optimize(n, m, df, operation):
	table = df.iloc[n:m,:]
	vector = df['Action'].copy()
	if operation == 'buy':
		min = table['Close'].idxmin(axis=0, skipna=True)
		table['Action'][min] = 'Buy_def'
		for i in range(n,m):
			vector[i] = table['Action'][i]
		
	if operation == 'sell':
		max = table['Close'].idxmax(axis=0, skipna=True)
		table['Action'][max] = 'Sell_def'
		for i in range(n,m):
			vector[i] = table['Action'][i]
	
	return vector		
		
