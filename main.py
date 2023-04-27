from fastapi import FastAPI
from pydantic import BaseModel
import requests
import hashlib
import json
from models import Lead, create_table_and_connection
from fetch_btc_price import router as btc_router


app = FastAPI()

app.include_router(btc_router)


class LoginData(BaseModel):
    username: str
    password: str
    rest_url: str

def fetch_leads(username: str, password: str, rest_url: str):
    # Generate MD5 password hash
    md5_password = hashlib.md5(password.encode()).hexdigest()

    # Login and get session ID
    login_data = {
        "method": "login",
        "input_type": "JSON",
        "response_type": "JSON",
        "rest_data": json.dumps({
            "user_auth": {
                "user_name": username,
                "password": md5_password,
            },
            "application_name": "FastAPI_SuiteCRM",
        })
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    login_response = requests.post(rest_url, data=login_data, headers=headers)

    print(login_response.status_code)
    print(login_response.text)

    session_id = login_response.json()["id"]

    # Fetch leads
    get_leads_data = {
        "method": "get_entry_list",
        "input_type": "JSON",
        "response_type": "JSON",
        "rest_data": json.dumps({
            "session": session_id,
            "module_name": "Leads",
            "query": "",
            "order_by": "",
            "offset": 0,
            "select_fields": ["id", "phone_work", "first_name", "last_name"],
            "max_results": 100,
        })
    }

    get_leads_response = requests.post(rest_url, data=get_leads_data, headers=headers)
    leads = get_leads_response.json()["entry_list"]

    return leads


import psycopg2

def create_connection():
    connection = psycopg2.connect(
        dbname="ChinmayiC",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
    )
    return connection

def store_leads(leads):
    session = create_table_and_connection()

    for lead in leads:
        print(lead)  # To see the response structure
        lead_data = lead["name_value_list"]
        lead_obj = Lead(
            id=lead_data["id"]["value"],
            phone_work=lead_data["phone_work"]["value"],
            first_name=lead_data["first_name"]["value"],
            last_name=lead_data["last_name"]["value"],
        )
        session.merge(lead_obj)

    session.commit()
    session.close()


@app.post("/fetch_leads")
async def fetch_and_store_leads(login_data: LoginData):
    leads = fetch_leads(login_data.username, login_data.password, login_data.rest_url)
    store_leads(leads)
    return {"status": "success", "message": "Leads fetched and stored"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)






