import React, { useState } from "react";
import Step from "./Step";

export default function Proof() {
  const [premises, setPremises] = useState<Array<{ type: "statement"; id: number }>>([]);
  const [steps, setSteps] = useState<Array<{ type: "statement" | "subproof"; id: number }>>([]);
  const [nextId, setNextId] = useState(1);

  const addPremise = () => {
    setPremises([...premises, { type: "statement", id: nextId }]);
    setNextId(nextId + 1);
  };

  const removePremise = (id: number) => {
    setPremises(premises.filter((premise) => premise.id !== id));
  };

  const movePremise = (index: number, direction: "up" | "down") => {
    if ((index === 0 && direction === "up") || (index === premises.length - 1 && direction === "down")) {
      return; // Do nothing if already at the top/bottom
    }

    const newPremises = [...premises];
    const swapIndex = direction === "up" ? index - 1 : index + 1;
    [newPremises[index], newPremises[swapIndex]] = [newPremises[swapIndex], newPremises[index]];
    setPremises(newPremises);
  };

  const addStep = (type: "statement" | "subproof") => {
    setSteps([...steps, { type, id: nextId }]);
    setNextId(nextId + 1);
  };

  const removeStep = (id: number) => {
    setSteps(steps.filter((step) => step.id !== id));
  };

  const moveStep = (index: number, direction: "up" | "down") => {
    if ((index === 0 && direction === "up") || (index === steps.length - 1 && direction === "down")) {
      return; // Do nothing if already at the top/bottom
    }

    const newSteps = [...steps];
    const swapIndex = direction === "up" ? index - 1 : index + 1;
    [newSteps[index], newSteps[swapIndex]] = [newSteps[swapIndex], newSteps[index]];
    setSteps(newSteps);
  };

  return (
    <div className="border p-4 space-y-4">
      {/* Premises Section */}
      <div className="space-y-2">
        {premises.map((premise, index) => (
          <Step
            key={premise.id}
            type={premise.type}
            onDelete={() => removePremise(premise.id)}
            onMoveUp={() => movePremise(index, "up")}
            onMoveDown={() => movePremise(index, "down")}
            isFirst={index === 0}
            isLast={index === premises.length - 1}
          />
        ))}
        <button onClick={addPremise} className="bg-blue-500 text-white px-4 py-2 rounded">
          + Add Premise
        </button>
      </div>

      {/* Purple Divider to Mark Steps Section */}
      <div className="border-t-4 border-purple-500 mt-4"></div>

      {/* Steps Section */}
      <div className="space-y-2">
        {steps.map((step, index) => (
          <Step
            key={step.id}
            type={step.type}
            onDelete={() => removeStep(step.id)}
            onMoveUp={() => moveStep(index, "up")}
            onMoveDown={() => moveStep(index, "down")}
            isFirst={index === 0}
            isLast={index === steps.length - 1}
          />
        ))}
      </div>

      {/* Add Step Buttons */}
      <div className="space-x-2">
        <button onClick={() => addStep("statement")} className="bg-green-500 text-white px-4 py-2 rounded">
          + Add Statement
        </button>
        <button onClick={() => addStep("subproof")} className="bg-purple-500 text-white px-4 py-2 rounded">
          + Add Subproof
        </button>
      </div>
    </div>
  );
}
