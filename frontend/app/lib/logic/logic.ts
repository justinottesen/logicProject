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
  value: '¬'; 
};

export type And = {
  type: "and";
  left: Formula;
  right: Formula;
  value: '∧';
};

export type Or = {
  type: "or";
  left: Formula;
  right: Formula;
  value: '∨';
};

export type Implies = {
  type: "implies";
  left: Formula;
  right: Formula;
  value: '→';
};

export type Iff = {
  type: "iff";
  left: Formula;
  right: Formula;
  value: '↔';
};

export type Equals = {
  type: "equals";
  left: Formula;
  right: Formula;
  value: '=';
}

export type NotEquals = {
  type: "notequals";
  left: Formula;
  right: Formula;
  value: '≠';
}

export type BinaryConnective = And | Or | Implies | Iff;

export type Bottom = {
  type: "bottom";
  value: '⊥';
};

export type Formula =
  | Predicate
  | Not
  | BinaryConnective
  | Bottom;