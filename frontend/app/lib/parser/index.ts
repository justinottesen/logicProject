import { Formula } from "frontend/app/lib/logic/logic";
import { ParsedFormula } from "frontend/app/lib/logic/proof";
import { tokenize } from "./tokenizer";
import { Parser } from "./parser";

export function parseFormulaInput(raw: string): ParsedFormula {
  if (raw.trim() === "") {
    return {
      status: "empty"
    }
  }

  try {
    const formula = parseFormula(raw);
    return { status: "ok", formula };
  } catch (err: unknown) {
    return { status: "error", error: getErrorMessage(err) };
  }
}

function parseFormula(input: string): Formula {
  const tokens = tokenize(input);
  const parser = new Parser(tokens);
  const formula = parser.parseFormula();
  parser.expectEOF();
  return formula;
}

function getErrorMessage(err: unknown): string {
  if (err instanceof Error) return err.message;
  return String(err);
}
