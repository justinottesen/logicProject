'use client';

import React from "react";
import { Proof, Step } from "@lib/logic/proof";
import StepEditor from "@components/StepEditor";

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
      result: { status: "error", error: "Parser Not Yet Implemented" },
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
          result: { status: "error", error: "Parser Not Yet Implemented" },
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
          result: { status: "error", error: "Parser Not Yet Implemented" },
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
          type: "proof",
          premises: [],
          steps: [],
        },
      ],
    });
  };

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h3 className="font-semibold mb-2">Premises</h3>
        <div className="flex flex-col gap-2">
          {proof.premises.map((p, i) => (
            <input
              key={i}
              value={p.raw}
              onChange={(e) => updatePremise(i, e.target.value)}
              className="border px-2 py-1 rounded w-full"
              placeholder={`Premise ${i + 1}`}
            />
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
            />
          ))}
          <div className="flex gap-4 mt-2">
            <button onClick={addStep} className="mt-2 text-sm text-blue-600">
              + Add Step
            </button>
            <button onClick={addSubproof} className="mt-2 text-sm text-blue-600">
              + Add Subproof
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
