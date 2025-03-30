import { Step } from "@lib/logic/proof";
import StatementEditor from "@components/StatementEditor";
import ProofEditor from "@components/ProofEditor";

type StepEditorProps = {
  step: Step;
  updateStep: (updated: Step) => void;
};

export default function StepEditor({ step, updateStep }: StepEditorProps) {
  if (step.type === "line") {
    return (
      <StatementEditor
        statement={step}
        onChange={(updated) => updateStep(updated)}
      />
    );
  } else {
    return (
      <div className="border-l-2 pl-4 ml-2">
        <ProofEditor
          proof={step}
          setProof={(updated) => updateStep(updated)}
        />
      </div>
    );
  }
}
