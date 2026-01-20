"use client";

import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/lib/auth";

export default function LoginPage() {
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    const result = await login(formData.email, formData.password);

    if (result.error) {
      setError(result.error);
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-grid">
      {/* Background Effects */}
      <div className="bg-glow-blob blob-1" />
      <div className="bg-glow-blob blob-2" />

      <div className="relative w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-secondary)] flex items-center justify-center">
              <svg
                className="w-7 h-7 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <span className="text-2xl font-bold gradient-text">BotStore</span>
          </Link>
        </div>

        {/* Card */}
        <div className="glass-card p-8">
          <h1 className="text-2xl font-bold text-center mb-2">
            Selamat Datang Kembali
          </h1>
          <p className="text-[var(--text-muted)] text-center mb-6">
            Masuk ke dashboard untuk kelola bot Anda
          </p>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                required
                placeholder="john@example.com"
                className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--color-primary)] transition-all"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium">Password</label>
                <a
                  href="#"
                  className="text-xs text-[var(--color-primary)] hover:underline"
                >
                  Lupa password?
                </a>
              </div>
              <input
                type="password"
                required
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--color-primary)] transition-all"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full !py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Masuk...
                </span>
              ) : (
                "Masuk"
              )}
            </button>
          </form>

          <div className="mt-6 text-center text-sm">
            <span className="text-[var(--text-muted)]">Belum punya akun? </span>
            <Link
              href="/auth/register"
              className="text-[var(--color-primary)] hover:underline"
            >
              Daftar gratis
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
