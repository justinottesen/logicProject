import { Step, Proof } from "../../proof"


//switch proof to subproof



export type ConjectionElim = {
    name: '∧Elim';
    parents: Step;
    symbol: '∧';
}

export type DisjunctionElim = {
    name: '∨Elim';
    parents: [Step, ...Proof[]];
    minLength: 2;
    symbol: '∨';
}

export type NegationElim = {
    name: '¬Elim';
    parents: Step;
    symbol: '¬';
}
    
export type FalseElim = {
    name: '⊥Elim'
    parents: Step;
    symbol: '⊥';
}

export type ConditionalElim = {
    name: '→Elim';
    parents: [Step, Step];
    symbol: '→';
}

export type BiconditionalElim = {
    name: '↔Elim';
    parents: [Step, Step];
    symbol: '↔';
}

export type IdentityElim = {
    name: '⊥Elim';
    parents: Step;
    symbol: '⊥';
}

export type UniversalElim = {
    name: '∀Elim';
    parents: Step;
    symbol: '∀';
}

export type ExistentialElim = {
    name: '∃Elim';
    parents: [Step, Proof];
    symbol: '∃';
}

