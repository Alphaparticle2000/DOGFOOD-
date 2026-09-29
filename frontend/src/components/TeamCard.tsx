import type { Team } from "../types/teams";

type TeamCardProps = {
  team: Team;
  onSelect: () => void;
};

export default function TeamCard({
  team,
  onSelect,
}: TeamCardProps) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-white">
            {team.name}
          </h2>

          <p className="mt-1 text-sm text-gray-400">
            {team.members.length} member
            {team.members.length !== 1 ? "s" : ""}
          </p>
        </div>

        <button
          type="button"
          onClick={onSelect}
          className="rounded-lg bg-white px-4 py-2 text-sm font-medium text-black hover:bg-gray-200"
        >
          View
        </button>
      </div>

      <div className="mt-4 space-y-2">
        {team.members.map((member) => (
          <div
            key={member.id}
            className="rounded-lg bg-black/20 px-3 py-2"
          >
            <p className="text-sm font-medium text-white">
              {member.name}
            </p>

            <p className="text-xs text-gray-400">
              {member.email}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}