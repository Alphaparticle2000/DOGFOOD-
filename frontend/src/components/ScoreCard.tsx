interface ScoreCardProps {
  title: string;
  score: number;
  maxScore: number;
}

export default function ScoreCard({
  title,
  score,
  maxScore,
}: ScoreCardProps) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#101522] p-5">
      <p className="text-sm text-gray-400">{title}</p>

      <div className="mt-3 flex items-end gap-1">
        <span className="text-3xl font-bold">{score}</span>
        <span className="pb-1 text-sm text-gray-500">
          / {maxScore}
        </span>
      </div>
    </div>
  );
}