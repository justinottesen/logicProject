import { parseFormulaInput } from "@lib/parser";
import { Statement, Step } from "@lib/logic/proof";
import { rules } from "@lib/logic/rules";

type StatementEditorProps = {
  statement: Statement;
  parents: Step[];
  onChange: (updated: Statement) => void;
  deleteStatement: () => void;
  deleteStatement: () => void;
};

export default function StatementEditor({
  statement,
  onChange,
  deleteStatement,
  deleteStatement,
}: StatementEditorProps) {
  const handleChange = (raw: string) => {
    const result = parseFormulaInput(raw);
    onChange({ ...statement, raw, result });
  };

  return (
    <div className="flex flex-row w-full h-full">
      <div className="h-full p-1 text-lg">{statement.number}</div>
      <input
        value={statement.raw}
        onChange={(e) => handleChange(e.target.value)}
        className="border px-2 py-1 rounded w-full"
        placeholder="Statement"
      />
      <select
        value={statement.rule}
        onChange={(e) => onChange({ ...statement, rule: e.target.value })}
        className="border px-2 py-1 rounded ml-2"
      >
        {rules.map((rule) => (
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

      <select
        value={statement.rule}
        onChange={(e) => onChange({ ...statement, rule: e.target.value })}
        className="border px-2 py-1 rounded ml-2"
      >
        {rules.map((rule) => (
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

      {statement.result.status === "error" && (
        <p className="text-red-600 text-sm mt-1">{statement.result.error}</p>
      )}
    </div>
  );
}
