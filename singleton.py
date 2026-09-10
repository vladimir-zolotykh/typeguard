#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict
import pytest


class Singleton(type):
    _instances = defaultdict(dict)

    def __call__(cls, *args, **kwargs):
        instances = type(cls)._instances
        name = args[0]
        if cls not in instances or name not in instances[cls]:
            instances[cls][name] = super().__call__(*args, **kwargs)
        return instances[cls][name]


class Symbol(metaclass=Singleton):
    def __init__(self, name: str, pat: str = ""):
        print(f"Initializing Symbol({name}, {pat})")
        self.name = name
        self.pat = pat


class Logger(metaclass=Singleton):
    def __init__(self, name: str):
        print(f"Initializing Logger({name})")
        self.name = name


def test_symbol():
    num = Symbol("NUM", r"\d+")
    num2 = Symbol("NUM")
    assert num is num2
    name = Symbol("NAME", r"[A-Za-z_]\w*")
    name2 = Symbol("NAME")
    assert name is name2
    g1 = Logger("sys")
    g2 = Logger("sys")
    assert g1 is g2


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
