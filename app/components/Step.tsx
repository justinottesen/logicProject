import React, { useState } from "react";
import Statement from "./Statement";
import Proof from "./Proof";

interface StepProps {
  type: "statement" | "subproof";
  onDelete: () => void;
  onMoveUp: () => void;
  onMoveDown: () => void;
  isFirst: boolean;
  isLast: boolean;
}

export default function Step({ type, onDelete, onMoveUp, onMoveDown, isFirst, isLast }: StepProps) {
  const [statement, setStatement] = useState("");

  return (
    <div className="flex items-start space-x-2">
      {/* If it's a statement, show input box */}
      {type === "statement" ? (
        <Statement value={statement} onChange={setStatement} onDelete={onDelete} placeholder="Enter statement" />
      ) : (
        <div className="border-l-4 border-purple-500 p-2 relative w-full">
          <h4 className="text-md font-semibold flex items-start justify-between">
            Subproof
          </h4>
          <Proof />
        </div>
      )}

      {/* Buttons Wrapper - Aligns to Top */}
      <div className="flex flex-col justify-between h-10">
        {/* Move Up Button */}
        <button
          onClick={onMoveUp}
          className={`w-6 h-5 bg-gray-500 text-white rounded flex items-center justify-center ${
            isFirst ? "opacity-50 cursor-not-allowed" : "hover:bg-gray-600"
          }`}
          disabled={isFirst}
        >
          ▲
        </button>

        {/* Move Down Button */}
        <button
          onClick={onMoveDown}
          className={`w-6 h-5 bg-gray-500 text-white rounded flex items-center justify-center ${
            isLast ? "opacity-50 cursor-not-allowed" : "hover:bg-gray-600"
          }`}
          disabled={isLast}
        >
          ▼
        </button>
      </div>

      {/* Delete Button */}
      <button
        onClick={onDelete}
        className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
      >
        ✖
      </button>
    </div>
  );
}
