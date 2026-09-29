import { NavLink } from "react-router-dom";

const links = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Events", path: "/events" },
  { label: "Teams", path: "/teams" },
  { label: "Submissions", path: "/submissions" },
  { label: "Gallery", path: "/gallery" },
  { label: "Judging", path: "/judging" },
  { label: "Voting", path: "/voting" },
  { label: "Results", path: "/results" },
  { label: "Admin", path: "/admin" },
];

export default function Sidebar() {
  return (
    <aside className="hidden min-h-[calc(100vh-4rem)] w-60 shrink-0 border-r border-white/10 bg-[#0B0F19] p-4 md:block">
      <nav className="space-y-1">
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              `block rounded-lg px-4 py-3 text-sm transition ${
                isActive
                  ? "bg-blue-600/15 text-blue-400"
                  : "text-gray-400 hover:bg-white/5 hover:text-white"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}