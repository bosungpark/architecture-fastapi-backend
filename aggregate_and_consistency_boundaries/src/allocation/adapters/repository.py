"""
One Aggregate = One Repository

*BE WARY OF BREAKING IT*
repository should only return aggregates
means aggregates are the only way into out domain model
"""
import abc

from sqlalchemy.orm import Session

from allocation.domain import model
from allocation.domain.model import Product


class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, product: Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractProductRepository):
    def __init__(self,session:Session):
        self.session=session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).one()
