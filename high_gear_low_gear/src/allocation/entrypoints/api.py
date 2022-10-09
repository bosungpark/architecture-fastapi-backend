"""
run cmd: uvicorn src.allocation.entrypoints.api:app --host=127.0.0.1 --port=8000 --reload

service layer pattren
separate between orchrstration logic and e2e api logic
"""
from datetime import datetime

from fastapi import FastAPI
from fastapi.params import Body

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.allocation.service_layer import services
from src.allocation.service_layer.services import InvalidSku
from src.allocation.adapters.orm import start_mappers
from src.allocation.adapters.repository import SqlAlchemyRepository, AbstractRepository
from src.allocation.config import get_postgres_uri
from src.allocation.domain.model import OrderLine, OutOfStock

start_mappers()
get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
app = FastAPI()

@app.post("/allocate", status_code=201)
def allocate_endpoint(data=Body()) -> dict:
    orderid=data["orderid"]
    sku=data["sku"]
    qty=data["qty"]
    session : Session = get_session()
    repo : AbstractRepository = SqlAlchemyRepository(session)
    try:
        batchref = services.allocate(orderid, sku, qty, repo, session)
    except (InvalidSku, OutOfStock) as e:
        return {"message": str(e),"status_code":400}
    else:
        return {"batchref" : batchref}

@app.post("/batch", status_code=201)
def add_batch(data=Body()) -> str:
    session : Session = get_session()
    repo : AbstractRepository = SqlAlchemyRepository(session)
    eta=data["eta"]
    if eta:
        eta=datetime.fromisoformat(eta).date()

    services.add_batch(
        data["ref"],
        data["sku"],
        data["qty"],
        eta,
        repo,
        session
    )
    return "OK"