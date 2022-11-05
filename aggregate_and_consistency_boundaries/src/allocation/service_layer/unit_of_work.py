import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from allocation import config
from allocation.adapters.repository import AbstractRepository, SqlAlchemyRepository


class AbstractUnitOfWork(abc.ABC):
    products: AbstractRepository

    def __exit__(self, *args):
        self.rollback()

    def __enter__(self):
        return self

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

DEFAULT_SESSION_FACTORY=sessionmaker(bind=create_engine(
    config.get_postgres_uri(),
    # 데이터의의 정합성에 관한 설정
    isolation_level="REPEATABLE READ",
))

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory=session_factory

    def __enter__(self):
        self.session : Session= self.session_factory()
        self.products = SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()