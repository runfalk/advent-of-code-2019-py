import pytest


from aoc.day4 import is_sorted, has_repetions, is_pw, has_pairs, solve


def test_is_sorted():
    assert is_sorted("abc")
    assert is_sorted("135679")
    assert is_sorted([1, 2, 3])
    assert not is_sorted("acb")
    assert not is_sorted([1, 3, 2])


def test_has_repetions():
    assert has_repetions([1, 1, 1, 2, 3])
    assert has_repetions("122345")
    assert not has_repetions("12345")


def test_has_pairs():
    assert has_pairs("1123")
    assert has_pairs("1233")
    assert has_pairs("11122")
    assert not has_pairs("11123")


def test_is_pw():
    assert is_pw("123455")
    assert not is_pw("123456")


def test_solve():
    assert solve("data/day4.txt") == (1169, 757)
