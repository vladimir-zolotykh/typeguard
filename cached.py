#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CachedMeta(type):
    _cached = defaultdict(dict)

    def __call__(cls, *args, **kwargs):
        cached = CachedMeta._cached
        key = cls.key(*args, **kwargs)
        if key not in cached[cls][key]:
            cached[cls][key] = super.__call__(*args, **kwargs)
        return cached[cls][key]


class Person(metaclass=CachedMeta):
    @classmethod
    def key(*args, **kwargs):
        print(f"{args = }, {kwargs = }")
        return tuple(args)

    def __init__(self, name, age, salary):
        for k, v in locals():
            if k != "self":
                setattr(self, k, v)

    def __repr__(self):
        kv = ", ".join("{k}={v}" for k, v in self.__dict__.items())
        return f"Person({kv})"


def test_person():
    bob = Person("Bob", 37, 12000.0)
    assert str(bob) == "Person('Bob', 37, 12000.0)"


if __name__ == "__main__":
    test_person()
