import { Statement, Subproof } from "../../proof"

export type ConjectionIntro = {
    name: '∧Intro';
    parents: Statement[];
    symbol: '∧';
    minLength: 2;
}

export type DisjunctionIntro = {
    name: '∨Intro';
    parents: Statement[];
    symbol: '∨';
    minLength: 2;
}

export type NegationIntro = {
    name: '¬Intro';
    parents: Subproof;
    symbol: '¬';
} 

export type FalseIntro = {
    name: '⊥Intro';
    parents: [Statement, Statement];
    symbol: '⊥';
}

export type ConditionalIntro = {
    name: '→Intro';
    parents: Subproof;
    symbol: '→';
}

export type BiconditionalIntro = {
    name: '↔Intro';
    parents: [Subproof, Subproof];
    symbol: '↔';
}

export type IdentityIntro = {
    name: '⊥Intro';
    symbol: '⊥';
}
