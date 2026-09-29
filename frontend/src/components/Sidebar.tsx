import {
  CalendarDays,
  ChevronRight,
  FileUp,
  Gauge,
  GitBranch,
  LayoutGrid,
  Settings,
  ShieldCheck,
  Trophy,
  UsersRound,
  X,
} from "lucide-react";

import { NavLink } from "react-router-dom";

type SidebarProps = {
  open: boolean;
  onClose: () => void;
};

const groups = [
  {
    label: "WORKSPACE",
    items: [
      {
        label: "Overview",
        path: "/dashboard",
        icon: Gauge,
      },
      {
        label: "Events",
        path: "/events",
        icon: CalendarDays,
      },
      {
        label: "Teams",
        path: "/teams",
        icon: UsersRound,
      },
      {
        label: "Submissions",
        path: "/submissions",
        icon: FileUp,
        count: "03",
      },
      {
        label: "Gallery",
        path: "/gallery",
        icon: LayoutGrid,
      },
    ],
  },
  {
    label: "COMPETITION",
    items: [
      {
        label: "Judging",
        path: "/judging",
        icon: GitBranch,
      },
      {
        label: "Results",
        path: "/results",
        icon: Trophy,
      },
    ],
  },
];

export default function Sidebar({
  open,
  onClose,
}: SidebarProps) {
  return (
    <>
      {open && (
        <button
          className="sidebar-overlay"
          aria-label="Close navigation"
          onClick={onClose}
        />
      )}

      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
        <div className="sidebar-header">
          <NavLink
            to="/dashboard"
            className="brand-lockup"
            onClick={onClose}
          >
            <span className="brand-mark">D</span>

            <span className="brand-copy">
              <strong>DOGFOOD</strong>
              <small>HACKATHON PLATFORM</small>
            </span>
          </NavLink>

          <button
            className="sidebar-close"
            aria-label="Close navigation"
            onClick={onClose}
          >
            <X size={17} />
          </button>
        </div>

        <div className="sidebar-scroll">
          {groups.map((group) => (
            <section
              className="nav-group"
              key={group.label}
            >
              <div className="nav-caption">
                {group.label}
              </div>

              <nav
                className="nav-list"
                aria-label={group.label}
              >
                {group.items.map(
                  ({
                    label,
                    path,
                    icon: Icon,
                    count,
                  }) => (
                    <NavLink
                      key={path}
                      to={path}
                      end={path === "/dashboard"}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `nav-item ${
                          isActive ? "active" : ""
                        }`
                      }
                    >
                      <Icon
                        size={17}
                        strokeWidth={1.8}
                        aria-hidden="true"
                      />

                      <span>{label}</span>

                      {count && (
                        <span className="nav-count">
                          {count}
                        </span>
                      )}
                    </NavLink>
                  )
                )}
              </nav>
            </section>
          ))}

          <section className="sidebar-event">
            <div className="kicker">
              <span className="live-dot" />
              LIVE EVENT
            </div>

            <h3>RAPTX 2026</h3>

            <p>
              Final submissions are still open. Keep an
              eye on the closing window.
            </p>

            <NavLink
              to="/events"
              onClick={onClose}
            >
              Open event
              <ChevronRight size={14} />
            </NavLink>
          </section>
        </div>

        <div className="sidebar-footer">
          <NavLink
            to="/admin"
            onClick={onClose}
            className={({ isActive }) =>
              `nav-item ${
                isActive ? "active" : ""
              }`
            }
          >
            <ShieldCheck
              size={17}
              strokeWidth={1.8}
            />

            <span>Admin</span>
          </NavLink>

          <button
            className="nav-item"
            type="button"
          >
            <Settings
              size={17}
              strokeWidth={1.8}
            />

            <span>Settings</span>
          </button>
        </div>
      </aside>
    </>
  );
}