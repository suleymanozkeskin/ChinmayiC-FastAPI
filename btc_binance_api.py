# btc_binance_api.py
from fastapi import APIRouter
from models import BitcoinOHLC, create_table_and_connection
from datetime import datetime
import requests
import plotly.graph_objects as go
import pandas as pd
from starlette.responses import HTMLResponse

router = APIRouter()

@router.post("/fetch_btc_ohlc")
async def fetch_and_store_btc_ohlc(interval: str = '1d'): 
    try:
        ohlc_data = fetch_bitcoin_ohlc(interval)
        store_bitcoin_ohlc(ohlc_data)
        return {"status": "success", "message": "Successfully fetched and stored Bitcoin OHLC data.Go to http://localhost:8000/btc/plot_btc_ohlc to see the BTC price chart."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred while fetching and storing Bitcoin OHLC data: {e}"}

def fetch_bitcoin_ohlc(interval: str):
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={interval}"
    response = requests.get(url)
    data = response.json()
    ohlc_data = []
    for item in data:
        time_open = datetime.fromtimestamp(item[0] / 1000)
        open_price = float(item[1])
        high_price = float(item[2])
        low_price = float(item[3])
        close_price = float(item[4])
        ohlc_data.append((time_open, open_price, high_price, low_price, close_price))
    return ohlc_data

def store_bitcoin_ohlc(ohlc_data):
    session = create_table_and_connection()
    for item in ohlc_data:
        bitcoin_ohlc_obj = BitcoinOHLC(open_price=item[1], high_price=item[2], low_price=item[3], close_price=item[4], timestamp=item[0])
        session.add(bitcoin_ohlc_obj)
    session.commit()
    session.close()

@router.get("/plot_btc_ohlc", response_class=HTMLResponse)
async def plot_and_get_btc_ohlc():
    session = create_table_and_connection()
    df = pd.read_sql(session.query(BitcoinOHLC).statement, session.bind)
    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                open=df['open_price'],
                high=df['high_price'],
                low=df['low_price'],
                close=df['close_price'])])
    
    fig.update_layout(
        title_text='BTC Price',
        title_font=dict(size=24),  # Increase title font size
        paper_bgcolor='rgba(0,0,0,0)', 
        xaxis_rangeslider_visible=False,  # Remove range slider
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        xaxis=dict(
            gridcolor='darkgray',  # Change grid line color
            gridwidth=1,  # Change grid line width
            linecolor='black',  # Change axis line color
            linewidth=2,  # Change axis line width
        ),
        yaxis=dict(
            gridcolor='darkgray',
            gridwidth=1,
            linecolor='black',
            linewidth=2,
        )
    )

    # use wheel zoom instead of drag
    fig.update_xaxes(fixedrange=False)
    fig.update_yaxes(fixedrange=False)
    # make candlestick bars thicker
    fig.update_traces(line_width=2.5)


    # hide modebar
    fig.update_layout(modebar={'orientation': 'v'})

    
    plot_html = fig.to_html(full_html=False)
    return plot_html



# to test with curl:

# curl -X POST "http://localhost:8000/btc/fetch_btc_ohlc?interval=1h"
# curl -X GET "http://localhost:8000/btc/plot_btc_ohlc"
