"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  return (
    <div className="min-h-screen bg-[var(--bg-dark)] flex flex-col">
      {/* Background Effects */}
      <div className="bg-glow-blob blob-1" />
      <div className="bg-glow-blob blob-2" />

      {/* Main Content */}
      <div className="flex-1 flex flex-col items-center justify-center px-4 relative z-10">
        {/* Logo */}
        <div className="mb-8 flex items-center gap-3">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-secondary)] flex items-center justify-center shadow-lg">
            <svg
              className="w-9 h-9 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-4xl md:text-5xl font-bold text-center mb-4">
          <span className="gradient-text">Bot Manager</span>
        </h1>

        {/* Subtitle */}
        <p className="text-[var(--text-secondary)] text-lg text-center max-w-md mb-8">
          Platform untuk mengelola semua bot Telegram Anda dari satu dashboard.
        </p>

        {/* Bot Type Badges */}
        <div className="flex flex-wrap justify-center gap-3 mb-10">
          <span className="px-4 py-2 rounded-full bg-blue-500/10 text-blue-400 text-sm font-medium border border-blue-500/20">
            🏪 Store Bot
          </span>
          <span className="px-4 py-2 rounded-full bg-green-500/10 text-green-400 text-sm font-medium border border-green-500/20">
            ✅ Verification Bot
          </span>
          <span className="px-4 py-2 rounded-full bg-purple-500/10 text-purple-400 text-sm font-medium border border-purple-500/20">
            📊 Points Verify Bot
          </span>
          <span className="px-4 py-2 rounded-full bg-orange-500/10 text-orange-400 text-sm font-medium border border-orange-500/20">
            ⚙️ Custom Bot
          </span>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          {isLoggedIn ? (
            <Link href="/dashboard" className="btn-primary text-lg px-8 py-4">
              <svg
                className="w-5 h-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                />
              </svg>
              Buka Dashboard
            </Link>
          ) : (
            <>
              <Link
                href="/auth/login"
                className="btn-primary text-lg px-8 py-4"
              >
                Masuk
              </Link>
              <Link
                href="/auth/register"
                className="btn-secondary text-lg px-8 py-4"
              >
                Daftar
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="py-6 text-center text-[var(--text-muted)] text-sm">
        <p>© 2024 Bot Manager. Personal Use Only.</p>
      </footer>
    </div>
  );
}
