#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import wraps
from inspect import signature, _empty


def autoassert(func):
    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, parm in sig.parameters.items():
            if parm.annotation is not _empty:
                assert isinstance(
                    bound.arguments[name], parm.annotation
                ), f"{name!r}: type mismatch, expected {parm.annotation!r}"
        res = func(*args, **kwargs)
        return res

    return wrapper


class Person:
    @autoassert
    def __init__(self, name: str, age: int, salary: float):
        for k, v in locals().items():
            if k == "self":
                continue
            setattr(self, k, v)

    def __repr__(self):
        args = ", ".join(f"{k}={v}" for k, v in vars(self).items())
        return f"Person({args})"


def test_person():
    bob = Person("Bob", 37, 12000.0)
    print(bob)


if __name__ == "__main__":
    test_person()
