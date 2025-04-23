from abc import ABC, abstractmethod
from typing import Optional
from proof_helper.core.proof import Step, Statement
from proof_helper.core.formula import Formula

class Rule(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def num_supports(self) -> Optional[int]:
        """Return number of required support steps, or None for variable."""
        pass

    @abstractmethod
    def is_applicable(self, supports: list[Step]) -> bool:
        """Return True if the rule could be applied to these steps (structure-only)."""
        pass

    @abstractmethod
    def verify(self, supports: list[Step], conclusion: Statement) -> bool:
        """Return True if the conclusion follows from supports via this rule."""
        pass

    @abstractmethod
    def conclude(self, supports: list[Step]) -> list[Formula]:
        """Return a list of formulas that can be concluded from a rule application"""
        return []
