"use client";
import { Statement, Subproof, Step } from "@/lib/logic/proof";
import { parseFormulaInput } from "@/lib/parser";
import { useState } from "react";
import StepEditor from "./StepEditor";
import StatementEditor from "./StatementEditor";
import { text } from "stream/consumers";

type SubproofEditorProps = {
  subproof: Subproof;
  onChange: (updated: Subproof) => void;
  deleteSubproof: () => void;
};

export default function SubproofEditor({
  subproof,
  onChange,
  deleteSubproof,
  
}: SubproofEditorProps) {
  const updateStepAt = (index: number, updated: Step) => {
    const newSteps = [...subproof.steps];
    newSteps[index] = updated;
    onChange({ ...subproof, steps: newSteps });
  };

  const addStep = () => {
    onChange({
      ...subproof,
      steps: [
        ...subproof.steps,
        {
          type: "line",
          raw: "",
          result: parseFormulaInput(""),
          rule: "∧Elim",
          parents: [],
          number: subproof.steps.length + 1,
        },
      ],
    });
  };

  const addSubproof = () => {
    onChange({
      ...subproof,
      steps: [
        ...subproof.steps,
        {
          type: "subproof",
          premise: {
            type: "line",
            raw: "",
            result: parseFormulaInput(""),
            rule: "none",
            parents: [],
            number: subproof.steps.length + 1,
          },
          steps: [],
          constants: [],
          number: subproof.steps.length + 1,
        },
      ],
    });
  };

  const onChangePremise = (text: string) => {
    const updatedPremise = {
      ...subproof.premise,
      raw: text,
      result: parseFormulaInput(text),
    };
    onChange({ ...subproof, premise: updatedPremise });
  };

  const deleteStep = (index: number) => {
    const newSteps = [...subproof.steps];
    newSteps.splice(index, 1);
    onChange({ ...subproof, steps: newSteps });
  };
  return (
    <div className="flex flex-col gap-2 pl-4 sub relative">
      <div className="flex flex-row w-full h-full mb-2">
        <div className="h-full p-1 text-lg">{subproof.number}</div>
        <input
          type="text"
          value={subproof.premise.raw}
          onChange={(e) => onChangePremise(e.target.value)}
          className="px-2 py-1 rounded w-full sub-premise"
          placeholder="Subproof Premise"
        />
        <button
          className="ml-2 border px-2 py-1 rounded bg-base hover-bg-dark-base text-white"
          onClick={deleteSubproof}
        >
          Delete
        </button>
      </div>
      {subproof.steps.map((step, i) => (
        <StepEditor
          key={"step-" + i}
          step={step}
          updateStep={(updated) => updateStepAt(i, updated)}
          deleteStep={() => deleteStep(i)}
        />
      ))}
      <div className="flex gap-4">
        <button onClick={addStep} className="mt-2 text-sm text-blue-600">
          + Add Step
        </button>
        <button onClick={addSubproof} className="mt-2 text-sm text-blue-600">
          + Add Subproof
        </button>
      </div>
    </div>
  );
}
