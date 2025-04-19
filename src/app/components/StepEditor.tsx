import { Step } from "@lib/logic/proof";
import StatementEditor from "@components/StatementEditor";
import SubproofEditor from "./SubproofEditor";

type StepEditorProps = {
  step: Step;
  updateStep: (updated: Step) => void;
  deleteStep: () => void;
};

export default function StepEditor({ step, updateStep, deleteStep }: StepEditorProps) {
  if (step.type === "line") {
    return (
      <StatementEditor
        statement={step}
        onChange={(updated) => updateStep(updated)}
        deleteStatement={deleteStep}
      />
    );
  } else {
    return (
      <SubproofEditor
        subproof={step}
        onChange={updateStep}
        deleteSubproof={deleteStep}
      />
    );
  }
}
