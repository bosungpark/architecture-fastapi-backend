from dataclasses import dataclass
from datetime import date
from typing import Optional, NewType, List


Quantity=NewType("Quantity", int)
SKU=NewType("SKU",str)
Reference=NewType("Reference",str)

@dataclass
class OrderLine:
    orderid:str
    sku: str
    qty: int

class OutOfStock(Exception):
    pass

class Batch:
    def __init__(self, ref: Reference, sku: SKU, qty: Quantity, eta: Optional[date]):
        self.reference=ref
        self.sku=sku
        self.eta=eta
        self._purchased_quantity=qty
        self._allocations=set()

    def allocate(self, line:OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line:OrderLine):
        if self.can_allocate(line):
            self._allocations.remove(line)

    @property
    def allocated_quantity(self)->int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity-self.allocated_quantity

    def can_allocate(self,line:OrderLine)->bool:
        return self.sku==line.sku and self.available_quantity>=line.qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference==self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta>other.eta

def allocate(line:OrderLine, batches:List[Batch]):
    try:
        batch=next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"out of stock sku {line.sku}")