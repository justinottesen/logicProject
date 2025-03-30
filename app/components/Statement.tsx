import React from "react";

interface StatementProps {
  value: string;
  onChange: (newValue: string) => void;
  onDelete: () => void;
  placeholder: string;
}

export default function Statement({ value, onChange, placeholder }: StatementProps) {
  return (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="border p-2 w-full"
      placeholder={placeholder || "Enter statement"}
    />
  );
}
