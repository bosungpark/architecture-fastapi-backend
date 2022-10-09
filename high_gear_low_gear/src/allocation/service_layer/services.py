from typing import List

from src.allocation.adapters.repository import AbstractRepository
from src.allocation.domain import model
from src.allocation.domain.model import SKU, Batch, OrderLine, Reference


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: SKU, batches: List[Batch]):
    return sku in {b.sku for b in batches}

def allocate(orderid:str, sku:str, qty: int, repo:AbstractRepository, session)-> str:
    batches: List[Batch] = repo.list()
    line: OrderLine= OrderLine(orderid=orderid, sku=sku, qty=qty)
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref: Reference = model.allocate(line, batches)
    session.commit()
    return batchref