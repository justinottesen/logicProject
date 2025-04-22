from proof_helper.core.formula import Formula, Variable, Not, And, Or, Implies, Iff, Bottom

def score_similarity(f1: Formula, f2: Formula) -> float:
    if type(f1) != type(f2):
        return 0.0

    if isinstance(f1, Variable) and isinstance(f2, Variable):
        return 1.0 if f1.name == f2.name else 0.0

    if isinstance(f1, Bottom):
        return 1.0  # All bottoms are the same

    if isinstance(f1, Not):
        return 0.9 * score_similarity(f1.value, f2.value)

    if isinstance(f1, And) or isinstance(f1, Or):
        # commutative — take best matching
        scores = [
            (score_similarity(f1.left, f2.left) + score_similarity(f1.right, f2.right)) / 2,
            (score_similarity(f1.left, f2.right) + score_similarity(f1.right, f2.left)) / 2
        ]
        return 0.9 * max(scores)

    if isinstance(f1, Implies) or isinstance(f1, Iff):
        return 0.9 * ((score_similarity(f1.left, f2.left) + score_similarity(f1.right, f2.right)) / 2)

    return 0.0
