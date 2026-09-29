import { Link, useParams } from "react-router-dom";

export default function TeamDetails() {
  const { teamId } = useParams();

  return (
    <div className="space-y-6">
      <Link
        to="/teams"
        className="text-sm text-blue-400 hover:text-blue-300"
      >
        ← Back to teams
      </Link>

      <div>
        <p className="text-sm text-gray-500">
          Team ID: {teamId}
        </p>

        <h1 className="mt-1 text-3xl font-bold">
          Demo Team
        </h1>
      </div>

      <div className="rounded-xl border border-white/10 bg-[#101522] p-6">
        <h2 className="text-lg font-semibold">
          Team Members
        </h2>

        <div className="mt-4 space-y-3">
          <div className="rounded-lg bg-white/5 p-4">
            Demo User
          </div>
        </div>
      </div>
    </div>
  );
}