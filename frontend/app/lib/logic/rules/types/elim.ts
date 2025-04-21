import { Statement, Subproof } from "../../proof"


//switch Subproof to subSubproof



export type ConjectionElim = {
    name: '∧Elim';
    parents: Statement;
    symbol: '∧';
}

export type DisjunctionElim = {
    name: '∨Elim';
    parents: [Statement, ...Subproof[]];
    minLength: 2;
    symbol: '∨';
}

export type NegationElim = {
    name: '¬Elim';
    parents: Statement;
    symbol: '¬';
}
    
export type FalseElim = {
    name: '⊥Elim'
    parents: Statement;
    symbol: '⊥';
}

export type ConditionalElim = {
    name: '→Elim';
    parents: [Statement, Statement];
    symbol: '→';
}

export type BiconditionalElim = {
    name: '↔Elim';
    parents: [Statement, Statement];
    symbol: '↔';
}

export type IdentityElim = {
    name: '⊥Elim';
    parents: Statement;
    symbol: '⊥';
}