import { Statement } from "../proof";

// Temporary parser
const parseFormulaInput = (raw: string) => ({
  status: "error" as const,
  error: "Parser Not Yet Implemented",
});

type StatementEditorProps = {
  statement: Statement;
  onChange: (updated: Statement) => void;
};

export default function StatementEditor({
  statement,
  onChange,
}: StatementEditorProps) {
  const handleChange = (raw: string) => {
    const result = parseFormulaInput(raw);
    onChange({ ...statement, raw, result });
  };

  return (
    <div>
      <input
        value={statement.raw}
        onChange={(e) => handleChange(e.target.value)}
        className="border px-2 py-1 rounded w-full"
        placeholder="Statement"
      />
      {statement.result.status === "error" && (
        <p className="text-red-600 text-sm mt-1">{statement.result.error}</p>
      )}
    </div>
  );
}
