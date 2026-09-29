import { Outlet } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-[#080B14] text-white">
      <Navbar />

      <div className="flex">
        <Sidebar />

        <main className="min-w-0 flex-1 p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}