// === Term-level: Constants and Variables ===

export type Constant = {
  type: "constant";
  name: string; // e.g., "alice", "a"
};

export type Variable = {
  type: "variable";
  name: string; // e.g., "x", "y"
};

// A Term is either a constant or a variable
export type Term = Constant | Variable;

// === Predicate ===

export type Predicate = {
  type: "predicate";
  name: string; // e.g., "Loves", "P"
  args: Term[]; // can be empty for 0-arity predicates
};

// === Logical Operators ===

export type Not = {
  type: "not";
  operand: Formula;
};

export type And = {
  type: "and";
  left: Formula;
  right: Formula;
};

export type Or = {
  type: "or";
  left: Formula;
  right: Formula;
};

export type Implies = {
  type: "implies";
  left: Formula;
  right: Formula;
};

export type Iff = {
  type: "iff";
  left: Formula;
  right: Formula;
};

export type Equals = {
  type: "equals";
  left: Formula;
  right: Formula;
}

export type NotEquals = {
  type: "notequals";
  left: Formula;
  right: Formula;
}

export type BinaryConnective = And | Or | Implies | Iff;

// === Quantifiers ===

export type ForAll = {
  type: "forall";
  variable: Variable;
  body: Formula;
};

export type Exists = {
  type: "exists";
  variable: Variable;
  body: Formula;
};

export type Quantifier = ForAll | Exists;

// === Formula (well-formed sentence) ===

export type Formula =
  | Predicate
  | Not
  | BinaryConnective
  | Quantifier;
