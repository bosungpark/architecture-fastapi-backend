from datetime import date

from sqlalchemy.orm import Session

from repository_pattern import model, repository


def test_repository_can_save_a_batch(session:Session):
    batch=model.Batch("batch-001","SMALL-TABLE", qty=20, eta=None)

    repo=repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows=list(session.execute(
        "SELECT reference, sku, _purchased_quantity, eta FROM 'batches'"
    ))

    assert rows==[("batch-001","SMALL-TABLE", 20, None)]

def insert_order_line(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES ('order1','sofa',12)"
    )
    [[orderline_id]]=session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1",sku="sofa")
    )
    return orderline_id

def insert_batch(session,reference):
    session.execute(
        f"INSERT INTO batches (reference, sku, _purchased_quantity) VALUES (:reference,'sofa',12)",
        dict(reference=reference)
    )
    [[reference]] = session.execute(
        "SELECT id FROM batches WHERE reference=:reference AND sku=:sku",
        dict(reference=reference,sku="sofa")
    )
    return reference

def insert_allocation(session,orderline_id,batch_id):
    session.execute(
        f"INSERT INTO allocations (orderline_id,batch_id) VALUES ({orderline_id},{batch_id})"
    )
    [[reference]] = session.execute(
        "SELECT id FROM allocations WHERE orderline_id=:orderline_id AND batch_id=:batch_id",
        dict(orderline_id=orderline_id, batch_id=batch_id)
    )
    return reference

def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id=insert_order_line(session)
    batch_reference1=insert_batch(session,"batch_reference1")
    insert_batch(session, "batch_reference2")
    insert_allocation(session,orderline_id,batch_reference1)

    repo=repository.SqlAlchemyRepository(session)
    retrieved=repo.get("batch_reference1")

    expected=model.Batch("batch_reference1",'sofa',12,eta=None)
    assert retrieved==expected
