import pytest

from allocation.adapters.repository import FakeRepository
from allocation.domain.model import OrderLine, Batch
from allocation.service_layer import services
from allocation.service_layer.services import InvalidSku


class FakeSession():
    commited=False

    def commit(self):
        self.commited=True

def test_commits():
    line = OrderLine("o1", "LAMP", 10)
    batch = Batch("b1", "LAMP", 100, eta=None)
    repo = FakeRepository([batch])
    session=FakeSession()

    services.allocate(line, repo, session)
    assert session.commited is True

def test_returns_allocation():
    line = OrderLine("o1", "LAMP", 10)
    batch = Batch("b1", "LAMP", 100, eta=None)
    repo = FakeRepository([batch])

    result = services.allocate(line, repo, FakeSession())
    assert result == "b1"

def test_error_for_invalid_sku():
    line = OrderLine("o1", "LAMP-1", 10)
    batch = Batch("b1", "LAMP-2", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(InvalidSku, match=f"Invalid sku LAMP-1"):
        result = services.allocate(line, repo, FakeSession())