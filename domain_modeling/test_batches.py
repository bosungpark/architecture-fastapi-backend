"""
domain model is mental map of that business owner have of their business
"""
import pytest
from datetime import date
from domain_modeling.model import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, linr_qty):
    return (Batch("batch-001", sku, batch_qty, eta=date.today()),
            OrderLine("order-123", sku, linr_qty))

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch=Batch("batch-001","SMALL-TABLE", qty=20, eta=date.today)
    line=OrderLine("order-ref","SMALL-TABLE",2)
    batch.allocate(line)
    assert batch.available_quantity==18

def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line=make_batch_and_line("ELEGANT-LAMP",20,2)
    assert large_batch.can_allocate(small_line)

def test_can_allocate_if_available_smaller_than_required():
    small_batch, large_line=make_batch_and_line("ELEGANT-LAMP",2,20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_smaller_than_required():
    batch, line=make_batch_and_line("ELEGANT-LAMP",2,2)
    assert batch.can_allocate(line)

def test_cannot_allocate_if_skus_do_not_match():
    batch=Batch("batch-001","SMALL-TABLE", qty=20, eta=date.today)
    line=OrderLine("order-ref","BIG-TABLE",2)
    assert batch.can_allocate(line) is False

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    with pytest.raises(KeyError):
        batch.deallocate(unallocated_line)
    assert batch.available_quantity==20

def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity==18