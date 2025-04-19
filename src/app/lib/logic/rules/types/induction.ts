import { Statement, Subproof } from "../../proof"

export type PeanoInduction = {
    name: 'Peano Induction';
    parents: [Statement, Subproof];
    symbol: 'P-Ind';
}

export type StrongInduction = {
    name: 'Strong Induction';
    parents: Subproof;
    symbol: 'S-Ind';
}