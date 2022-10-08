from typing import List

from allocation.adapters.repository import AbstractRepository
from allocation.domain import model
from allocation.domain.model import SKU, Batch, OrderLine, Reference


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: SKU, batches: List[Batch]):
    return sku in {b.sku for b in batches}

def allocate(line:OrderLine, repo:AbstractRepository, session)-> str:
    batches: List[Batch] = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref: Reference = model.allocate(line, batches)
    session.commit()
    return batchref