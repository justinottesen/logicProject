import { Formula } from "@lib/logic/logic";

// === Step Types ===

export type Subproof = {
  type: "subproof";
  premise: Statement;
  steps: Step[];
}

export type Statement = {
  type: "line";
  raw: string;
  result: ParsedFormula;
};

export type ParsedFormula = 
  | { status: "ok"; formula: Formula }
  | { status: "error"; error: string };

export type Step = Statement | Subproof;

// === Full Proof ===

export type Proof = {
  type: "proof";
  premises: Statement[];
  steps: Step[];
  goals: Statement[];
};