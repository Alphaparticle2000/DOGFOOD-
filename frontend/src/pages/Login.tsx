import React, { useState } from 'react'
import { useAuth } from "../context/AuthContext";
import { Code2, Mail, LockKeyhole } from "lucide-react";

const Login = () => {

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const { login } = useAuth();
  console.log(login);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(email);
  };

  return (
    <>
      <div className="min-h-screen w-full bg-linear-to-br from-[#070B14] via-[#101A3D] to-[#25105C] text-white grid grid-cols-1 md:grid-cols-2">

        <div className="flex flex-col justify-center px-20">

          <div className="flex items-center gap-3 mb-10">
            <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-purple-500/10 border border-purple-500/30">
              <Code2 size={28} className="text-purple-400" />
            </div>

            <span className="text-2xl font-bold tracking-wide">
              Hackathon RAPTX
            </span>
          </div>

          <div className="max-w-lg">
            <h1 className="text-5xl font-bold leading-tight">
              Build.
              <br />
              <span className="text-purple-400">
                Submit.
              </span>
              <br />
              Get Recognized.
            </h1>

            <p className="mt-6 text-gray-400 text-lg leading-relaxed">
              A unified platform for hackathons, projects,
              teams and judging.
            </p>
          </div>

          <div className="mt-12 text-sm text-gray-500">
            HACKATHON RAPTZ 2026
          </div>

        </div>

        <div className="flex items-center justify-center px-16">

          <div className="w-full max-w-md rounded-2xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl shadow-2xl">

            <div className="mb-8">
              <h2 className="text-3xl font-bold">
                Welcome Back
              </h2>

              <p className="mt-2 text-sm text-gray-400">
                Sign in to continue to HACKATHON RAPTZ
              </p>
            </div>

            <form onSubmit={handleSubmit}>
            <div className="mb-5">

              <label className="mb-2 block text-sm text-gray-300">
                Email
              </label>

              <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-black/20 px-4 py-3">

                <Mail
                  size={19}
                  className="text-gray-500"
                />

                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-transparent outline-none text-white placeholder:text-gray-600"
                />

              </div>

            </div>

            <div className="mb-6">

              <label className="mb-2 block text-sm text-gray-300">
                Password
              </label>

              <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-black/20 px-4 py-3">

                <LockKeyhole
                  size={19}
                  className="text-gray-500"
                />

                <input
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-transparent outline-none text-white placeholder:text-gray-600"
                />

              </div>

            </div>
              <button
                type='submit'
                className="w-full rounded-xl bg-linear-to-r from-purple-500 to-blue-500 py-3 font-semibold transition hover:opacity-90"
              >
                Sign In
              </button>

              <p className="mt-6 text-center text-xs text-gray-500">
                Secure access to your HACKATHON RAPTZ workspace
              </p>
            </form>
          </div>

        </div>

      </div>
    </>
  )
}

export default Login