import { Bell, ChevronDown, LogOut, Menu, Search } from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

type NavbarProps = {
  onMenuClick: () => void;
};

export default function Navbar({ onMenuClick }: NavbarProps) {
  const { user, logout } = useAuth();

  const initial = (user?.name?.trim()?.[0] ?? "U").toUpperCase();

  return (
    <header className="topbar">
      <div className="topbar-left">
        <button
          className="mobile-menu"
          aria-label="Open navigation"
          onClick={onMenuClick}
        >
          <Menu size={17} />
        </button>

        <Link to="/dashboard" className="mobile-brand">
          <span className="brand-mark">D</span>
          <span>DOGFOOD</span>
        </Link>

        <label className="global-search">
          <Search size={16} aria-hidden="true" />

          <input
            aria-label="Search projects and teams"
            placeholder="Search projects, teams…"
          />

          <span className="search-shortcut">⌘ K</span>
        </label>
      </div>

      <div className="topbar-right">
        <button
          className="icon-btn"
          aria-label="Notifications"
          style={{ position: "relative" }}
        >
          <Bell size={17} />
          <span className="notify-dot" />
        </button>

        <button
          className="profile-trigger"
          type="button"
          onClick={logout}
          title="Sign out"
        >
          <span className="avatar">{initial}</span>

          <span className="profile-copy">
            <strong>{user?.name ?? "User"}</strong>
            <small>{user?.role ?? "participant"}</small>
          </span>

          <ChevronDown size={14} />

          <LogOut
            size={14}
            style={{ display: "none" }}
          />
        </button>
      </div>
    </header>
  );
}