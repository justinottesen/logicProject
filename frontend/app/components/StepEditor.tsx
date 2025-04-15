import { Step } from "@lib/logic/proof";
import StatementEditor from "@components/StatementEditor";
import SubproofEditor from "./SubproofEditor";

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
      <SubproofEditor
        // subproof={step}
        // onChange={updateStep}
      />
    );
  }
}
