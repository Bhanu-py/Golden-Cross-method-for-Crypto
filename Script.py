import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data = yf.download(tickers='ETH-USD', period='10d', interval='90m')
print(data.columns)

# Moving average using Python Rolling function
data['MA5'] = data['Close'].rolling(5).mean()
data['MA20'] = data['Close'].rolling(20).mean()
print(data)

plt.plot(data.index.values, data['MA5'], color='orange')
plt.plot(data.index.values, data['MA20'], color='blue')

plt.show()
