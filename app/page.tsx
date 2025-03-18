"use client";

import { useEffect, useState } from "react";
import InputBox from "./InputBox";

const defaultNum = 3;
export default function Home() {
  const [premises, setPremises] = useState<string[]>([""]);
  const [steps, setSteps] = useState<string[]>([""]);
  const [conclusion, setConclusion] = useState<string>("");

  const addPremise = () => {
    setPremises([...premises, ""]);
  };

  const removePremise = (index: number) => {
    setPremises(premises.filter((_, i) => i !== index));
  };

  const handlePremiseChange = (index: number, value: string) => {
    const updatedPremises = [...premises];
    updatedPremises[index] = value;
    setPremises(updatedPremises);
  }

  const addStep = () => {
    setSteps([...steps, ""]);
  }

  const removeStep = (index: number) => {
    setSteps(steps.filter((_, i) => i !== index));
  }

  const moveStepUp = (index: number) => {
    if (index === 0) return; // Can't move the first step up
    const updatedSteps = [...steps];
    [updatedSteps[index], updatedSteps[index - 1]] = [
      updatedSteps[index - 1],
      updatedSteps[index],
    ];
    setSteps(updatedSteps);
  };

  const moveStepDown = (index: number) => {
    if (index === steps.length - 1) return; // Can't move the last step down
    const updatedSteps = [...steps];
    [updatedSteps[index], updatedSteps[index + 1]] = [
      updatedSteps[index + 1],
      updatedSteps[index],
    ];
    setSteps(updatedSteps);
  };


  const handleStepChange = (index: number, value: string) => {
    const updatedSteps = [...steps];
    updatedSteps[index] = value;
    setSteps(updatedSteps);
  }

  return (
    <div className="flex flex-col w-full min-h-screen">
      {/* Top Section - Premises */}
      <section className="bg-gray-200 p-4 border-b border-gray-400">
        <h2 className="text-lg font-bold mb-2">Premises</h2>
        {/* <div className="mb-4">
          <button
            onClick={addPremise}
            className="mr-2 px-3 py-1 bg-blue-500 text-white rounded"
          >
            Add
          </button>
          <button
            onClick={removePremise}
            className={`px-3 py-1 rounded text-white ${
              premises.length === 0
                ? "bg-red-300 opacity-50 cursor-not-allowed"
                : "bg-red-500"
            }`}
            disabled={premises.length === 0}
          >
            Remove
          </button>
        </div> */}

        {/* Premises Input Fields */}
        <div className="space-y-2">
        {premises.map((premise, index) => (
            <div key={index} className="flex items-center space-x-2">
              <input
                type="text"
                value={premise}
                onChange={(e) => handlePremiseChange(index, e.target.value)}
                className="flex-grow p-2 border border-gray-400 rounded"
                placeholder={`Step ${index + 1}`}
              />
              <button
                onClick={() => removePremise(index)}
                className="px-3 py-1 bg-red-500 text-white rounded"
              >
                ✖
              </button>
            </div>
          ))}
        </div>
        {/* Button to add a premise at the end */}
        <button
          onClick={addPremise}
          className="mt-4 w-full px-3 py-1 bg-blue-500 text-white rounded"
        >
          + Add Premise
        </button>
      </section>

      {/* Middle Section - Proof Steps */}
      <section className="flex-grow bg-white p-4 border-b border-gray-400">
        <h2 className="text-lg font-bold">Proof Steps</h2>
        <div className="space-y-2">
          {steps.map((step, index) => (
            <div key={index} className="flex items-center space-x-2">
              <input
                type="text"
                value={step}
                onChange={(e) => handleStepChange(index, e.target.value)}
                className="flex-grow p-2 border border-gray-400 rounded"
                placeholder={`Step ${index + 1}`}
              />
              <div className="flex flex-col justify-between h-10">
                <button
                  onClick={() => moveStepUp(index)}
                  className={`w-6 h-5 bg-gray-500 text-white rounded flex items-center justify-center ${
                    index === 0 ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                  disabled={index === 0}
                >
                  ▲
                </button>
                <button
                  onClick={() => moveStepDown(index)}
                  className={`w-6 h-5 bg-gray-500 text-white rounded flex items-center justify-center ${
                    index === steps.length - 1 ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                  disabled={index === steps.length - 1}
                >
                  ▼
                </button>
              </div>
              <button
                onClick={() => removeStep(index)}
                className="px-3 py-1 bg-red-500 text-white rounded"
              >
                ✖
              </button>
            </div>
          ))}
        </div>
        {/* Button to add a step at the end */}
        <button
          onClick={addStep}
          className="mt-4 w-full px-3 py-1 bg-blue-500 text-white rounded"
        >
          + Add Step
        </button>
      </section>

      {/* Bottom Section - Proof Statement */}
      <section className="bg-gray-300 p-4">
        <h2 className="text-lg font-bold">Proof Statement</h2>
        <input
          type="text"
          value={conclusion}
          onChange={(e) => setConclusion(e.target.value)}
          className="w-full p-2 border border-gray-400 rounded"
          placeholder="Conclusion statement"
        />
      </section>
    </div>
  );
}
