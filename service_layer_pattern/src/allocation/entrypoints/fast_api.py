"""
run cmd: uvicorn src.allocation.entrypoints.fast_api:app --host=127.0.0.1 --port=8000 --reload

service layer pattren
separate between orchrstration logic and business logic
: entry-point to domain model
"""

from fastapi import FastAPI
from fastapi.params import Body

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from src.allocation.adapters.orm import start_mappers
from src.allocation.adapters.repository import SqlAlchemyRepository
from src.allocation.config import get_postgres_uri
from src.allocation.domain.model import OrderLine, allocate

start_mappers()
get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
app = FastAPI()

@app.post("/allocate", status_code=status.HTTP_201_CREATED)
def allocate_endpoint(data=Body()) -> dict:
    session= get_session()
    batches = SqlAlchemyRepository(session).list()
    line = OrderLine(
        data["orderid"],
        data["sku"],
        data["qty"]
    )
    batchref = allocate(line,batches)
    return {"batchref":batchref}