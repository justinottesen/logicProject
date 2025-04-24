import { parseFormulaInput } from "@lib/parser";
import { Statement, Step } from "@lib/logic/proof";
import { rules, ShortRules } from "@lib/logic/rules";
import { replaceSubstitutions } from "@/lib/logic/substitutions";
import { useState } from "react";
import CustomRules from "@/lib/CustomRules";

type StatementEditorProps = {
  statement: Statement;
  onChange: (updated: Statement) => void;
  deleteStatement: () => void;
};

export default function StatementEditor({
  statement,
  onChange,
  deleteStatement,
}: StatementEditorProps) {
  const [selected, setSelected] = useState<boolean>(false);
  const handleChange = (raw: string) => {
    raw = replaceSubstitutions(raw);
    const result = parseFormulaInput(raw);
    onChange({ ...statement, raw, result });
  };

  const changeParents = (parentsRaw: string) => {
    const newStatement = {
      ...statement,
      parentsRaw: parentsRaw,
      parents: parentsRaw.split(","),
    };
    onChange(newStatement);
  };

  const changeRule = (rule: string) => {
    const newStatement = { ...statement, rule: rule };
    onChange(newStatement);
  };

  return (
    <div className="flex flex-row w-full h-full align-middle gap-2 relative">
      <div className="p-1 text-lg text-center grid items-center justify-center">
        <p>{statement.number}</p>
      </div>
      <input
        value={statement.raw}
        onChange={(e) => handleChange(e.target.value)}
        onFocus={() => setSelected(true)}
        onBlur={() => setSelected(false)}
        className="border px-2 py-1 rounded flex-grow-3"
        placeholder="Statement"
      />
      <input
        type="text"
        value={statement.parentsRaw}
        onChange={(e) => changeParents(e.target.value)}
        className="border px-2 py-1 rounded flex-grow-1"
        placeholder="Parents (1,2,3)"
      />

      <select
        value={statement.rule}
        onChange={(e) => changeRule(e.target.value)}
        className="border px-2 py-1 rounded ml-2"
      >
        {rules.map((rule) => (
          <option key={"statment-rule-" + rule} value={rule}>
            {rule}
          </option>
        ))}
        {CustomRules.rules.map((rule) => (
          <option key={"statment-rule-" + rule} value={rule}>
            {rule}
          </option>
        ))}
      </select>
      <button
        className="ml-2 border px-2 py-1 rounded bg-base hover-bg-dark-base text-white"
        onClick={deleteStatement}
      >
        Delete
      </button>

      {(statement.result.status === "error" ||
        (statement.result.status === "incomplete" && !selected)) && (
        <div className="w-28 bg-red-100 border border-red-300 rounded flex items-center justify-center text-center">
          <p className="text-red-600 text-xs">{statement.result.error}</p>
        </div>
      )}
    </div>
  );
}
