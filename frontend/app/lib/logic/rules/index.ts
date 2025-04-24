export const rules: ShortRules[] = [
    "∧Elim",
    "∨Elim",
    "¬Elim",
    "⊥Elim",
    "→Elim",
    "↔Elim",
    "∧Intro",
    "∨Intro",
    "¬Intro",
    "⊥Intro",
    "→Intro",
    "↔Intro",
]

type LongRulesObject = Record<ShortRules, LongRules>;

export const longRuleObjects: LongRulesObject = {
    "∧Elim": "And Elimination",
    "∨Elim": "Or Elimination",
    "¬Elim": "Not Elimination",
    "⊥Elim": "Bottom Elimination",
    "→Elim": "Implication Elimination",
    "↔Elim": "Biconditional Elimination",
    "∧Intro": "And Introduction",
    "∨Intro": "Or Introduction",
    "¬Intro": "Not Introduction",
    "⊥Intro": "Bottom Introduction",
    "→Intro": "Implication Introduction",
    "↔Intro": "Biconditional Introduction",
};

export const longRules = [
    "And Elimination",
    "Or Elimination",
    "Not Elimination",
    "Bottom Elimination",
    "Implication Elimination",
    "Biconditional Elimination",
    "And Introduction",
    "Or Introduction",
    "Not Introduction",
    "Bottom Introduction",
    "Implication Introduction",
    "Biconditional Introduction",
]
export type ShortRules = "∧Elim" | "∨Elim" | "¬Elim" | "⊥Elim" | "→Elim" | "↔Elim" | "∧Intro" | "∨Intro" | "¬Intro" | "⊥Intro" | "→Intro" | "↔Intro";

export type LongRules = "And Elimination" | "Or Elimination" | "Not Elimination" | "Bottom Elimination" | "Implication Elimination" | "Biconditional Elimination" | "And Introduction" | "Or Introduction" | "Not Introduction" | "Bottom Introduction" | "Implication Introduction" | "Biconditional Introduction";
