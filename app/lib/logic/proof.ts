import { Formula } from "@lib/logic/logic";

// === Step Types ===

export type Statement = {
  type: "line";
  raw: string;
  result: ParsedFormula;
};

export type ParsedFormula = 
  | { status: "ok"; formula: Formula }
  | { status: "error"; error: string };

export type Step = Statement | Proof;

// === Full Proof ===

export type Proof = {
  type: "proof";
  premises: Statement[]; // Premises can't have subproofs
  steps: Step[]; // Steps can be either statements or subproofs
};