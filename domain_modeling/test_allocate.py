from datetime import date

import pytest

from domain_modeling.model import Batch, OrderLine, OutOfStock, allocate


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch=Batch("batch-001","SMALL-TABLE", qty=10, eta=date.today)
    line = OrderLine("order-ref", "SMALL-TABLE", 10)
    allocate(line, [batch])

    with pytest.raises(OutOfStock, match="SMALL-TABLE"):
        allocate(line, [batch])