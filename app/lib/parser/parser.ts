// app/lib/parser/parser.ts

import { Token } from "./tokenizer";
import { Formula, Predicate, Term } from "@/lib/logic/logic";

export class Parser {
  private tokens: Token[];
  private pos = 0;

  constructor(tokens: Token[]) {
    this.tokens = tokens;
  }

  private current(): Token {
    return this.tokens[this.pos];
  }

  private advance(): void {
    this.pos++;
  }

  private matchSymbol(sym: string): boolean {
    const token = this.current();
    if (token.type === "symbol" && token.value === sym) {
      this.advance();
      return true;
    }
    return false;
  }

  private expectSymbol(sym: string): void {
    if (!this.matchSymbol(sym)) {
      throw new Error(`Expected symbol '${sym}', got '${this.current().type === "symbol" ? this.current().value : this.current().type}'`);
    }
  }

  public expectEOF(): void {
    if (this.current().type !== "eof") {
      throw new Error("Unexpected input after formula");
    }
  }

  public parseFormula(): Formula {
    return this.parseIff();
  }

  // === Operator precedence ===

  private parseIff(): Formula {
    let left = this.parseImplies();
    while (this.matchSymbol("↔")) {
      const right = this.parseImplies();
      left = { type: "iff", left, right };
    }
    return left;
  }

  private parseImplies(): Formula {
    let left = this.parseOr();
    while (this.matchSymbol("→")) {
      const right = this.parseOr();
      left = { type: "implies", left, right };
    }
    return left;
  }

  private parseOr(): Formula {
    let left = this.parseAnd();
    while (this.matchSymbol("∨")) {
      const right = this.parseAnd();
      left = { type: "or", left, right };
    }
    return left;
  }

  private parseAnd(): Formula {
    let left = this.parseUnary();
    while (this.matchSymbol("∧")) {
      const right = this.parseUnary();
      left = { type: "and", left, right };
    }
    return left;
  }

  private parseUnary(): Formula {
    if (this.matchSymbol("¬")) {
      const operand = this.parseUnary();
      return { type: "not", operand };
    }
    return this.parseQuantifier();
  }

  private parsePrimary(): Formula {
    const token = this.current();

    if (token.type === "symbol" && token.value === "(") {
      this.advance();
      const inner = this.parseFormula();
      this.expectSymbol(")");
      return inner;
    }

    if (token.type === "identifier") {
      return this.parsePredicate();
    }

    throw new Error(`Unexpected token: ${JSON.stringify(token)}`);
  }

  private parsePredicate(): Predicate {
    const nameToken = this.current();
    if (nameToken.type !== "identifier") {
      throw new Error("Expected predicate name");
    }
    const name = nameToken.value;
    this.advance();

    const args: Term[] = [];

    if (this.matchSymbol("(")) {
      if (!this.matchSymbol(")")) {
        do {
          const argToken = this.current();
          if (argToken.type !== "identifier") {
            throw new Error("Expected term identifier");
          }
          const argName = argToken.value;
          this.advance();

          const isVariable = /^[a-z]$/.test(argName);
          const term: Term = isVariable
            ? { type: "variable", name: argName }
            : { type: "constant", name: argName };

          args.push(term);
        } while (this.matchSymbol(","));

        this.expectSymbol(")");
      }
    }

    return { type: "predicate", name, args };
  }

  private parseQuantifier(): Formula {
    const token = this.current();
  
    let quantifierType: "forall" | "exists" | null = null;
  
    if (token.type === "symbol" && token.value === "∀") {
      quantifierType = "forall";
    } else if (token.type === "symbol" && token.value === "∃") {
      quantifierType = "exists";
    }
  
    if (!quantifierType) {
      return this.parsePrimary(); // defer to next rule
    }
  
    this.advance(); // consume ∀ or ∃
  
    const varToken = this.current();
    if ((varToken.type !== "identifier" || !/^[a-z]$/.test(varToken.value))) {
      throw new Error(`Expected variable name after '${token.value}'`);
    }
  
    this.advance(); // consume variable name
  
    const body = this.parseFormula(); // not parseUnary — we allow full formulas here
  
    return {
      type: quantifierType,
      variable: { type: "variable", name: varToken.value },
      body: body,
    };
  }  
}
