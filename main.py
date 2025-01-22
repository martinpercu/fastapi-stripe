import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep

app = FastAPI()

@app.get("/")
async def root():
        return {"message": "Hola universoddssqdd"}


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get('/time/{iso_code}')
async def time(iso_code: str):
        iso = iso_code.upper()
        timezone_string = country_timezones.get(iso)
        tz = zoneinfo.ZoneInfo(timezone_string)
        return{'time': datetime.now(tz),
               'pais timezone_string': timezone_string,
               'iso en mayusculas': iso}

db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
       customer = Customer.model_validate(customer_data.model_dump())
       # customer is to use de DB
       customer.id = len(db_customers)
       db_customers.append(customer)       
       return customer

@app.get("/customers", response_model=list[Customer])
async def list_customers():     
       return db_customers



@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
       return transaction_data


@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
       breakpoint()
       return invoice_data
