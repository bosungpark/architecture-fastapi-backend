from datetime import date

import pytest

from allocation.adapters.repository import AbstractRepository
from allocation.domain.model import OrderLine, Batch, allocate
from allocation.service_layer import services
from allocation.service_layer.services import InvalidSku

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

class FakeSession():
    commited=False

    def commit(self):
        self.commited=True

def test_commits():
    repo = FakeRepository.for_batch("b1", "LAMP", 100, eta=None)
    session=FakeSession()

    services.allocate("o1", "LAMP", 10, repo, session)
    assert session.commited is True

def test_add_batch():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("o1", "LAMP-1", 10, None, repo, session)

    assert repo.get("o1") is not None
    assert session.commited

def test_returns_allocation():
    repo, session = FakeRepository.for_batch("b1", "LAMP", 100, eta=None), FakeSession()
    result = services.allocate("o1", "LAMP", 10, repo, session)
    assert result == "b1"

def test_error_for_invalid_sku():
    repo, session= FakeRepository.for_batch("b1", "LAMP-2", 100, eta=None), FakeSession()

    with pytest.raises(InvalidSku, match=f"Invalid sku LAMP-1"):
        services.allocate("o1", "LAMP-1", 10, repo, session)

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
    in_stock_batch=Batch("in_stock_batch", "clock", 100, eta=None)
    shipment_batch = Batch("shipment_batch", "clock", 100, eta=date.max)
    repo=FakeRepository([in_stock_batch,shipment_batch])
    session=FakeSession()

    services.allocate("oref", "clock", 10, repo, session)

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

