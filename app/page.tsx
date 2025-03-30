"use client";

import { useEffect, useState } from "react";
import Proof from "./components/Proof";

export default function Home() {
  const [conclusion, setConclusion] = useState<string>("");

  return (
    <div className="flex flex-col w-full min-h-screen">
      <section className="flex-1 border p-4 overflow-auto">
        <h2 className="text-xl font-bold mb-4">Proof</h2>
        <Proof/>
      </section>

      {/* Bottom Section - Proof Statement */}
      <section className="bg-gray-300 p-4">
        <h2 className="text-lg font-bold">Conclusion Statement</h2>
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
