"""
run cmd: uvicorn src.allocation.entrypoints.fast_api:app --host=127.0.0.1 --port=8000 --reload

service layer pattren
separate between orchrstration logic and business logic
: entry-point to domain model
"""
from typing import List

from fastapi import FastAPI
from fastapi.openapi.models import Response
from fastapi.params import Body

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette import status

from src.allocation.adapters.orm import start_mappers
from src.allocation.adapters.repository import SqlAlchemyRepository
from src.allocation.config import get_postgres_uri
from src.allocation.domain.model import OrderLine, allocate, Batch, SKU, Reference, OutOfStock

start_mappers()
get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
app = FastAPI()

def is_valid_sku(sku: SKU, batches: List[Batch]):
    return sku in {b.sku for b in batches}

@app.post("/allocate", status_code=201)
def allocate_endpoint(data=Body(), response=Response) -> dict:
    session : Session = get_session()
    batches : List[Batch] = SqlAlchemyRepository(session).list()
    line = OrderLine(
        data["orderid"],
        data["sku"],
        data["qty"]
    )
    if not is_valid_sku(line.sku, batches):
        return {"message":f"Invalid sku {line.sku}","status_code":400}
    try:
        batchref : Reference = allocate(line,batches)
    except OutOfStock as e:
        return {"message": str(e),"status_code":400}
    else:
        session.commit()
        return {"batchref" : batchref}