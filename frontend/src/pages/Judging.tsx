import { useState } from "react";
import { Award, CheckCircle, ExternalLink, Github, Scale, Star, ThumbsUp } from "lucide-react";

interface EvaluationProject {
  id: string;
  title: string;
  track: string;
  summary: string;
  repoUrl: string;
  scores: {
    innovation: number;
    technical: number;
    impact: number;
    uiUx: number;
  };
  notes: string;
  submitted: boolean;
}

const INITIAL_ASSIGNMENTS: EvaluationProject[] = [
  {
    id: "sub-1",
    title: "Glass Signal",
    track: "Web & Microservices",
    summary: "Real-time hackathon management platform and microservice workflow orchestrator.",
    repoUrl: "https://github.com/Alphaparticle2000/DOGFOOD-",
    scores: { innovation: 9, technical: 9, impact: 8, uiUx: 9 },
    notes: "Solid end-to-end implementation with clean API architecture and Supabase auth.",
    submitted: false,
  },
  {
    id: "sub-2",
    title: "Code Orbit",
    track: "AI & Machine Learning",
    summary: "Autonomous code review and developer collaboration agent with contextual AST parsing.",
    repoUrl: "https://github.com/",
    scores: { innovation: 8, technical: 9, impact: 9, uiUx: 8 },
    notes: "High potential for real developer productivity gains.",
    submitted: false,
  },
  {
    id: "sub-3",
    title: "Data Forge",
    track: "Developer Tools & Infrastructure",
    summary: "High-throughput mock database and automated dataset generation harness.",
    repoUrl: "https://github.com/",
    scores: { innovation: 7, technical: 8, impact: 8, uiUx: 7 },
    notes: "Great developer utility with impressive benchmark throughput.",
    submitted: false,
  },
];

