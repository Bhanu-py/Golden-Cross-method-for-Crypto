import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import plotly.graph_objs as go
import plotly as plo

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_data(tick, short_win=5, long_win=20, period='9d', interval='90m'):
    df = yf.download(tickers=tick.upper() + '-USD', period=period, interval=interval)
    # Moving average using Python Rolling function
    df['shortMA'] = df['Close'].rolling(short_win).mean()
    df['longMA'] = df['Close'].rolling(long_win).mean()
    df['x'] = (df['shortMA'] > df['longMA']).astype(int)
    df['y'] = df['x'].diff()
    df['buy'] = df['Close'][df['y'] > 0]
    df['sell'] = df['Close'][df['y'] < 0]
    return df


def crypto(tick, s_w=5, l_w=20, period='9d', interval='90m'):
    plo.io.orca.config.executable = '/path/to/orca'
    data = get_data(tick, short_win=s_w, long_win=l_w, period=period, interval=interval)
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], opacity=0.5, name='market data'))

    # Add Moving average on the graph
    fig.add_trace(go.Scatter(x=data.index, y=data['longMA'], line=dict(color='blue', width=1.5), name='Long Term MA'))
    fig.add_trace(go.Scatter(x=data.index, y=data['shortMA'], line=dict(color='darkgoldenrod', width=1.5), name='Short Term MA'))
    fig.update_layout(autosize=False, width=900, height=500, margin=dict(l=20, r=20, t=50, b=20), legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.write_image("plot.png")
    # fig.write_image("/home/runner/G-cross/fig1.jpeg")


def notify(tick):
    df = yf.download(tickers=tick.upper() + '-USD', period='9d', interval='90m')
    ma5 = df['close'].iloc[0:5].mean(axis=0)
    ma20 = df['close'].iloc[0:20].mean(axis=0)
    if (ma5 - ma20) == 0:
        return True

# print(crypto('btc'))