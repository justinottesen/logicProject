export const rules = [
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

type FullNamesObject = Record<ShortRules, string>;

export const rulesFullName: FullNamesObject = {
    "∧Elim": "∧ Elimination",
    "∨Elim": "∨ Elimination",
    "¬Elim": "¬ Elimination",
    "⊥Elim": "⊥ Elimination",
    "→Elim": "→ Elimination",
    "↔Elim": "↔ Elimination",
    "∧Intro": "∧ Introduction",
    "∨Intro": "∨ Introduction",
    "¬Intro": "¬ Introduction",
    "⊥Intro": "⊥ Introduction",
    "→Intro": "→ Introduction",
    "↔Intro": "↔ Introduction",
};

export const rulesFullNames = [
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

export type LongRules = "And Elimination" | "Or Elimination" |  "Not Elimination" | "Bottom Elimination" | "Implication Elimination" | "Biconditional Elimination" | "And Introduction" | "Or Introduction" | "Not Introduction" | "Bottom Introduction" | "Implication Introduction" | "Biconditional Introduction";
