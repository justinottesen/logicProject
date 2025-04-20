import { Step } from "@lib/logic/proof";
import StatementEditor from "@components/StatementEditor";
import SubproofEditor from "./SubproofEditor";

type StepEditorProps = {
  step: Step;
  parents: Step[];
  updateStep: (updated: Step) => void;
  deleteStep: () => void;
};

export default function StepEditor({ step, parents, updateStep, deleteStep }: StepEditorProps) {
  if (step.type === "line") {
    return (
      <StatementEditor
        statement={step}
        parents={parents}
        onChange={(updated) => updateStep(updated)}
        deleteStatement={deleteStep}
      />
    );
  } else {
    return (
      <SubproofEditor
        subproof={step}
        parents={parents}
        onChange={updateStep}
        deleteSubproof={deleteStep}
        
      />
    );
  }
}
