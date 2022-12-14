import abc

from sqlalchemy.orm import Session

from allocation.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session :Session= session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(model.Product).\
            filter_by(sku=sku).\
            with_for_update().\
            first()