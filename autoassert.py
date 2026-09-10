#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


def autoassert():
    pass


class Person:
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
