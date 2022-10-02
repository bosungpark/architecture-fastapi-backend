from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base=declarative_base()

class Order(Base):
    id=Column(Integer, primary_key=True)

class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku=Column(String(250))
    qty=Integer(String(250))
    order_id=Column(Integer, ForeignKey("order.id"))
    order=relationship(Order)

class Allocation(Base):
    ...