#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
import types
from contextlib import contextmanager
from time import perf_counter
import pytest


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)


@pytest.mark.parametrize(
    "n, res",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
    ],
)
def test_fib(n, res):
    assert fib(n) == res


def ackermann(m, n):
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))


@pytest.mark.parametrize(
    ("m", "n", "expected"),
    [
        (0, 0, 1),
        (0, 1, 2),
        (0, 5, 6),
        (1, 0, 2),
        (1, 1, 3),
        (1, 5, 7),
        (2, 0, 3),
        (2, 1, 5),
        (2, 5, 13),
        (3, 0, 5),
        (3, 1, 13),
        (3, 2, 29),
        (3, 3, 61),
        (3, 4, 125),
    ],
)
def test_ackermann(m: int, n: int, expected: int) -> None:
    assert ackermann(m, n) == expected


class lazyproperty:
    def __init__(self, func: Callable[[int], int]):
        self.func = func
        self.cached = {}

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        cached_name = f"cached_{self.func.__name__}"
        if not hasattr(instance, cached_name):
            setattr(instance, cached_name, self.cached)
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        key = tuple(args)
        if key not in self.cached:
            self.cached[key] = self.func(*args, **kwargs)
        return self.cached[key]


class Box:
    @lazyproperty
    def fib(self, n: int) -> int:
        return fib(n)

    @lazyproperty
    def ackermann(self, m, n):
        return ackermann(m, n)


@contextmanager
def time_counter(label="Fibonacci"):
    start = perf_counter()
    try:
        yield start
    finally:
        elapsed = perf_counter() - start
        print(f"{label} elapsed: {elapsed:.4f}")


def test_lazyproperty():
    box = Box()
    with time_counter("Fibonacci"):
        print(box.fib(40))
    print(box.ackermann(1, 5))


if __name__ == "__main__":
    test_lazyproperty()
