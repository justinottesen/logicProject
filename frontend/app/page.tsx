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

  const changeProof = (newProof: Proof, changeNumber?: boolean) => {
    if (changeNumber) number(newProof);
    setProof(newProof);
  };

  async function verify() {
    let converted: Converted | null = null;
    try {
      converted = convert(proof);
    } catch (error) {
      console.log("Error converting proof:", getErrorMessage(error));
    }
    try {
      if (!converted) return;
      console.log(JSON.stringify(converted));
      const verify = await verifyProof(converted);
      console.log(verify);
    } catch (error) {
      console.log("Error verifying proof:", getErrorMessage(error));
    }
  }

  useEffect(() => {
    verify();
  }, [proof]);

  return (
    <div className="flex flex-col w-full min-h-screen">
      <section className="flex-1 border p-4 overflow-auto">
        <h2 className="text-xl font-bold mb-4">Proof</h2>
        <ProofEditor proof={proof} setProof={changeProof} />
      </section>
    </div>
  );
}
