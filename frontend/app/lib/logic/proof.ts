import { Constant, Formula } from "frontend/app/lib/logic/logic";

// === Step Types ===

export type Subproof = {
  type: "subproof";
  premise: Statement;
  steps: Step[];
  constants: Constant[];
  number: number;
}

export type Statement = {
  type: "line";
  raw: string;
  result: ParsedFormula;
  rule: string;
  parents: Statement[];
  number: number;
};

export type ParsedFormula = 
  | { status: "ok"; formula: Formula }
  | { status: "empty" }
  | { status: "error"; error: string };

export type Step = Statement | Subproof;

// === Full Proof ===

export type Proof = {
  type: "proof";
  premises: Statement[];
  steps: Step[];
  goals: Statement[];
};