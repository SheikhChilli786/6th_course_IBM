import pandas as pd
import numpy as np 
import plotly.graph_objects as go 
from plotly.offline import plot
import matplotlib.pyplot as plt 
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

dict_  = {'a':[11,21,31],'b':[12,22,32]}

df = pd.DataFrame(dict_)
cg = CoinGeckoAPI()#creating instance of coingeckoAPI
bitcoin_data = cg.get_coin_market_chart_by_id(id = 'bitcoin' ,vs_currency = 'usd',days = 30) #collecting data about coins for 30 days from https://coingecko.com
bitcoin_price_data = bitcoin_data['prices']#filtering the list of prices out of data
data = pd.DataFrame(bitcoin_price_data,columns=['TimeStamp','Price']) # forming a dataframe of bitcoin price and its Unix-timestamp
data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))#convertime time stamp into yyyy-mm-dd format
candlestick_data  = data.groupby(data.date,as_index = False).agg({'Price':['min','max','first','last']})#initializing a candlestick chart data to give us precise value of... what was the price of bitcoin when market of that day opened,maximum,minimum, and closed
fig = go.Figure(data = [go.Candlestick(x=candlestick_data['date'],open = candlestick_data['Price']['first'],
                                       high = candlestick_data['Price']['max'],
                                       low = candlestick_data['Price']['min'],
                                       close = candlestick_data['Price']['last'])])
#forming a candlestick chart using graphobjects(go) 
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()
print(bitcoin_price_data[0:5])