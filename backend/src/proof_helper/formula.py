from __future__ import annotations
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Variable:
    name: str

@dataclass(frozen=True)
class Not:
    value: Formula

@dataclass(frozen=True)
class And:
    left: Formula
    right: Formula

@dataclass(frozen=True)
class Or:
    left: Formula
    right: Formula

@dataclass(frozen=True)
class Implies:
    left: Formula
    right: Formula

@dataclass(frozen=True)
class Iff:
    left: Formula
    right: Formula

Formula = Union[Variable, Not, And, Or, Implies, Iff]