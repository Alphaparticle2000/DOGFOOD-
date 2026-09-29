import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const stats = [
  {
    title: "My Team",
    value: "1",
    description: "Active team",
  },
  {
    title: "Project",
    value: "1",
    description: "Submission",
  },
  {
    title: "Status",
    value: "Draft",
    description: "Current state",
  },
  {
    title: "Deadline",
    value: "Open",
    description: "Submission window",
  },
];

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">

      <section>
        <p className="text-sm text-gray-500">Dashboard</p>

        <h1 className="mt-1 text-3xl font-bold">
          Welcome, {user?.name ?? "User"}
        </h1>

        <p className="mt-2 text-gray-400">
          Manage your hackathon activity from here.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.title}
            className="rounded-xl border border-white/10 bg-[#101522] p-5"
          >
            <p className="text-sm text-gray-500">
              {stat.title}
            </p>

            <p className="mt-2 text-2xl font-bold">
              {stat.value}
            </p>

            <p className="mt-1 text-xs text-gray-500">
              {stat.description}
            </p>
          </div>
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">

        <div className="rounded-2xl border border-white/10 bg-[#101522] p-6">
          <p className="text-sm text-blue-400">
            Current Project
          </p>

          <h2 className="mt-2 text-2xl font-semibold">
            No project selected
          </h2>

          <p className="mt-2 text-sm text-gray-400">
            Create or edit your hackathon submission.
          </p>

          <Link
            to="/submissions"
            className="mt-6 inline-block rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium hover:bg-blue-500"
          >
            Manage Submission
          </Link>
        </div>

        <div className="rounded-2xl border border-white/10 bg-[#101522] p-6">
          <p className="text-sm text-purple-400">
            Quick Actions
          </p>

          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            <Link
              to="/teams"
              className="rounded-lg border border-white/10 p-4 text-sm hover:bg-white/5"
            >
              Manage Team
            </Link>

            <Link
              to="/gallery"
              className="rounded-lg border border-white/10 p-4 text-sm hover:bg-white/5"
            >
              Browse Projects
            </Link>

            <Link
              to="/events"
              className="rounded-lg border border-white/10 p-4 text-sm hover:bg-white/5"
            >
              View Events
            </Link>

            <Link
              to="/results"
              className="rounded-lg border border-white/10 p-4 text-sm hover:bg-white/5"
            >
              View Results
            </Link>
          </div>
        </div>

      </section>
    </div>
  );
}