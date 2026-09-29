const adminActions = [
  "Manage Events",
  "Manage Tracks",
  "Manage Judges",
  "Manage Users",
  "Export Results",
];

export default function Admin() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Admin</h1>

        <p className="mt-2 text-gray-400">
          Administrative controls.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {adminActions.map((action) => (
          <button
            key={action}
            className="rounded-xl border border-white/10 bg-[#101522] p-6 text-left transition hover:border-blue-500/30 hover:bg-white/5"
          >
            <h2 className="font-semibold">{action}</h2>

            <p className="mt-2 text-sm text-gray-500">
              Configure {action.toLowerCase()}.
            </p>
          </button>
        ))}
      </div>
    </div>
  );
}