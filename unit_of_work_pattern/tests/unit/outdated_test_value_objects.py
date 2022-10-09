# """
# data value obj is identified only by it's data and doesn't have long-lived identity
#
# domain obj that have long-lived identity is entity
# """
#
# from collections import namedtuple
# from dataclasses import dataclass
# from typing import NamedTuple
#
# import pytest
#
# #data value obj
# @dataclass(frozen=True)
# class Name:
#     first_name:str
#     surname:str
#
# class Money(NamedTuple):
#     currency:str
#     value:int
#
# Line=namedtuple("Line", ["sku","qty"])
#
# def test_equality():
#     assert Money("gbp",10)==Money("gbp",10)
#     assert Name("harry","potter") != Name("drake", "malpoy")
#     assert Line("foo",1)==Line("foo",1)
#
# # entity
# class Person:
#     def __init__(self, name: Name):
#         self.name=name
#
# def test_harry_is_malpoy():
#     harry=Person(Name("harry","potter"))
#     malpoy=harry
#
#     malpoy.name=Name("drake", "malpoy")
#     assert harry is malpoy and malpoy is harry