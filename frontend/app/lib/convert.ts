import { Formula } from "./logic/logic";
import { ParsedFormula, Proof, Step } from "./logic/proof";
import { FullNames } from "./logic/rules";



type AllRules = FullNames | "Assumption";

type Converted = {
    premises: ConvertedPremise[];
    steps: ConvertedStep[];
    conclusions: ConvertedConclusion[];

}
type ConvertedPremise = {
    id: string;
    formula: ConvertedFormula;
    rule: "Assumption";
}

type ConvertedStep = {
    id: string;
    formula: ConvertedFormula;
    rule: AllRules;
    premises: string[];
}

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

const convert = (proof: Proof) => {
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
    return converted
}





    const convertToFormula = (formula: ParsedFormula): ConvertedFormula => {
        if (formula.status !== "ok") throw new Error("Formula is not valid");
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
        const convertedStep: ConvertedStep = {
            id: step.number + "",
            premises: [],
            formula: emptyConvertedFormula,
            rule: "∧ Elimination"
        };
        if (step.type === "subproof") {
            convertedStep.formula = convertToFormula(step.premise.result);
            convertedStep.rule = "Assumption";
            for (const substep of step.steps) {
                convertedStep.
            }
            
        } else if (step.type === "line") {
            
        } else {
            throw new Error("Unknown step type");
        }