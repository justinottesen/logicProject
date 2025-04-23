import { Formula } from "./logic/logic";
import { ParsedFormula, Proof, Step } from "./logic/proof";
import { FullNames } from "./logic/rules";



type AllRules = FullNames;

export type Converted = {
    premises: ConvertedPremise[];
    steps: ConvertedStep[];
    conclusions: ConvertedConclusion[];

}
type ConvertedPremise = {
    id: string;
    formula: ConvertedFormula;
    rule: "Assumption";
}

type ConvertedStatement = {
    id: string;
    formula: ConvertedFormula;
    rule: AllRules;
    premises: string[];
}

type ConvertedSubproof = {
    id: string;
    formula: ConvertedFormula;
    rule: "Assumption";
    premises: string[];
    steps: ConvertedStep[];
}

type ConvertedStep = ConvertedStatement | ConvertedSubproof;


type ConvertedConclusion = {
    id: string;
    formula: ConvertedFormula;
    rule: "Reiteration";
    premises: string[];
}

type ConvertedFormula = {
    type: "var",
    name: string
} | {
    type: Types,
    left: ConvertedFormula,
    right: ConvertedFormula
}

type Types = "and" | "or" | "not" | "implies" | "iff";

const emptyConvertedFormula: ConvertedFormula = {
    type: "var",
    name: ""
}

export const convert = (proof: Proof) => {
    // convert the proof to json
    const converted: Converted = {
        premises: [],
        steps: [],
        conclusions: []
    };
    let i = 0;
    for (const premise of proof.premises) {
        converted.premises.push({
            id: premise.number + "",
            formula: convertToFormula(premise.result),
            rule: "Assumption"
        });
        i++;
    }
    for (const step of proof.steps) {
        converted.steps.push(convertStep(step));
    }
    for (const conclusion of proof.goals) {
        converted.conclusions.push({
            id: `conclusion${i}`,
            formula: convertToFormula(conclusion.result),
            rule: "Reiteration",
            premises: [conclusion.parent + ""]
        });
        i++;
    }
    number(converted);
    return JSON.stringify(converted, null, 2);
}





const convertToFormula = (formula: ParsedFormula): ConvertedFormula => {
    if (formula.status !== "ok") return emptyConvertedFormula;
    return convertFormula(formula.formula);

}

const convertFormula = (formula: Formula): ConvertedFormula => {

    switch (formula.type) {
        case "predicate":
            return {
                type: "var",
                name: formula.name
            }
        case "not":
            return {
                type: "not",
                left: convertFormula(formula.operand),
                right: convertFormula(formula.operand)
            }
        case "and":
            return {
                type: "and",
                left: convertFormula(formula.left),
                right: convertFormula(formula.right)
            }
        case "or":
            return {
                type: "or",
                left: convertFormula(formula.left),
                right: convertFormula(formula.right)
            }
        case "implies":
            return {
                type: "implies",
                left: convertFormula(formula.left),
                right: convertFormula(formula.right)
            }
        case "iff":
            return {
                type: "iff",
                left: convertFormula(formula.left),
                right: convertFormula(formula.right)
            }
        default:
            throw new Error("Unknown formula type");
    }
}

const convertStep = (step: Step): ConvertedStep => {

    if (step.type === "subproof") {
        const convertedStep: ConvertedSubproof = {
            id: step.number + "",
            premises: [],
            formula: emptyConvertedFormula,
            rule: "Assumption",
            steps: []
        };
        convertedStep.formula = convertToFormula(step.premise.result);
        convertedStep.rule = "Assumption";
        for (const substep of step.steps) {
            convertedStep.steps.push(convertStep(substep));
        }
        return convertedStep;

    } else if (step.type === "line") {
        const convertedStep: ConvertedStatement = {
            id: step.number + "",
            formula: emptyConvertedFormula,
            rule: step.rule as AllRules,
            premises: step.parents.map((parent) => parent + "")
        };
        convertedStep.formula = convertToFormula(step.result);
        return convertedStep;

    } else {
        throw new Error("Unknown step type");
    }
}

const number = (proof: Converted) => {
    let i = 1;
    for (const premise of proof.premises) {
        premise.id = i + "";
        i++;
    }
    for (const step of proof.steps) {
        numberSubproofs(step, i + "");
        i++;
    }
    for (const conclusion of proof.conclusions) {
        conclusion.id = i + "";
        i++;
    }
}

const numberSubproofs = (step: ConvertedStep, index: string) => {
    if (step.rule === "Assumption") {
        step.id = index;
        let i = 1;
        for (const substep of step.steps) {
            numberSubproofs(substep, index + "." + i);
            i++;
        }
        console.log("step", step.id);
    }
    else {
        step.id = index;
        console.log("step", step.id);
    }
}


