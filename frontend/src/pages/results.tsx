const results = [
  {
    rank: 1,
    project: "Glass Signal",
    score: 92,
  },
  {
    rank: 2,
    project: "Code Orbit",
    score: 88,
  },
  {
    rank: 3,
    project: "Data Forge",
    score: 84,
  },
];

export default function Results() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Results</h1>

        <p className="mt-2 text-gray-400">
          Published hackathon results.
        </p>
      </div>

      <div className="overflow-hidden rounded-xl border border-white/10">
        {results.map((result) => (
          <div
            key={result.rank}
            className="flex items-center justify-between border-b border-white/10 bg-[#101522] p-5 last:border-b-0"
          >
            <div className="flex items-center gap-4">
              <span className="text-xl font-bold text-gray-500">
                #{result.rank}
              </span>

              <span>{result.project}</span>
            </div>

            <span className="font-semibold text-blue-400">
              {result.score}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}