export default function Judging() {
  const [projects, setProjects] = useState<EvaluationProject[]>(INITIAL_ASSIGNMENTS);
  const [selectedId, setSelectedId] = useState<string>(INITIAL_ASSIGNMENTS[0].id);

  const activeProject = projects.find((p) => p.id === selectedId) || projects[0];

  const updateScore = (field: keyof EvaluationProject["scores"], value: number) => {
    setProjects((prev) =>
      prev.map((p) =>
        p.id === activeProject.id
          ? { ...p, scores: { ...p.scores, [field]: value } }
          : p
      )
    );
  };

  const updateNotes = (notes: string) => {
    setProjects((prev) =>
      prev.map((p) => (p.id === activeProject.id ? { ...p, notes } : p))
    );
  };

  const handleScoreSubmit = (id: string) => {
    setProjects((prev) =>
      prev.map((p) => (p.id === id ? { ...p, submitted: true } : p))
    );
  };

  const totalScore = (scores: EvaluationProject["scores"]) =>
    scores.innovation + scores.technical + scores.impact + scores.uiUx;

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div>
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">
          <Scale className="w-4 h-4" /> Judging Portal & Rubric Evaluation
        </div>
        <h1 className="text-3xl font-bold text-white">Judge Assigned Submissions</h1>
        <p className="mt-2 text-gray-400 text-sm">
          Evaluate your assigned submissions across 4 normalized rubric dimensions (each scale 1-10). Submitted scorecards are cryptographically signed.
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Submissions List */}
        <div className="space-y-3">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-gray-400 px-1">
            Assigned Projects ({projects.length})
          </h2>
          {projects.map((project) => {
            const isSelected = project.id === activeProject.id;
            return (
              <div
                key={project.id}
                onClick={() => setSelectedId(project.id)}
                className={`p-4 rounded-xl border cursor-pointer transition ${
                  isSelected
                    ? "border-blue-500 bg-blue-500/10"
                    : "border-white/10 bg-[#101522] hover:bg-white/5"
                }`}
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-white text-sm">{project.title}</h3>
                  {project.submitted ? (
                    <span className="flex items-center gap-1 text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                      <CheckCircle className="w-3 h-3" /> Scored
                    </span>
                  ) : (
                    <span className="text-[11px] text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">
                      Pending
                    </span>
                  )}
                </div>
                <div className="text-xs text-blue-400 mt-1">{project.track}</div>
                <div className="mt-2 text-xs text-gray-400 line-clamp-1">{project.summary}</div>
                <div className="mt-3 flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-white/5">
                  <span>Score: {totalScore(project.scores)} / 40</span>
                  <span className="font-mono">{Math.round((totalScore(project.scores) / 40) * 100)}%</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Active Rubric Scoring Panel */}
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-white/10 bg-[#101522] p-6 sm:p-8 space-y-6">
            <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-white/10">
              <div>
                <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider">
                  {activeProject.track}
                </span>
                <h2 className="text-2xl font-bold text-white mt-1">{activeProject.title}</h2>
                <p className="text-gray-300 text-sm mt-2">{activeProject.summary}</p>
              </div>
              <a
                href={activeProject.repoUrl}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 text-xs font-medium text-gray-200 transition"
              >
                <Github className="w-4 h-4" /> Repository <ExternalLink className="w-3 h-3" />
              </a>
            </div>

            {/* Rubric Criteria Sliders */}
            <div className="space-y-5">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-gray-300 flex items-center gap-2">
                <Award className="w-4 h-4 text-amber-400" /> Scoring Rubric
              </h3>

              <div className="space-y-4">
                {[
                  { key: "innovation", label: "Innovation & Creativity", desc: "Originality and novelty of the core concept" },
                  { key: "technical", label: "Technical Execution", desc: "Architecture, code quality, stability and test coverage" },
                  { key: "impact", label: "Real-world Impact", desc: "Practical utility, market viability, and user value" },
                  { key: "uiUx", label: "UI / UX & Polish", desc: "Design elegance, user experience, and visual clarity" },
                ].map(({ key, label, desc }) => {
                  const scoreVal = activeProject.scores[key as keyof EvaluationProject["scores"]];
                  return (
                    <div key={key} className="p-4 rounded-xl border border-white/5 bg-white/[0.02] space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="font-semibold text-white">{label}</span>
                        <span className="font-mono text-sm font-bold text-blue-400 bg-blue-500/10 px-2.5 py-0.5 rounded-md border border-blue-500/20">
                          {scoreVal} / 10
                        </span>
                      </div>
                      <p className="text-xs text-gray-400">{desc}</p>
                      <input
                        type="range"
                        min="1"
                        max="10"
                        value={scoreVal}
                        onChange={(e) =>
                          updateScore(key as keyof EvaluationProject["scores"], Number(e.target.value))
                        }
                        className="w-full accent-blue-500 cursor-pointer"
                      />
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Judge Feedback Notes */}
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-gray-300">
                Judge Evaluation & Qualitative Feedback
              </label>
              <textarea
                rows={3}
                value={activeProject.notes}
                onChange={(e) => updateNotes(e.target.value)}
                placeholder="Add constructive feedback for the team..."
                className="w-full rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-white placeholder-gray-500 outline-none focus:border-blue-500 transition resize-none"
              />
            </div>

            {/* Total and Submit */}
            <div className="flex items-center justify-between pt-4 border-t border-white/10">
              <div>
                <span className="text-xs text-gray-400">Total Scorecard Value:</span>
                <div className="text-2xl font-bold text-white">
                  {totalScore(activeProject.scores)} <span className="text-sm font-normal text-gray-400">/ 40 points</span>
                </div>
              </div>

              <button
                type="button"
                onClick={() => handleScoreSubmit(activeProject.id)}
                className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-sm transition ${
                  activeProject.submitted
                    ? "bg-emerald-600/80 text-white cursor-default"
                    : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20"
                }`}
              >
                <ThumbsUp className="w-4 h-4" />
                {activeProject.submitted ? "Scorecard Recorded" : "Submit Scorecard"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
