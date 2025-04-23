"use client";

import React, { useEffect } from "react";
import { Proof, Step, ProofStep, Premise, Goal } from "@lib/logic/proof";
import StepEditor from "@components/StepEditor";
import { replaceSubstitutions } from "@lib/logic/substitutions";
import { parseFormulaInput } from "@lib/parser";

type ProofEditorProps = {
  proof: Proof;
  setProof: (proof: Proof, changeNumber?: boolean) => void;
};

export default function ProofEditor({ proof, setProof }: ProofEditorProps) {
  const updatePremiseRaw = (index: number, raw: string) => {
    const newPremises = [...proof.premises];
    newPremises[index] = {
      type: "premise",
      raw: replaceSubstitutions(raw),
      result: parseFormulaInput(replaceSubstitutions(raw)),
      rule: "none",
      number: index + 1,
    };
    setProof({ ...proof, premises: newPremises });
  };

  const updateGoalRaw = (index: number, raw: string) => {
    const newGoals = [...proof.goals];
    newGoals[index] = {
      type: "goal",
      raw: replaceSubstitutions(raw),
      result: parseFormulaInput(replaceSubstitutions(raw)),
      rule: "none",
      number: index + 1,
      parent: newGoals[index].parent,
    };
    setProof({ ...proof, goals: newGoals });
  };

  const updateGoalParent = (index: number, parent: string) => {
    const newGoals = [...proof.goals];
    newGoals[index] = {
      type: "goal",
      raw: newGoals[index].raw,
      result: newGoals[index].result,
      rule: "none",
      number: index + 1,
      parent: parseInt(parent),
    };
    setProof({ ...proof, goals: newGoals });
  };

  const addPremise = () => {
    const p = {
      type: "premise",
      raw: "",
      result: parseFormulaInput(""),
      rule: "none",
      number: 0,
    } as Premise;
    setProof(
      {
        ...proof,
        premises: [...proof.premises, p],
      },
      true
    );
  };

  const addGoal = () => {
    const g = {
      type: "goal",
      raw: "",
      result: parseFormulaInput(""),
      rule: "none",
      number: 0,
      parent: 0,
    } as Goal;
    setProof(
      {
        ...proof,
        goals: [...proof.goals, g],
      },
      true
    );
  };

  const deletePremise = (index: number) => {
    const newPremises = [...proof.premises];
    newPremises.splice(index, 1);
    setProof({ ...proof, premises: newPremises }, true);
  };

  const deleteGoal = (index: number) => {
    const newGoals = [...proof.goals];
    newGoals.splice(index, 1);
    setProof({ ...proof, goals: newGoals }, true);
  };

  const updateStepAt = (
    index: number,
    updated: Step,
    changeNumber?: boolean
  ) => {
    const newSteps = [...proof.steps];
    newSteps[index] = updated;
    setProof({ ...proof, steps: newSteps }, changeNumber);
  };

  const addStep = () => {
    setProof(
      {
        ...proof,
        steps: [
          ...proof.steps,
          {
            type: "line",
            raw: "",
            result: parseFormulaInput(""),
            rule: "∧Elim",
            parents: [],
            parentsRaw: "",
            number: 0,
          },
        ],
      },
      true
    );
  };

  const addSubproof = () => {
    setProof(
      {
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
              parentsRaw: "",
              number: 0,
            },
            steps: [],
            raw: "",
            constantsRaw: "",
            number: 0,
          },
        ],
      },
      true
    );
  };

  const deleteStep = (index: number) => {
    const newSteps = [...proof.steps];
    newSteps.splice(index, 1);
    setProof({ ...proof, steps: newSteps }, true);
  };

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
                onChange={(e) => updatePremiseRaw(i, e.target.value)}
                className="border px-2 py-1 rounded w-full"
                placeholder={`Premise ${i + 1}`}
              />
              <button
                onClick={() => deletePremise(i)}
                className="ml-2 border px-2 py-1 rounded bg-base hover-bg-dark-base text-white"
              >
                Delete
              </button>
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
              updateStep={(updated, changeNumber) =>
                updateStepAt(i, updated, changeNumber)
              }
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
      <div>
        <h3 className="font-semibold mb-2">Goals</h3>
        <div className="flex flex-col gap-2">
          {proof.goals.map((g, i) => (
            <div className="flex flex-row w-full h-full" key={g.number}>
              <div className="h-full p-1 text-lg">{g.number}</div>

              <input
                value={g.raw}
                onChange={(e) => updateGoalRaw(i, e.target.value)}
                className="border px-2 py-1 flex-grow-3 rounded w-full"
                placeholder={`Goal ${i + 1}`}
              />
              <input
                type="text"
                value={(isNaN(g.parent) || g.parent <= 0) ? "" : g.parent}
                onChange={(e) => updateGoalParent(i, e.target.value)}
                className="border px-2 py-1 flex-grow-1 rounded w-full"
                placeholder={`Parent ${i + 1}`}
              />
              <button
                onClick={() => deleteGoal(i)}
                className="ml-2 border px-2 py-1 rounded bg-base hover-bg-dark-base text-white"
              >
                Delete
              </button>
            </div>
          ))}
          <button onClick={addGoal} className="mt-2 text-sm text-blue-600">
            + Add Goal
          </button>
        </div>
      </div>
    </div>
  );
}
