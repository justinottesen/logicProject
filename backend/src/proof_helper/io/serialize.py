from proof_helper.core.formula import Variable, Not, And, Or, Implies, Iff, Bottom, Formula
from proof_helper.core.proof import StepID, Statement, Subproof, Step, Proof

def dump_formula(f: Formula) -> dict:
    if isinstance(f, Variable):
        return {"type": "var", "name": f.name}
    if isinstance(f, Not):
        return {"type": "not", "value": dump_formula(f.value)}
    if isinstance(f, And):
        return {"type": "and", "left": dump_formula(f.left), "right": dump_formula(f.right)}
    if isinstance(f, Or):
        return {"type": "or", "left": dump_formula(f.left), "right": dump_formula(f.right)}
    if isinstance(f, Implies):
        return {"type": "implies", "left": dump_formula(f.left), "right": dump_formula(f.right)}
    if isinstance(f, Iff):
        return {"type": "iff", "left": dump_formula(f.left), "right": dump_formula(f.right)}
    if isinstance(f, Bottom):
        return {"type": "bottom"}
    raise TypeError(f"Cannot serialize formula type: {type(f)}")

def dump_statement(s: Statement) -> dict:
    return {
        "id": str(s.id),
        "formula": dump_formula(s.formula),
        "rule": s.rule,
        "premises": [str(p) for p in s.premises]
    }

def dump_subproof(sp: Subproof) -> dict:
    return {
        "id": str(sp.id),
        "type": "subproof",
        "assumption": dump_statement(sp.assumption),
        "steps": [dump_step(step) for step in sp.steps]
    }

def dump_step(step: Step) -> dict:
    if isinstance(step, Subproof):
        return dump_subproof(step)
    if isinstance(step, Statement):
        return dump_statement(step)
    raise TypeError(f"Cannot serialize step type: {type(step)}")

def dump_proof(proof: Proof) -> dict:
    return {
        "premises": [dump_statement(p) for p in proof.premises],
        "steps": [dump_step(s) for s in proof.steps],
        "conclusions": [dump_statement(c) for c in proof.conclusions]
    }
