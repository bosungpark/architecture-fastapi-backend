"""
run cmd: uvicorn src.allocation.entrypoints.api:app --host=127.0.0.1 --port=8000 --reload
"""

import uuid

import pytest
import requests

from allocation import config


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock):
    sku, othersku=random_sku(), random_sku("other")
    earlybatch= random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock([
        (laterbatch, sku, 100, "2022-01-02"),
        (earlybatch, sku, 100, "2022-01-01"),
        (otherbatch, othersku, 100, None)
    ])
    data={"orderid": random_orderid(), "sku": sku, "qty": 3}
    url= config.get_api_url()
    r= requests.post(url=f"{url}/allocate", json=data)
    assert r.status_code== 201
    assert r.json()["batchref"] == earlybatch

@pytest.mark.usefixtures("restart_api")
def test_api_returns_are_persisted(add_stock):
    sku=random_sku()
    batch1, batch2 = random_batchref(1), random_batchref(2)
    order1, order2 = random_orderid(1), random_orderid(2)
    add_stock([
        (batch1, sku, 100, "2022-01-01"),
        (batch2, sku, 100, "2022-01-02"),
    ])
    # _____save_____
    line1={"orderid": order1, "sku": sku, "qty": 100}
    line2 = {"orderid": order2, "sku": sku, "qty": 100}
    url= config.get_api_url()

    r= requests.post(url=f"{url}/allocate", json=line1)
    assert r.status_code== 201
    assert r.json()["batchref"] == batch1

    r = requests.post(url=f"{url}/allocate", json=line2)
    assert r.status_code == 201
    assert r.json()["batchref"] == batch2

@pytest.mark.usefixtures("restart_api")
def test_400_for_out_of_stock(add_stock):
    sku, smalll_batch, large_order= random_sku(), random_batchref(), random_orderid()
    add_stock([
        (smalll_batch, sku, 10, None)
    ])
    data={"orderid": large_order, "sku": sku, "qty": 100}
    url = config.get_api_url()

    r = requests.post(url=f"{url}/allocate", json=data)
    assert r.json()["status_code"] == 400
    assert r.json()["message"] == f"out of stock sku {sku}"

@pytest.mark.usefixtures("restart_api")
def test_400_for_invalid_sku(add_stock):
    unknown_sku, orderid= random_sku(), random_orderid()
    data={"orderid": orderid, "sku": unknown_sku, "qty": 100}
    url = config.get_api_url()

    r = requests.post(url=f"{url}/allocate", json=data)
    assert r.json()["status_code"] == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"