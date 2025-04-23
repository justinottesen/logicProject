import { Formula } from "./logic/logic";
import { ParsedFormula, Proof, Step } from "./logic/proof";
import { LongRules, longRuleObjects, ShortRules } from "./logic/rules";


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
    rule: LongRules;
    premises: string[];
}

type ConvertedSubproof = {
    id: string;
    type: "subproof";
    assumption: ConvertedPremise
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
} | {
    type: "not",
    value: ConvertedFormula
} | {
    type: "bottom"
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
            id: conclusion.number + "",
            formula: convertToFormula(conclusion.result),
            rule: "Reiteration",
            premises: [conclusion.parent + ""]
        });
        i++;
    }
    return converted;
}





const convertToFormula = (formula: ParsedFormula): ConvertedFormula => {
    if (formula.status !== "ok") throw new Error("Formula is not ok");
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
                value: convertFormula(formula.operand)
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
        case "bottom":
            return {
                type: "bottom"
            }
        default:
            throw new Error("Unknown formula type");
    }
}

const convertStep = (step: Step): ConvertedStep => {

    if (step.type === "subproof") {
        const convertedStep: ConvertedSubproof = {
            id: step.number + "",
            type: "subproof",
            assumption: {
                id: step.number + ".1",
                formula: convertToFormula(step.premise.result),
                rule: "Assumption"
            },
            steps: []
        };
        for (const substep of step.steps) {
            convertedStep.steps.push(convertStep(substep));
        }
        return convertedStep;

    } else if (step.type === "line") {
        const convertedStep: ConvertedStatement = {
            id: step.number + "",
            formula: emptyConvertedFormula,
            rule: convertRule(step.rule),
            premises: step.parents.map((parent) => parent + "")
        };
        convertedStep.formula = convertToFormula(step.result);
        return convertedStep;

    } else {
        throw new Error("Unknown step type");
    }
}
const convertRule = (rule: ShortRules | "none"): LongRules => {
    if (rule === "none") throw new Error("Rule is none");
    return longRuleObjects[rule] as LongRules;
}



