from datetime import date
from typing import List, Optional

from allocation.domain import model
from allocation.domain.model import SKU, Batch, OrderLine, Reference
from allocation.service_layer.unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: SKU, batches: List[Batch]):
    return sku in {b.sku for b in batches}

def allocate(orderid:str, sku:str, qty: int,
             uow: AbstractUnitOfWork)-> str:
    line: OrderLine = OrderLine(orderid=orderid, sku=sku, qty=qty)
    with uow:
        batches: List[Batch] = uow.batches.list()

        if not is_valid_sku(sku, batches):
            raise InvalidSku(f"Invalid sku {sku}")
        batchref: Reference = model.allocate(line, batches)
        uow.commit()
    return batchref


def reallocate(orderid:str, sku:str, qty: int,
             uow: AbstractUnitOfWork)-> str:
    line: OrderLine = OrderLine(orderid=orderid, sku=sku, qty=qty)
    with uow:
        batch: Batch = uow.batches.get(sku)
        if batch is None:
            raise InvalidSku(f"Invalid sku {sku}")
        batch.deallocate(line)
        allocate(line)
        uow.commit()

def add_batch(
        ref: str, sku:str, qty: int, eta: Optional[date],
        uow: AbstractUnitOfWork
):
    with uow:
        uow.batches.add(Batch(ref, sku, qty, eta))
        uow.commit()