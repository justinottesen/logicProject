import { Proof, Subproof } from "./proof";


export const number = (proof: Proof) => {
    console.log("proof");
    let i = 1;

    for (const premise of proof.premises) {
        premise.number = i + "";
        i++;
    }
    for (const step of proof.steps) {
        step.number = i + "";
        if (step.type === "subproof") {
            numberIndex(step, i + "")
        }
        i++;
    }
    for (const goal of proof.goals) {
        goal.number = i + "";
        i++;
    }
}

const numberIndex = (subproof: Subproof, index: string) => {
    let i = 2;
    for (const step of subproof.steps) {
        step.number = index + "." + i;

        if (step.type === "subproof") {
            numberIndex(step, index + "." + i)
        }
        i++;
    }
}