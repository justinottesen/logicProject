import { ConjectionElim, DisjunctionElim, NegationElim, FalseElim, ConditionalElim, BiconditionalElim, IdentityElim, } from './elim';
import { ConjectionIntro, DisjunctionIntro, NegationIntro, FalseIntro, ConditionalIntro, BiconditionalIntro } from './intro';

export type Rules = ConjectionElim | DisjunctionElim | NegationElim | FalseElim | ConditionalElim | BiconditionalElim | IdentityElim | ConjectionIntro| DisjunctionIntro | NegationIntro | FalseIntro | ConditionalIntro | BiconditionalIntro;
