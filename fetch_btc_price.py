# fetch_btc_price.py
import requests
from models import BitcoinPrice, create_table_and_connection
from datetime import datetime

time_expected = datetime.now()
time_actual = datetime.fromisoformat(time_expected.isoformat())
assert time_actual == time_expected


from fastapi import APIRouter

router = APIRouter()



def fetch_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    data = response.json()
    price = data["bpi"]["USD"]["rate_float"]
    timestamp = data["time"]["updatedISO"]
    return price, timestamp



def store_bitcoin_price(price, timestamp):
    session = create_table_and_connection()

    bitcoin_price_obj = BitcoinPrice(price=price, timestamp=timestamp)
    session.add(bitcoin_price_obj)

    session.commit()
    session.close()


@router.post("/fetch_btc_price")
async def fetch_and_store_btc_price():
    try:
        # Fetch and store Bitcoin price
        price, timestamp = fetch_bitcoin_price()
        store_bitcoin_price(price, timestamp)
        return {"status": "success", "message": f"Successfully fetched and stored Bitcoin price: {price}, timestamp: {timestamp}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred while fetching and storing Bitcoin price: {e}"}


def test():
    price, timestamp = fetch_bitcoin_price()
    assert isinstance(price, float)
    assert isinstance(timestamp, str)
    dt = datetime.fromisoformat(timestamp)
    assert isinstance(dt, datetime)

