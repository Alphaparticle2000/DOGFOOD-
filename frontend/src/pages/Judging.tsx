import { useMemo, useState } from "react";

interface Project {
  id: string;
  title: string;
  summary: string;
  track: string;
  repoUrl: string;
}

const projects: Project[] = [
  {
    id: "1",
    title: "Glass Signal",
    summary:
      "A project management and hackathon workflow platform.",
    track: "Web",
    repoUrl: "https://github.com/",
  },
  {
    id: "2",
    title: "Code Orbit",
    summary:
      "A developer collaboration platform.",
    track: "AI",
    repoUrl: "https://github.com/",
  },
  {
    id: "3",
    title: "Data Forge",
    summary:
      "A data-focused developer tool.",
    track: "Data",
    repoUrl: "https://github.com/",
  },
];

export default function Gallery() {
  const [search, setSearch] = useState("");

  const filteredProjects = useMemo(() => {
    return projects.filter((project) =>
      `${project.title} ${project.summary} ${project.track}`
        .toLowerCase()
        .includes(search.toLowerCase())
    );
  }, [search]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">
          Project Gallery
        </h1>

        <p className="mt-2 text-gray-400">
          Explore submitted projects.
        </p>
      </div>

      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search projects..."
        className="w-full rounded-xl border border-white/10 bg-[#101522] px-4 py-3 outline-none focus:border-blue-500"
      />

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {filteredProjects.map((project) => (
          <article
            key={project.id}
            className="rounded-xl border border-white/10 bg-[#101522] p-5"
          >
            <div className="flex justify-between gap-3">
              <h2 className="font-semibold">
                {project.title}
              </h2>

              <span className="text-xs text-blue-400">
                {project.track}
              </span>
            </div>

            <p className="mt-3 text-sm text-gray-400">
              {project.summary}
            </p>

            <a
              href={project.repoUrl}
              target="_blank"
              rel="noreferrer"
              className="mt-5 inline-block text-sm text-blue-400 hover:text-blue-300"
            >
              Repository →
            </a>
          </article>
        ))}
      </div>
    </div>
  );
}