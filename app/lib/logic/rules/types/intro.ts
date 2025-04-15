import { Step, Proof } from "../../proof"

export type ConjectionIntro = {
    name: '∧Intro';
    parents: Step[];
    symbol: '∧';
    minLength: 2;
}

export type DisjunctionIntro = {
    name: '∨Intro';
    parents: Step[];
    symbol: '∨';
    minLength: 2;
}

export type NegationIntro = {
    name: '¬Intro';
    parents: Proof;
    symbol: '¬';
} 

export type FalseIntro = {
    name: '⊥Intro';
    parents: [Step, Step];
    symbol: '⊥';
}

export type ConditionalIntro = {
    name: '→Intro';
    parents: Proof;
    symbol: '→';
}

export type BiconditionalIntro = {
    name: '↔Intro';
    parents: [Proof, Proof];
    symbol: '↔';
}

export type IdentityIntro = {
    name: '⊥Intro';
    symbol: '⊥';
}

export type UniversalIntro = {
    name: '∀Intro';
    parents: Proof;
    symbol: '∀';
}

export type ExistentialIntro = {
    name: '∃Intro';
    parents: Step;
    symbol: '∃';
}
