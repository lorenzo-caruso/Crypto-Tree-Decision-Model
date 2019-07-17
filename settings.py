from binance.client import Client

# Binance Client
client = Client('YOUR_API_KEY', 'YOUR_SECRET_KEY')
symbol = 'BTCUSDT'

# Preprocessing 
data_inizio = '01.01.2019 00:00:00,00'
data_fine = '30.05.2019 00:00:00,00'

# model
model_name = 'Gini'
model_name_2 = 'Entropy'


