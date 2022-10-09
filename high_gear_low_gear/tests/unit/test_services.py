from datetime import date

import pytest

from allocation.adapters.repository import FakeRepository
from allocation.domain.model import OrderLine, Batch, allocate
from allocation.service_layer import services
from allocation.service_layer.services import InvalidSku


class FakeSession():
    commited=False

    def commit(self):
        self.commited=True

def test_commits():
    batch = Batch("b1", "LAMP", 100, eta=None)
    repo = FakeRepository([batch])
    session=FakeSession()

    services.allocate("o1", "LAMP", 10, repo, session)
    assert session.commited is True

def test_returns_allocation():
    batch = Batch("b1", "LAMP", 100, eta=None)
    repo = FakeRepository([batch])

    result = services.allocate("o1", "LAMP", 10, repo, FakeSession())
    assert result == "b1"

def test_error_for_invalid_sku():
    batch = Batch("b1", "LAMP-2", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(InvalidSku, match=f"Invalid sku LAMP-1"):
        services.allocate("o1", "LAMP-1", 10, repo, FakeSession())

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

