from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
from proof_helper.formula import Formula
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class StepID:
    path: Tuple[int, ...]

    def __str__(self):
        return ".".join(str(x) for x in self.path)
    
    @classmethod
    def from_string(cls, s: str) -> StepID:
        return cls(tuple(int(x) for x in s.split('.')))
    
    def contains(self, other: StepID) -> bool:
        return len(self.path) <= len(other.path) and self.path == other.path[:len(self.path)]
    
    def equals(self, other: StepID) -> bool:
        return self.path == other.path
    
    def is_before(self, other: StepID) -> bool:
        for x, y in zip(self.path, other.path):
            if x < y:
                return True
            if x > y:
                return False
        return len(self.path) < len(other.path)
    
    def is_given_for(self, other: StepID) -> bool:
        return self.is_before(other) and len(self.path) <= len(other.path)
    
@dataclass(frozen=True)
class Step(ABC):
    id: StepID

    @abstractmethod
    def get_step(self, id: StepID) -> Optional[Step]:
        pass

@dataclass(frozen=True)
class Statement(Step):
    formula: Formula
    rule: Optional[str] = None
    premises: List[StepID] = ()
    
    def get_step(self, step: StepID) -> Optional[Step]:
        return self if self.id.equals(step) else None

@dataclass(frozen=True)
class Subproof(Step):
    assumption: Statement
    steps: List[Step]
    
    def get_step(self, step: StepID) -> Optional[Step]:
        for x in [self.assumption] + self.steps:
            if x.id.contains(step):
                return x.get_step(step)
        return None

@dataclass(frozen=True)
class Proof:
    premises: List[Statement]
    steps: List[Step]
    conclusions: List[Statement]
    
    def get_step(self, step: StepID) -> Optional[Step]:
        for x in self.premises + self.steps + self.conclusions:
            if x.id.contains(step):
                return x.get_step(step)
        return None