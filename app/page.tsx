"use client";

import { useState } from "react";
import ProofEditor from "./components/ProofEditor";
import { Proof, Statement } from "./proof";

export default function Home() {
  const [proof, setProof] = useState<Proof>({
    type: "proof",
    premises: [],
    steps: []
  });
  const [conclusion, setConclusion] = useState<Statement>({
    type: "line",
    raw: "",
    result: { status: "error", error: "Parser Not Yet Implemented" }
  });

  return (
    <div className="flex flex-col w-full min-h-screen">
      <section className="flex-1 border p-4 overflow-auto">
        <h2 className="text-xl font-bold mb-4">Proof</h2>
        <ProofEditor proof={proof} setProof={setProof} />
      </section>

      {/* Bottom Section - Proof Statement */}
      <section className="bg-gray-300 p-4">
        <h2 className="text-lg font-bold">Conclusion Statement</h2>
        <input
          type="text"
          value={conclusion.raw}
          onChange={(e) => setConclusion({
            type: "line",
            raw: e.target.value,
            result: { status: "error", error: "Parser Not Yet Implemented" }
          })}
          className="w-full p-2 border border-gray-400 rounded"
          placeholder="Conclusion statement"
        />
      </section>
    </div>
  );
}
