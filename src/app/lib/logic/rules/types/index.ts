import { ConjectionElim, DisjunctionElim, NegationElim, FalseElim, ConditionalElim, BiconditionalElim, IdentityElim, UniversalElim, ExistentialElim } from './elim';
import { ConjectionIntro, DisjunctionIntro, NegationIntro, FalseIntro, ConditionalIntro, BiconditionalIntro } from './intro';
import { PeanoInduction, StrongInduction } from './induction';

export type Rules = ConjectionElim | DisjunctionElim | NegationElim | FalseElim | ConditionalElim | BiconditionalElim | IdentityElim | UniversalElim | ExistentialElim | ConjectionIntro| DisjunctionIntro | NegationIntro | FalseIntro | ConditionalIntro | BiconditionalIntro| PeanoInduction| StrongInduction;
