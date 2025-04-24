"use client";

import { useEffect, useState } from "react";
import ProofEditor from "./components/ProofEditor";
import { Proof } from "./lib/logic/proof";
import { number } from "./lib/logic/numberSteps";
import { convert, Converted } from "./lib/convert";
import { addRule, getRules, suggestRules, verifyProof } from "./lib/api";
import { getErrorMessage } from "./lib/parser";
import CustomRules from "./lib/CustomRules";

export default function Home() {
  const [proof, setProof] = useState<Proof>({
    type: "proof",
    premises: [],
    steps: [],
    goals: [],
  });

  const [valid, setValid] = useState<boolean>(false);
  const [suggestions, setSuggestions] = useState<string>("");
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const [addingCustomRule, setAddingCustomRule] = useState<boolean>(false);
  const [customRuleName, setCustomRuleName] = useState<string>("");

  const changeProof = (newProof: Proof, changeNumber?: boolean) => {
    if (changeNumber) number(newProof);
    setProof(newProof);
  };

  async function verify() {
    let converted: Converted | null = null;
    try {
      converted = convert(proof);
    } catch (error) {
      setValid(false);
      console.log("Error converting proof:", getErrorMessage(error));
    }
    try {
      if (!converted) return;
      console.log(JSON.stringify(converted));
      const verify = await verifyProof(converted);
      console.log(verify);
      setValid(verify.valid);
    } catch (error) {
      setValid(false);
      console.log("Error verifying proof:", getErrorMessage(error));
    }
  }

  async function setCustomRules() {
    try {
      const rules = await getRules();
      CustomRules.rules = rules.custom;
      console.log(CustomRules.rules);
    } catch (error) {
      console.log("Error getting rules:", getErrorMessage(error));
    }
  }

  async function getSuggestions() {
    let converted: Converted | null = null;
    try {
      converted = convert(proof);
    } catch (error) {
      console.log("Error converting proof:", getErrorMessage(error));
    }
    if (!converted) return;
    try {
      const suggestions = await suggestRules(converted);
      setSuggestions(suggestions);
    } catch (error) {
      console.log("Error getting suggestions:", getErrorMessage(error));
    }
  }

  useEffect(() => {
    verify();
    setCustomRules();
    getSuggestions();
  }, [proof]);

  async function addCustomRule() {
    let converted: Converted | null = null;
    try {
      converted = convert(proof);
    } catch (error) {
      console.log("Error converting proof:", getErrorMessage(error));
    }
    if (!converted) return;
    try {
      addRule(converted, customRuleName);
      setAddingCustomRule(false);
    } catch (error) {
      console.log("Error adding rule:", getErrorMessage(error));
    }
  }

  return (
    <div className="flex flex-col w-full min-h-screen">
      <section className="flex-1 border p-4 overflow-auto relative">
        <div className="grid grid-cols-4 text-center gap-4 mb-4">
          <h2 className="text-2xl font-bold py-2">Proof</h2>
          {valid ? (
            <div className="bg-green-500 text-white text-2xl font-bold px-2 py-2 rounded">
              Valid
            </div>
          ) : (
            <div className="bg-red-500 text-white text-xl font-bold px-2 py-2 rounded">
              Invalid
            </div>
          )}

          <button
            className="bg-blue-500 text-white text-xl font-bold px-2 py-1 rounded"
            onClick={(e) => setShowSuggestions(!showSuggestions)}
          >
            {showSuggestions ? "Hide" : "Show"} suggestions
          </button>

          <button
            className="bg-blue-500 text-white text-xl font-bold px-2 py-1 rounded"
            onClick={(e) => setAddingCustomRule(!addingCustomRule)}
          >
            {addingCustomRule ? "Hide" : "Add"} custom rule
          </button>
        </div>
        {showSuggestions && (
          <div className="bg-blue-500 text-white text-xl font-bold px-2 py-1 rounded">
            {suggestions ? suggestions : "No suggestions"}
          </div>
        )}
        {addingCustomRule && (
          <div className="bg-blue-500 text-xl font-bold px-2 py-1 rounded flex flex-row justify-center gap-2">
            <input
              type="text"
              placeholder="Add custom rule"
              onChange={(e) => {
                setCustomRuleName(e.target.value);
              }}
              className="flex-grow-3 text-black border border-gray-300 rounded-md px-2 py-1"
            />
            <button
              className="bg-blue-500 text-white text-xl font-bold px-2 py-1 rounded flex-grow-2"
              onClick={() => {
                addCustomRule();
                setAddingCustomRule(false);
              }}
            >
              Add
            </button>
          </div>
        )}
        <ProofEditor proof={proof} setProof={changeProof} />
      </section>
    </div>
  );
}
