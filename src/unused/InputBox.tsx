"use client";

const rules = ["premise", "other", "goal"]

export default function InputBox({
  text,
  setText,
  rule,
  setRule,
}: Readonly<{
  text: string;
  setText: (text: string) => void;
  rule: string;
  setRule: (rule: string) => void;
}>) {
  return (
    <div className="flex w-full h-full">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="h-full flex-grow border border-gray-300 rounded-l-md px-2 py-1"
      />
      <select
        value={rule}
        onChange={(e) => setRule(e.target.value)}
        className="h-full border border-gray-300 rounded-r-md px-2 py-1"
      >
        {rules.map((rule) => (
          <option key={rule}>{rule}</option>
        ))}
      </select>
    </div>
  );
}
