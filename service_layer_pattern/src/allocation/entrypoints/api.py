"""
run cmd: uvicorn src.allocation.entrypoints.fast_api:app --host=127.0.0.1 --port=8000 --reload

service layer pattren
separate between orchrstration logic and e2e api logic
"""
from typing import List

from fastapi import FastAPI
from fastapi.openapi.models import Response
from fastapi.params import Body

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from allocation.service_layer import services
from allocation.service_layer.services import InvalidSku
from src.allocation.adapters.orm import start_mappers
from src.allocation.adapters.repository import SqlAlchemyRepository, AbstractRepository
from src.allocation.config import get_postgres_uri
from src.allocation.domain.model import OrderLine, OutOfStock

start_mappers()
get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
app = FastAPI()

@app.post("/allocate", status_code=201)
def allocate_endpoint(data=Body()) -> dict:
    session : Session = get_session()
    repo : AbstractRepository = SqlAlchemyRepository
    line = OrderLine(
        data["orderid"],
        data["sku"],
        data["qty"]
    )
    try:
        batchref = services.allocate(line, repo, session)
    except (InvalidSku, OutOfStock) as e:
        return {"message": str(e),"status_code":400}
    else:
        return {"batchref" : batchref}