import { Constant, Formula } from "@lib/logic/logic";

// === Step Types ===

export type Subproof = {
  type: "subproof";
  premise: Statement;
  raw: string;
  steps: Step[];
  constantsRaw: string;
  number: number;
}

export type Statement = {
  type: "line";
  raw: string;
  result: ParsedFormula;
  rule: string;
  parents: Statement[];
  parentsRaw: string;
  number: number;
};

export type Premise = {
  type: "premise";
  raw: string;
  result: ParsedFormula;
  rule: "none";
  number: number;
}
export type Goal = {
  type: "goal";
  raw: string;
  result: ParsedFormula;
  rule: "none";
  number: number;
}

export type ParsedFormula =
  | { status: "ok"; formula: Formula }
  | { status: "empty" }
  | { status: "error"; error: string };

export type Step = Statement | Subproof;

export type ProofStep = Premise | Statement | Subproof;

// === Full Proof ===

export type Proof = {
  type: "proof";
  premises: Premise[];
  steps: Step[];
  goals: Goal[];
};