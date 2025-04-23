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
    "∧ Elimination",
    "∨ Elimination",
    "¬ Elimination",
    "⊥ Elimination",
    "→ Elimination",
    "↔ Elimination",
    "∧ Introduction",
    "∨ Introduction",
    "¬ Introduction",
    "⊥ Introduction",
    "→ Introduction",
    "↔ Introduction",
]
export type ShortRules = "∧Elim" | "∨Elim" | "¬Elim" | "⊥Elim" | "→Elim" | "↔Elim" | "∧Intro" | "∨Intro" | "¬Intro" | "⊥Intro" | "→Intro" | "↔Intro";
export type FullNames = "∧ Elimination" | "∨ Elimination" | "¬ Elimination" | "⊥ Elimination" | "→ Elimination" | "↔ Elimination" | "∧ Introduction" | "∨ Introduction" | "¬ Introduction" | "⊥ Introduction" | "→ Introduction" | "↔ Introduction";
