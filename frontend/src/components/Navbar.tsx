import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-[#080B14]/95 backdrop-blur">
      <div className="flex h-16 items-center justify-between px-6">
        <Link
          to="/dashboard"
          className="text-lg font-bold tracking-wide"
        >
          DOGFOOD
        </Link>

        <div className="flex items-center gap-4">
          <div className="hidden text-right sm:block">
            <p className="text-sm font-medium">
              {user?.name ?? "User"}
            </p>

            <p className="text-xs capitalize text-gray-500">
              {user?.role ?? "participant"}
            </p>
          </div>

          <button
            onClick={logout}
            className="rounded-lg border border-white/10 px-3 py-2 text-sm text-gray-300 transition hover:bg-white/5 hover:text-white"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}