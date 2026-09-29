import { useNavigate } from "react-router-dom";

import TeamCard from "../components/TeamCard";
import type { Team } from "../types/teams";

const teams: Team[] = [
  {
    id: "team-1",
    name: "Demo Team",
    eventId: "event-1",
    createdAt: "2026-09-29T10:00:00Z",
    members: [
      {
        id: "member-1",
        userId: "user-1",
        name: "Demo User",
        email: "demo@example.com",
      },
    ],
  },
];

export default function Teams() {
  const navigate = useNavigate();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Teams</h1>
        <p className="mt-2 text-gray-400">
          Manage your hackathon teams.
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {teams.map((team) => (
          <TeamCard
            key={team.id}
            team={team}
            onSelect={() => navigate(`/teams/${team.id}`)}
          />
        ))}
      </div>
    </div>
  );
}