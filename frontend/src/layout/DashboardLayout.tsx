import { useState } from "react";
import { Outlet } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function DashboardLayout() {
  const [open, setOpen] = useState(false);

  return (
    <div className="app-shell">
      <Sidebar
        open={open}
        onClose={() => setOpen(false)}
      />

      <div className="main-shell">
        <Navbar
          onMenuClick={() => setOpen(true)}
        />

        <main className="page-shell">
          <div className="page-frame">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}