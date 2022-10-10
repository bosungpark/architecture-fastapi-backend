import pytest
from sqlalchemy.orm import Session

from allocation.domain.model import OrderLine
from allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork


def insert_batch(session:Session, ref, sku, qty, eta):
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        " VALUES (:ref, :sku, :qty, :eta)",
        dict(ref=ref, sku=sku, qty=qty, eta=eta)
    )

def get_allocated_batch_ref(session:Session, orderid, sku):
    [[orderlineid]]=session.execute(
        "SELECT id FROM order_lines WHERE orderid= :orderid AND sku= :sku",
        dict(orderid=orderid,sku=sku)
    )
    [[batchref]] = session.execute(
        "SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id"
        " WHERE orderline_id= :orderline_id",
        dict(orderline_id=orderlineid)
    )
    return batchref

def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session=session_factory()
    insert_batch(session, "b1", "bench", 100, None)
    session.commit()

    uow= SqlAlchemyUnitOfWork(session_factory)
    with uow:
        batch = uow.batches.get(reference="b1")
        line= OrderLine("o1","bench",10)
        batch.allocate(line)
        uow.commit()

    batchref= get_allocated_batch_ref(session, "o1", "bench")
    assert batchref=="b1"

def test_rolls_back_uncommited_work_by_default(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session,"b1", "plinth", 100, None)
        # uow.commit()
    new_sesson:Session=session_factory()
    rows=list(new_sesson.execute("SELECT * FROM 'batches'"))
    assert rows==[]

def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session,"b1", "plinth", 100, None)
            raise MyException
    new_sesson:Session=session_factory()
    rows=list(new_sesson.execute("SELECT * FROM 'batches'"))
    assert rows==[]