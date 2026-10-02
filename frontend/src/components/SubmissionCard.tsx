import type { Team } from "../types/teams";

interface TeamCardProps {
  team: Team;
  onSelect?: () => void;
}

export default function TeamCard({
  team,
  onSelect,
}: TeamCardProps) {
  return (
    <button
      onClick={onSelect}
      className="w-full rounded-xl border border-white/10 bg-[#101522] p-5 text-left transition hover:border-blue-500/40 hover:bg-[#131a29]"
    >
      <h3 className="font-semibold">{team.name}</h3>

      <p className="mt-2 text-sm text-gray-400">
        {team.members.length} member
        {team.members.length !== 1 ? "s" : ""}
      </p>
    </button>
  );
}