import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";

import AuthLayout from "./layout/AuthLayout";
import DashboardLayout from "./layout/DashboardLayout";

import ProtectedRoute from "./components/ProtectedRoutes";

import Login from "./pages/Login";
import Register from "./pages/Register";

import Dashboard from "./pages/Dashboard";
import Events from "./pages/Events";
import Teams from "./pages/Team";
import TeamDetails from "./pages/TeamsDetails";
import Submissions from "./pages/Submission";
import Gallery from "./pages/Gallery";
import Judging from "./pages/Judging";
import Voting from "./pages/Voting";
import Results from "./pages/results";
import Admin from "./pages/Admin";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Login />} />
          
          {/* PUBLIC */}
          <Route element={<AuthLayout />}>
            <Route
              path="/login"
              element={<Login />}
            />

            <Route
              path="/register"
              element={<Register />}
            />
          </Route>

          <Route
            path="/gallery"
            element={<Gallery />}
          />

          {/* PROTECTED */}
          <Route element={<ProtectedRoute />}>

            <Route
              element={<DashboardLayout />}
            >

              <Route
                path="/dashboard"
                element={<Dashboard />}
              />

              <Route
                path="/events"
                element={<Events />}
              />

              <Route
                path="/teams"
                element={<Teams />}
              />

              <Route
                path="/teams/:teamId"
                element={<TeamDetails />}
              />

              <Route
                path="/submissions"
                element={<Submissions />}
              />

              <Route
                path="/judging"
                element={<Judging />}
              />

              <Route
                path="/voting"
                element={<Voting />}
              />

              <Route
                path="/results"
                element={<Results />}
              />

              <Route path="/admin" element={<Admin />} />

            </Route>

          </Route>

        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}