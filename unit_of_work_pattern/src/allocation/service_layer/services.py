from datetime import date
from typing import List, Optional

from allocation.adapters.repository import AbstractRepository
from allocation.domain import model
from allocation.domain.model import SKU, Batch, OrderLine, Reference


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: SKU, batches: List[Batch]):
    return sku in {b.sku for b in batches}

def allocate(orderid:str, sku:str, qty: int, repo:AbstractRepository, session)-> str:
    batches: List[Batch] = repo.list()
    line: OrderLine= OrderLine(orderid=orderid, sku=sku, qty=qty)
    if not is_valid_sku(sku, batches):
        raise InvalidSku(f"Invalid sku {sku}")
    batchref: Reference = model.allocate(line, batches)
    session.commit()
    return batchref

def add_batch(
        ref: str, sku:str, qty: int, eta: Optional[date],
        repo: AbstractRepository, session
):
    repo.add(Batch(ref, sku, qty, eta))
    session.commit()