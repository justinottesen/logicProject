"use client";

import { useState } from "react";
import ProofEditor from "./components/ProofEditor";
import { Proof } from "./lib/logic/proof";
import { number } from "./lib/logic/numberSteps";

export default function Home() {
  const [proof, setProof] = useState<Proof>({
    type: "proof",
    premises: [],
    steps: [],
    goals: [],
  });

  const changeProof = (newProof: Proof, changeNumber?: boolean) => {
    if(changeNumber) number(newProof);
    setProof(newProof);
  };



  return (
    <div className="flex flex-col w-full min-h-screen">
      <section className="flex-1 border p-4 overflow-auto">
        <h2 className="text-xl font-bold mb-4">Proof</h2>
        <ProofEditor proof={proof} setProof={changeProof} />
      </section>
    </div>
  );
}
