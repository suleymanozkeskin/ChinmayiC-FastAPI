# ChinmayiC-FastAPI

ChinmayiC-FastAPI is a FastAPI-based application that fetches data from SuiteCRM and Bitcoin prices from CoinDesk API and stores the fetched data in a PostgreSQL database. The application provides two main endpoints, one for fetching and storing CRM leads and another for fetching and storing Bitcoin prices.

## Features

- Fetch leads from SuiteCRM and store them in a PostgreSQL database.
- Fetch the current Bitcoin price from the CoinDesk API and store it in a PostgreSQL database.

## Installation

1. Clone the repository: https://github.com/suleymanozkeskin/ChinmayiC-FastAPI.git

2. Create a virtual environment and activate it:

   - cd ChinmayiC-FastAPI
   - python -m venv env
   - source env/bin/activate # For Linux and macOS
   - env\Scripts\activate # For Windows

3. Install the required dependencies:

    pip install -r requirements.txt

4. Set up the PostgreSQL database and update the `create_connection()` function in `models.py` with your database credentials.

5. Run the FastAPI server:

    python main.py

The server will start listening on `http://localhost:8000`.

## Alternative Installation with Docker

    - sudo docker build -t chinmayi_c .
    - sudo docker run -d --name chinmayi_c_container -p 8000:8000 chinmayi_c
The server will start listening on `http://localhost:8000`.

## Usage

You can test the application using an HTTP client like `httpie` or Postman.

1. Fetch and store leads from SuiteCRM:

    http POST http://localhost:8000/fetch_leads username="Demo" password="Demo" rest_url="https://suitecrmdemo.dtbc.eu/service/v4/rest.php"

2. Fetch and store the current Bitcoin price:

    http POST http://localhost:8000/fetch_btc_price

## Project Structure

- `main.py`: The main FastAPI application file that includes the routers for fetching and storing leads and Bitcoin prices.
- `models.py`: Contains the ORM models for the PostgreSQL database and the function for creating a database connection.
- `fetch_leads.py`: Contains the functions for fetching leads from SuiteCRM and storing them in the PostgreSQL database.
- `fetch_btc_price.py`: Contains the functions for fetching the current Bitcoin price from CoinDesk API and storing it in the PostgreSQL database.

## License

This project is licensed under the MIT License.
