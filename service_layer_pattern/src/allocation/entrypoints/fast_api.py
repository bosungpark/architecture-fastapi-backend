"""
service layer pattren
separate between orchrstration logic and business logic
: entry-point to domain model
"""

from fastapi import Body, FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.allocation.adapters.orm import start_mappers
from src.allocation.adapters.repository import SqlAlchemyRepository
from src.allocation.config import get_postgres_uri
from src.allocation.domain.model import OrderLine, allocate

start_mappers()
get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
app = FastAPI()

@app.post("/allocate", status_code=202)
def allocate_endpoint() -> dict:
    print("!!")
    session= get_session()
    batches = SqlAlchemyRepository(session).list()
    line = OrderLine(
        # data["orderid"],
        # data["sku"],
        # data["qty"]
    )

    batchref = allocate(line,batches)
    return {"batchref":batchref}