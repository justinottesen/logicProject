import { Step, Proof } from "../../proof"

export type PeanoInduction = {
    name: 'Peano Induction';
    parents: [Step, Proof];
    symbol: 'P-Ind';
}

export type StrongInduction = {
    name: 'Strong Induction';
    parents: Proof;
    symbol: 'S-Ind';
}