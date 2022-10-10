from datetime import date

import pytest

from allocation.adapters.repository import AbstractRepository
from allocation.domain.model import OrderLine, Batch, allocate
from allocation.service_layer import services
from allocation.service_layer.services import InvalidSku
from allocation.service_layer.unit_of_work import AbstractUnitOfWork


class FakeRepository(AbstractRepository):
    def __init__(self,batches):
        self._batches=set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference==reference)

    def list(self):
        return list(self._batches)

    @staticmethod
    def for_batch(ref, sku, qty, eta=None):
        return FakeRepository([
            Batch(ref, sku, qty, eta=None)
        ])

class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

def test_add_batch():
    uow = FakeUnitOfWork()
    services.add_batch("o1", "LAMP-1", 10, None, uow)

    assert uow.batches.get("o1") is not None
    assert uow.committed

def test_returns_allocation():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "LAMP", 100, eta=None, uow=uow)
    result = services.allocate("o1", "LAMP", 10, uow)
    assert result == "b1"

def test_error_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "LAMP-2", 100, eta=None, uow=uow)

    with pytest.raises(InvalidSku, match=f"Invalid sku LAMP-1"):
        services.allocate("o1", "LAMP-1", 10, uow)

# domain-test
def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch=Batch("in_stock_batch", "clock", 100, eta=None)
    shipment_batch = Batch("shipment_batch", "clock", 100, eta=date.max)
    line=OrderLine("oref", "clock", 10)

    allocate(line, [in_stock_batch,shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

# service-test
def test_prefers_current_stock_batches_to_shipments():
    uow= FakeUnitOfWork()
    services.add_batch("in_stock_batch", "clock", 100, eta=None, uow=uow)
    services.add_batch("shipment_batch", "clock", 100, eta=date.max, uow=uow)

    services.allocate("oref", "clock", 10, uow)

    in_stock_batch =uow.batches.get(reference="in_stock_batch")
    shipment_batch = uow.batches.get(reference="shipment_batch")
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

# outdated
# class FakeSession():
#     commited=False
#
#     def commit(self):
#         self.commited=True
#
# def test_commits():
#     repo = FakeRepository.for_batch("b1", "LAMP", 100, eta=None)
#     session=FakeSession()
#
#     services.allocate("o1", "LAMP", 10, repo, session)
#     assert session.commited is True