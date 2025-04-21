from proof_helper.core.formula import Variable, Not, And, Or, Implies, Iff, Bottom, Formula
from proof_helper.core.proof import StepID, Proof, Statement, Subproof, Step

def parse_formula(data: dict) -> Formula:
    t = data["type"]
    if t == "var":
        return Variable(data["name"])
    if t == "not":
        return Not(parse_formula(data["value"]))
    if t == "and":
        return And(parse_formula(data["left"]), parse_formula(data["right"]))
    if t == "or":
        return Or(parse_formula(data["left"]), parse_formula(data["right"]))
    if t == "implies":
        return Implies(parse_formula(data["left"]), parse_formula(data["right"]))
    if t == "iff":
        return Iff(parse_formula(data["left"]), parse_formula(data["right"]))
    if t == "bottom":
        return Bottom()
    raise ValueError(f"Unknown formula type: {t}")

def parse_statement(data: dict) -> Statement:
    return Statement(
        id=StepID.from_string(data["id"]),
        formula=parse_formula(data["formula"]),
        rule=data.get("rule"),
        premises=[StepID.from_string(pid) for pid in data.get("premises", [])]
    )

def parse_subproof(data: dict) -> Subproof:
    return Subproof(
        id=StepID.from_string(data["id"]),
        assumption=parse_statement(data["assumption"]),
        steps=[parse_step(step) for step in data["steps"]]
    )

def parse_step(data: dict) -> Step:
    if data.get("type") == "subproof":
        return parse_subproof(data)
    return parse_statement(data)

def build_proof(data: dict) -> Proof:
    return Proof(
        premises=[parse_statement(p) for p in data.get("premises", [])],
        steps=[parse_step(s) for s in data.get("steps", [])],
        conclusions=[parse_statement(c) for c in data.get("conclusions", [])]
    )
