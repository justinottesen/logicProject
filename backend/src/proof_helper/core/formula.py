from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Dict

# === Base Formatting Helper ===

def format_formula(formula: Formula, parent_prec: int) -> str:
    return formula._to_string(parent_prec)

# === Formula Classes ===

@dataclass(frozen=True)
class Variable:
    name: str

    def precedence(self) -> int:
        return 100  # Highest precedence

    def _to_string(self, parent_prec: int) -> str:
        return self.name

    def __str__(self) -> str:
        return self._to_string(0)

    def __repr__(self) -> str:
        return self._to_string(0)
    
    def match(self, other: Formula, subst: Dict[str, Formula]) -> bool:
        if self.name in subst:
            return subst[self.name] == other
        subst[self.name] = other
        return True
    
    def substitute(self, subst: dict[str, Formula]) -> Formula:
        return subst.get(self.name, self)

@dataclass(frozen=True)
class Bottom:
    def precedence(self) -> int:
        return 100

    def _to_string(self, parent_prec: int) -> str:
        return "⊥"

    def __str__(self) -> str:
        return self._to_string(0)

    def __repr__(self) -> str:
        return self._to_string(0)
    
    def match(self, other: Formula, subst: dict[str, Formula]) -> bool:
        return isinstance(other, Bottom)
    
    def substitute(self, subst: dict[str, Formula]) -> Formula:
        return self

@dataclass(frozen=True)
class Not:
    value: Formula

    def precedence(self) -> int:
        return 5

    def _to_string(self, parent_prec: int) -> str:
        inner = format_formula(self.value, self.precedence())
        return f"¬{inner}"

    def __str__(self) -> str:
        return self._to_string(0)

    def __repr__(self) -> str:
        return self._to_string(0)
    
    def match(self, other: Formula, subst: dict[str, Formula]) -> bool:
        return isinstance(other, Not) and \
               self.value.match(other.value, subst)
    
    def substitute(self, subst: dict[str, Formula]) -> Formula:
        return Not(self.value.substitute(subst))

@dataclass(frozen=True)
class And:
    left: Formula
    right: Formula

    def precedence(self) -> int:
        return 4

    def _to_string(self, parent_prec: int) -> str:
        lp = format_formula(self.left, self.precedence())
        rp = format_formula(self.right, self.precedence() + 1)
        s = f"{lp} ∧ {rp}"
        return f"({s})" if self.precedence() < parent_prec else s

    def __str__(self) -> str:
        return self._to_string(0)

    def __repr__(self) -> str:
        return self._to_string(0)
    
    def match(self, other: Formula, subst: dict[str, Formula]) -> bool:
        return isinstance(other, And) and \
               self.left.match(other.left, subst) and \
               self.right.match(other.right, subst)

    def substitute(self, subst: dict[str, Formula]) -> Formula:
        return And(self.left.substitute(subst), self.right.substitute(subst))

@dataclass(frozen=True)
class Or:
    left: Formula
    right: Formula

    def precedence(self) -> int:
        return 3

    def _to_string(self, parent_prec: int) -> str:
        lp = format_formula(self.left, self.precedence())
        rp = format_formula(self.right, self.precedence() + 1)
        s = f"{lp} ∨ {rp}"
        return f"({s})" if self.precedence() < parent_prec else s

    def __str__(self) -> str:
        return self._to_string(0)

    def __repr__(self) -> str:
        return self._to_string(0)
    
    def match(self, other: Formula, subst: dict[str, Formula]) -> bool:
        return isinstance(other, Or) and \
               self.left.match(other.left, subst) and \
               self.right.match(other.right, subst)
    
    def substitute(self, subst: dict[str, Formula]) -> Formula:
        return Or(self.left.substitute(subst), self.right.substitute(subst))

@dataclass(frozen=True)
class Implies:
    left: Formula
    right: Formula

    def precedence(self) -> int:
        return 2

    def _to_string(self, parent_prec: int) -> str:
        lp = format_formula(self.left, self.precedence() + 1)
        rp = format_formula(self.right, self.precedence())
        s = f"{lp} → {rp}"
        return f"({s})" if self.precedence() < parent_prec else s

    def __str__(self) -> str:
        return self._to_string(0)

    def __repr__(self) -> str:
        return self._to_string(0)
    
    def match(self, other: Formula, subst: dict[str, Formula]) -> bool:
        return isinstance(other, Implies) and \
               self.left.match(other.left, subst) and \
               self.right.match(other.right, subst)
    
    def substitute(self, subst: dict[str, Formula]) -> Formula:
        return Implies(self.left.substitute(subst), self.right.substitute(subst))

@dataclass(frozen=True)
class Iff:
    left: Formula
    right: Formula

    def precedence(self) -> int:
        return 1

    def _to_string(self, parent_prec: int) -> str:
        lp = format_formula(self.left, self.precedence() + 1)
        rp = format_formula(self.right, self.precedence())
        s = f"{lp} ↔ {rp}"
        return f"({s})" if self.precedence() < parent_prec else s

    def __str__(self) -> str:
        return self._to_string(0)

    def __repr__(self) -> str:
        return self._to_string(0)
    
    def match(self, other: Formula, subst: dict[str, Formula]) -> bool:
        return isinstance(other, Iff) and \
               self.left.match(other.left, subst) and \
               self.right.match(other.right, subst)
    
    def substitute(self, subst: dict[str, Formula]) -> Formula:
        return Or(self.left.substitute(subst), self.right.substitute(subst))

# Final union
Formula = Union[Variable, Not, And, Or, Implies, Iff, Bottom]
