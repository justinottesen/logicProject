import { Proof, Subproof } from "./proof";


export const number = (proof: Proof) => {
    let i = 1;
    const numberIndex = (subproof: Subproof, index: number) => {
        for (const step of subproof.steps) {
            step.number = i++;
            if (step.type === "subproof") {
                numberIndex(step, index)
            }
        }
    }
    for (const premise of proof.premises) {
        premise.number = i++;
    }
    for (const step of proof.steps) {
        step.number = i++;
        if (step.type === "subproof") {
            numberIndex(step, i)
        }
    }
    for (const goal of proof.goals) {
        goal.number = i++;
    }
}