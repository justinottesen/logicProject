"use client";

import { useEffect, useState } from "react";
import ProofEditor from "./components/ProofEditor";
import { Proof } from "./lib/logic/proof";
import { number } from "./lib/logic/numberSteps";
import { convert, Converted } from "./lib/convert";
import { verifyProof } from "./lib/api";
import { getErrorMessage } from "./lib/parser";

export default function Home() {
  const [proof, setProof] = useState<Proof>({
    type: "proof",
    premises: [],
    steps: [],
    goals: [],
  });

  const [valid, setValid] = useState<boolean>(false);

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

  useEffect(() => {
    verify();
  }, [proof]);

  return (
    <div className="flex flex-col w-full min-h-screen">
      <section className="flex-1 border p-4 overflow-auto">
        <div className="grid grid-cols-2">
          <h2 className="text-xl font-bold mb-4">Proof</h2>
          {valid && (
            <div className="bg-green-500 text-white text-xl font-bold mr-2 px-2 py-1 rounded">
              Valid
            </div>
          )}
          {!valid && (
            <div className="bg-red-500 text-white text-xl font-bold mr-2 px-2 py-1 rounded">
              Invalid
            </div>
          )}
        </div>
        <ProofEditor proof={proof} setProof={changeProof} />
      </section>
    </div>
  );
}
