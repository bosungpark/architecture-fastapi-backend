# from sqlalchemy.orm import Session
#
# from repository_pattern import model
#
#
# def test_orderline_mapper_can_load_lines(session:Session):
#     session.execute(
#         "INSERT INTO order_lines (orderid, sku, qty) VALUES ('order1','chair', 12)"
#     )
#     expected=[
#         model.OrderLine(orderid= 'order1', sku='chair', qty=12)
#     ]
#     assert session.query(model.OrderLine).all() == expected