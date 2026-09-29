import { useState } from "react";

const projects = [
  "Glass Signal",
  "Code Orbit",
  "Data Forge",
];

export default function Voting() {
  const [selected, setSelected] = useState("");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Voting</h1>

        <p className="mt-2 text-gray-400">
          Cast your project vote.
        </p>
      </div>

      <div className="space-y-3">
        {projects.map((project) => (
          <button
            key={project}
            onClick={() => setSelected(project)}
            className={`w-full rounded-xl border p-5 text-left transition ${
              selected === project
                ? "border-blue-500 bg-blue-500/10"
                : "border-white/10 bg-[#101522] hover:bg-white/5"
            }`}
          >
            {project}
          </button>
        ))}
      </div>

      <button
        disabled={!selected}
        onClick={() => {
          // Backend_Voting_type_api
          console.log("Vote:", selected);
        }}
        className="rounded-lg bg-blue-600 px-5 py-3 disabled:opacity-40"
      >
        Submit Vote
      </button>
    </div>
  );
}