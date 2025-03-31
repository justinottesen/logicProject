'use client';

// type SubproofEditorProps = {
//   subproof: Subproof;
//   onChange: (updated: Subproof) => void;
// };

export default function SubproofEditor(/* { subproof, onChange }: SubproofEditorProps*/) {
  // const updatePremise = (updated: Statement) => {
  //   onChange({
  //     ...subproof,
  //     premise: updated,
  //   });
  // };

  // const updateSteps = (steps: Step[]) => {
  //   onChange({
  //     ...subproof,
  //     steps,
  //   });
  // };

  return (
    <div className="border-l-2 pl-4 ml-2 mt-4">
      <div className="mt-3">
      

        <p>
          TODO: Make subproofs work. Maybe we have a shared UI object for proofs,
          special exception for the high level proof since it needs to show the conclusion?

          Idk, Murray you seemed to prefer working in UI, I will defer this choice to you.
        </p>
      </div>
    </div>
  );
}
