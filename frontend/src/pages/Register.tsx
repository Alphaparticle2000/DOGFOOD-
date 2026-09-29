import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setError("");

    if (!name || !email || !password || !confirmPassword) {
      setError("Please fill all fields.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    try {
      setLoading(true);

      // Backend_Register_type_api
      // TODO: Connect this to Supabase Auth / FastAPI registration.

      console.log({
        name,
        email,
        password,
      });

      // Temporary navigation for frontend testing
      navigate("/login");
    } catch (err) {
      console.error(err);
      setError("Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#080B14] text-white flex items-center justify-center px-4">
      <div className="w-full max-w-md">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight">
            Create Account
          </h1>

          <p className="text-gray-400 mt-2">
            Join the DOGFOOD hackathon
          </p>
        </div>

        {/* Register Card */}
        <div className="bg-[#101522] border border-white/10 rounded-2xl p-6 shadow-xl">

          {error && (
            <div className="mb-5 rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">

            {/* Name */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Full Name
              </label>

              <input
                type="text"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg border border-white/10 bg-[#080B14] px-4 py-3 text-white outline-none transition focus:border-blue-500"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Email
              </label>

              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border border-white/10 bg-[#080B14] px-4 py-3 text-white outline-none transition focus:border-blue-500"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Password
              </label>

              <input
                type="password"
                placeholder="Create a password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-white/10 bg-[#080B14] px-4 py-3 text-white outline-none transition focus:border-blue-500"
              />
            </div>

            {/* Confirm Password */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Confirm Password
              </label>

              <input
                type="password"
                placeholder="Confirm your password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full rounded-lg border border-white/10 bg-[#080B14] px-4 py-3 text-white outline-none transition focus:border-blue-500"
              />
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-blue-600 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>

          </form>

          {/* Login */}
          <p className="text-center text-sm text-gray-400 mt-6">
            Already have an account?{" "}
            <Link
              to="/login"
              className="text-blue-400 hover:text-blue-300"
            >
              Login
            </Link>
          </p>

        </div>
      </div>
    </div>
  );
}