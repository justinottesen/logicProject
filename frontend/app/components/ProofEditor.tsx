"use client";

import React, { useEffect } from "react";
import { Proof, Step } from "@lib/logic/proof";
import StepEditor from "@components/StepEditor";
import { replaceSubstitutions } from "@lib/logic/substitutions";
import { parseFormulaInput } from "@lib/parser";

type ProofEditorProps = {
  proof: Proof;
  setProof: (proof: Proof) => void;
};

export default function ProofEditor({ proof, setProof }: ProofEditorProps) {
  const updatePremise = (index: number, raw: string) => {
    const newPremises = [...proof.premises];
    newPremises[index] = {
      type: "line",
      raw,
      result: parseFormulaInput(raw),
      rule: "none",
      parents: [],
      number: proof.premises[index].number,
    };
    setProof({ ...proof, premises: newPremises });
  };

  const addPremise = () => {
    setProof({
      ...proof,
      premises: [
        ...proof.premises,
        {
          type: "line",
          raw: "",
          result: parseFormulaInput(""),
          rule: "none",
          parents: [],
          number: proof.premises.length + 1,
        },
      ],
    });
  };

  const updateStepAt = (index: number, updated: Step) => {
    const newSteps = [...proof.steps];
    newSteps[index] = updated;
    setProof({ ...proof, steps: newSteps });
  };

  const addStep = () => {
    setProof({
      ...proof,
      steps: [
        ...proof.steps,
        {
          type: "line",
          raw: "",
          result: parseFormulaInput(""),
          rule: "∧Elim",
          parents: [],
          number: proof.steps.length + 1,
        },
      ],
    });
  };

  const addSubproof = () => {
    setProof({
      ...proof,
      steps: [
        ...proof.steps,
        {
          type: "subproof",
          premise: {
            type: "line",
            raw: "",
            result: parseFormulaInput(""),
            rule: "none",
            parents: [],
            number: proof.steps.length + 1,
          },
          steps: [],
          constants: [],
          number: proof.steps.length + 1,
        },
      ],
    });
  };

  const deleteStep = (index: number) => {
    const newSteps = [...proof.steps];
    newSteps.splice(index, 1);
    setProof({ ...proof, steps: newSteps });
  };

  const deleteStep = (index: number) => {
    const newSteps = [...proof.steps];
    newSteps.splice(index, 1);
    setProof({ ...proof, steps: newSteps });
  };

  // add the substutions to the proof
  useEffect(() => {
    let changed = false;
    const oldPremises = proof.premises;
    for (const premise of oldPremises) {
      const oldRaw = premise.raw;
      premise.raw = replaceSubstitutions(premise.raw);
      if (oldRaw !== premise.raw) {
        changed = true;
      }
    }

    const oldSteps = proof.steps;
    for (const step of oldSteps) {
      if (step.type === "line") {
        const oldRaw = step.raw;
        step.raw = replaceSubstitutions(step.raw);
        if (oldRaw !== step.raw) {
          changed = true;
        }
      }
    }

    if (changed) {
      setProof({ ...proof });
    }
  }, [proof, setProof]);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h3 className="font-semibold mb-2">Premises</h3>
        <div className="flex flex-col gap-2">
          {proof.premises.map((p, i) => (
            <div className="flex flex-row w-full h-full" key={p.number}>
              <div className="h-full p-1 text-lg">{p.number}</div>

              <input
                value={p.raw}
                onChange={(e) => updatePremise(i, e.target.value)}
                className="border px-2 py-1 rounded w-full"
                placeholder={`Premise ${i + 1}`}
              />
            </div>
          ))}
          <button onClick={addPremise} className="mt-2 text-sm text-blue-600">
            + Add Premise
          </button>
        </div>
      </div>

      <div>
        <h3 className="font-semibold mb-2">Steps</h3>
        <div className="flex flex-col gap-2">
          {proof.steps.map((step, i) => (
            <StepEditor
              key={i}
              step={step}
              updateStep={(updated) => updateStepAt(i, updated)}
              deleteStep={() => deleteStep(i)}
              deleteStep={() => deleteStep(i)}
            />
          ))}
          <div className="flex gap-4 mt-2">
            <button onClick={addStep} className="mt-2 text-sm text-blue-600">
              + Add Step
            </button>
            <button
              onClick={addSubproof}
              className="mt-2 text-sm text-blue-600"
            >
              + Add Subproof
            </button>
          </div>
        </div>
      </div>

      <p>
        TODO: Add the goals & conclusion at the bottom. I put it in the proof
        type. See the other TODO that shows up when you click Add subproof.
      </p>
    </div>
  );
}
