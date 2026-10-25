import { useState } from "react";
import { Link } from "react-router-dom";
import { Send, CheckCircle2, Clock, Github, ExternalLink, Code2, Layers } from "lucide-react";

interface SubmissionState {
  title: string;
  track: string;
  summary: string;
  description: string;
  repoUrl: string;
  demoUrl: string;
  techStack: string;
}

const AVAILABLE_TRACKS = [
  "AI & Machine Learning",
  "Web3 & Decentralized Systems",
  "FinTech & Open Banking",
  "Developer Tools & Infrastructure",
  "Open Innovation",
];

export default function Submission() {
  const [formData, setFormData] = useState<SubmissionState>({
    title: "",
    track: AVAILABLE_TRACKS[0],
    summary: "",
    description: "",
    repoUrl: "",
    demoUrl: "",
    techStack: "",
  });

  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setTimeout(() => {
      setIsSubmitting(false);
      setSubmitted(true);
    }, 800);
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div>
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">
          <Layers className="w-4 h-4" /> Hackathon Project Submission
        </div>
        <h1 className="text-3xl font-bold text-white">Submit Your Project</h1>
        <p className="mt-2 text-gray-400 text-sm">
          Complete the project specification below before the submission deadline. You can edit your submission until judging commences.
        </p>
      </div>

      {submitted ? (
        <div className="rounded-2xl border border-emerald-500/30 bg-emerald-950/20 p-8 text-center space-y-4 animate-fade-in">
          <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-white">Project Successfully Submitted!</h2>
          <p className="text-gray-300 text-sm max-w-lg mx-auto">
            Your project <strong className="text-white font-semibold">{formData.title || "Demo Project"}</strong> has been registered under the <strong className="text-emerald-400 font-semibold">{formData.track}</strong> track.
          </p>
          <div className="pt-4 flex flex-wrap gap-4 justify-center">
            <button
              onClick={() => setSubmitted(false)}
              className="px-5 py-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-sm font-semibold transition"
            >
              Edit Submission
            </button>
            <Link
              to="/gallery"
              className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-sm font-semibold text-white transition"
            >
              View in Project Gallery
            </Link>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="rounded-2xl border border-white/10 bg-[#101522] p-6 sm:p-8 space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-gray-300">
                  Project Title *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="e.g. Glass Signal"
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-blue-500 transition"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-gray-300">
                  Hackathon Track *
                </label>
                <select
                  value={formData.track}
                  onChange={(e) => setFormData({ ...formData, track: e.target.value })}
                  className="w-full rounded-xl border border-white/10 bg-[#101522] px-4 py-3 text-white outline-none focus:border-blue-500 transition"
                >
                  {AVAILABLE_TRACKS.map((t) => (
                    <option key={t} value={t} className="bg-[#101522]">
                      {t}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-gray-300">
                Short Tagline / Summary *
              </label>
              <input
                type="text"
                required
                value={formData.summary}
                onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
                placeholder="A one-sentence elevator pitch of your hack..."
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-blue-500 transition"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-gray-300">
                Project Description & Architecture
              </label>
              <textarea
                rows={4}
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Explain the problem, your solution, system architecture, and how it was built..."
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-blue-500 transition resize-none"
              />
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-gray-300 flex items-center gap-1.5">
                  <Github className="w-3.5 h-3.5" /> Repository URL *
                </label>
                <input
                  type="url"
                  required
                  value={formData.repoUrl}
                  onChange={(e) => setFormData({ ...formData, repoUrl: e.target.value })}
                  placeholder="https://github.com/..."
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-blue-500 transition"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-gray-300 flex items-center gap-1.5">
                  <ExternalLink className="w-3.5 h-3.5" /> Live Demo / Pitch Video URL
                </label>
                <input
                  type="url"
                  value={formData.demoUrl}
                  onChange={(e) => setFormData({ ...formData, demoUrl: e.target.value })}
                  placeholder="https://youtu.be/... or https://..."
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-blue-500 transition"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-gray-300 flex items-center gap-1.5">
                <Code2 className="w-3.5 h-3.5" /> Tech Stack & Technologies Used
              </label>
              <input
                type="text"
                value={formData.techStack}
                onChange={(e) => setFormData({ ...formData, techStack: e.target.value })}
                placeholder="FastAPI, React, Supabase, Tailwind, TypeScript, Docker"
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-blue-500 transition"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-2 text-xs text-gray-400">
              <Clock className="w-4 h-4 text-amber-400" /> Deadline locks automatically upon judging start.
            </div>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm transition shadow-lg shadow-blue-500/20 disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
              {isSubmitting ? "Submitting..." : "Submit Project"}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
