from proof_helper.core.formula import Variable, Not, Bottom, Or
from proof_helper.core.proof import Proof, Subproof
from proof_helper.io.parse_proof import parse_proof_text

def test_parse_excluded_middle(monkeypatch):
    P = Variable("P")
    not_p = Not(P)
    p_or_not_p = Or(P, not_p)
    bottom = Bottom()

    content = """
    Excluded Middle
    |           ; No premises necessary, this is a comment
    |--------------
    | | 1.1: ¬(P ∨ ¬P) 'Assumption' []
    | |-------------------------------
    | | | 1.2.1: P 'Assumption' []
    | | |-------------------------
    | | | 1.2.2: P ∨ ¬P 'Or Introduction' [1.2.1]
    | | | 1.2.3: ⊥ 'Bottom Introduction' [1.1, 1.2.1]
    | | >
    | | 1.3: ¬P 'Not Introduction' [1.2]
    | | 1.4: P ∨ ¬P 'Or Introduction' [1.3]
    | | 1.5: ⊥ 'Bottom Introduction' [1.1, 1.4]
    | >
    | 2. ¬¬(P ∨ ¬P) 'Not Introduction' [1]
    | 3. P ∨ ¬P 'Not Elimination' [2]
    |---------------
    | 4. P ∨ ¬P 'Reiteration' [3]
    """

    proof = parse_proof_text(content)

    assert isinstance(proof, Proof)
    assert proof.premises == []
    assert len(proof.steps) == 3
    assert isinstance(proof.steps[0], Subproof)
    assert proof.steps[1].formula == Not(Not(p_or_not_p))
    assert proof.steps[2].formula == p_or_not_p
    assert proof.conclusions[0].formula == p_or_not_p
