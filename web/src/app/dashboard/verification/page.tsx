"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

interface Bot {
  id: number;
  bot_username: string;
  bot_name: string;
  bot_type: string;
  is_active: boolean;
  users_count: number;
  verifications_count: number;
  pending_count: number;
}

export default function VerificationPage() {
  const [bots, setBots] = useState<Bot[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const result = await api.getBots();
      if (result.data?.bots) {
        setBots(
          result.data.bots.filter((b: Bot) => b.bot_type === "verification"),
        );
      }
      setIsLoading(false);
    };
    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-green-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-3">
            <span className="w-10 h-10 rounded-lg bg-gradient-to-br from-green-500/20 to-green-600/20 flex items-center justify-center text-green-400">
              <svg
                className="w-5 h-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </span>
            Verification Bots
          </h1>
          <p className="text-[var(--text-muted)] mt-1">
            Bot verifikasi mahasiswa/anggota sederhana
          </p>
        </div>
      </div>

      {bots.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="w-16 h-16 mx-auto rounded-xl bg-gradient-to-br from-green-500/20 to-green-600/20 flex items-center justify-center mb-4 text-green-400">
            <svg
              className="w-8 h-8"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold mb-2">
            Belum ada Verification Bot
          </h3>
          <p className="text-[var(--text-muted)]">
            Tambahkan bot dengan type &quot;verification&quot; untuk memulai
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {bots.map((bot) => (
            <div key={bot.id} className="glass-card p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center text-white font-bold text-lg">
                  {bot.bot_name?.charAt(0) || "V"}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold">{bot.bot_name}</h3>
                  <p className="text-sm text-[var(--text-muted)]">
                    @{bot.bot_username}
                  </p>
                </div>
                <span
                  className={`w-3 h-3 rounded-full ${bot.is_active ? "bg-green-500" : "bg-red-500"}`}
                />
              </div>

              <div className="grid grid-cols-3 gap-4 text-center py-4 border-t border-b border-[var(--border-color)]">
                <div>
                  <p className="text-xl font-bold text-green-400">
                    {bot.users_count || 0}
                  </p>
                  <p className="text-xs text-[var(--text-muted)]">Users</p>
                </div>
                <div>
                  <p className="text-xl font-bold text-blue-400">
                    {bot.verifications_count || 0}
                  </p>
                  <p className="text-xs text-[var(--text-muted)]">Verified</p>
                </div>
                <div>
                  <p className="text-xl font-bold text-yellow-400">
                    {bot.pending_count || 0}
                  </p>
                  <p className="text-xs text-[var(--text-muted)]">Pending</p>
                </div>
              </div>

              <div className="flex gap-2 mt-4">
                <button className="flex-1 px-4 py-2 text-sm font-medium text-green-400 bg-green-500/10 rounded-lg hover:bg-green-500/20 transition-colors">
                  Lihat Pending
                </button>
                <button className="flex-1 px-4 py-2 text-sm font-medium text-[var(--text-secondary)] bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                  Riwayat
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
