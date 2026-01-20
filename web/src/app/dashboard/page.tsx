"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import api from "@/lib/api";

interface Bot {
  id: number;
  bot_username: string;
  bot_name: string;
  bot_type: string;
  is_active: boolean;
  products_count?: number;
  users_count?: number;
  transactions_count?: number;
  verifications_count?: number;
}

interface Stats {
  total_bots: number;
  store_bots: number;
  verification_bots: number;
  points_verify_bots: number;
}

const botTypeConfig: Record<
  string,
  { label: string; color: string; icon: React.ReactNode }
> = {
  store: {
    label: "Store",
    color: "blue",
    icon: (
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
          d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
        />
      </svg>
    ),
  },
  verification: {
    label: "Verification",
    color: "green",
    icon: (
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
    ),
  },
  points_verify: {
    label: "Points Verify",
    color: "purple",
    icon: (
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
          d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
    ),
  },
  custom: {
    label: "Custom",
    color: "orange",
    icon: (
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
          d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
        />
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
        />
      </svg>
    ),
  },
};

const getColorClasses = (color: string) => {
  const colors: Record<string, { bg: string; text: string; border: string }> = {
    blue: {
      bg: "from-blue-500/20 to-blue-600/20",
      text: "text-blue-400",
      border: "border-blue-500/30",
    },
    green: {
      bg: "from-green-500/20 to-green-600/20",
      text: "text-green-400",
      border: "border-green-500/30",
    },
    purple: {
      bg: "from-purple-500/20 to-purple-600/20",
      text: "text-purple-400",
      border: "border-purple-500/30",
    },
    orange: {
      bg: "from-orange-500/20 to-orange-600/20",
      text: "text-orange-400",
      border: "border-orange-500/30",
    },
  };
  return colors[color] || colors.blue;
};

export default function DashboardPage() {
  const [bots, setBots] = useState<Bot[]>([]);
  const [stats, setStats] = useState<Stats>({
    total_bots: 0,
    store_bots: 0,
    verification_bots: 0,
    points_verify_bots: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const result = await api.getBots();
      if (result.data?.bots) {
        const botsList = result.data.bots;
        setBots(botsList);
        setStats({
          total_bots: botsList.length,
          store_bots: botsList.filter((b: Bot) => b.bot_type === "store")
            .length,
          verification_bots: botsList.filter(
            (b: Bot) => b.bot_type === "verification",
          ).length,
          points_verify_bots: botsList.filter(
            (b: Bot) => b.bot_type === "points_verify",
          ).length,
        });
      }
      setIsLoading(false);
    };
    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <svg
            className="w-8 h-8 animate-spin mx-auto mb-4 text-[var(--color-primary)]"
            viewBox="0 0 24 24"
          >
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
          <p className="text-[var(--text-muted)]">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-[var(--text-muted)]">
            Kelola semua bot Telegram Anda dari sini.
          </p>
        </div>
        <Link href="/dashboard/bots" className="btn-primary">
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
              d="M12 4v16m8-8H4"
            />
          </svg>
          Tambah Bot
        </Link>
      </div>

      {/* Stats by Bot Type */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-primary)]/20 to-[var(--color-secondary)]/20 flex items-center justify-center text-[var(--color-primary)]">
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
                  d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
          </div>
          <p className="text-2xl font-bold">{stats.total_bots}</p>
          <p className="text-sm text-[var(--text-muted)]">Total Bot</p>
        </div>

        {[
          { key: "store_bots", type: "store", count: stats.store_bots },
          {
            key: "verification_bots",
            type: "verification",
            count: stats.verification_bots,
          },
          {
            key: "points_verify_bots",
            type: "points_verify",
            count: stats.points_verify_bots,
          },
        ].map((item) => {
          const config = botTypeConfig[item.type];
          const colors = getColorClasses(config.color);
          return (
            <div key={item.key} className="glass-card p-6">
              <div className="flex items-center gap-3 mb-3">
                <div
                  className={`w-10 h-10 rounded-xl bg-gradient-to-br ${colors.bg} flex items-center justify-center ${colors.text}`}
                >
                  {config.icon}
                </div>
              </div>
              <p className="text-2xl font-bold">{item.count}</p>
              <p className="text-sm text-[var(--text-muted)]">{config.label}</p>
            </div>
          );
        })}
      </div>

      {/* Bot List by Type */}
      {bots.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-[var(--color-primary)]/20 to-[var(--color-secondary)]/20 flex items-center justify-center mb-6">
            <svg
              className="w-10 h-10 text-[var(--color-primary)]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-2">Belum Ada Bot</h3>
          <p className="text-[var(--text-muted)] mb-6">
            Mulai dengan menambahkan bot Telegram pertama Anda
          </p>
          <Link href="/dashboard/bots" className="btn-primary">
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
                d="M12 4v16m8-8H4"
              />
            </svg>
            Tambah Bot Pertama
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Group bots by type */}
          {Object.entries(botTypeConfig).map(([type, config]) => {
            const typeBots = bots.filter((b) => b.bot_type === type);
            if (typeBots.length === 0) return null;

            const colors = getColorClasses(config.color);

            return (
              <div key={type} className="glass-card p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg bg-gradient-to-br ${colors.bg} flex items-center justify-center ${colors.text}`}
                    >
                      {config.icon}
                    </div>
                    <h2 className="font-semibold">{config.label} Bots</h2>
                    <span
                      className={`px-2 py-0.5 rounded-full text-xs ${colors.text} ${colors.border} border`}
                    >
                      {typeBots.length}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {typeBots.map((bot) => (
                    <div
                      key={bot.id}
                      className={`p-4 rounded-xl bg-[var(--bg-dark)] border ${bot.is_active ? colors.border : "border-red-500/30"}`}
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <div
                          className={`w-10 h-10 rounded-lg bg-gradient-to-br ${colors.bg} flex items-center justify-center ${colors.text} font-bold`}
                        >
                          {bot.bot_name?.charAt(0) || "B"}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="font-medium truncate">
                            {bot.bot_name || "Unnamed"}
                          </p>
                          <p className="text-xs text-[var(--text-muted)] truncate">
                            @{bot.bot_username}
                          </p>
                        </div>
                        <span
                          className={`w-2 h-2 rounded-full ${bot.is_active ? "bg-green-500" : "bg-red-500"}`}
                        />
                      </div>

                      {type === "store" && (
                        <div className="grid grid-cols-3 gap-2 text-center text-sm">
                          <div>
                            <p className="font-semibold">
                              {bot.products_count || 0}
                            </p>
                            <p className="text-xs text-[var(--text-muted)]">
                              Produk
                            </p>
                          </div>
                          <div>
                            <p className="font-semibold">
                              {bot.users_count || 0}
                            </p>
                            <p className="text-xs text-[var(--text-muted)]">
                              Users
                            </p>
                          </div>
                          <div>
                            <p className="font-semibold">
                              {bot.transactions_count || 0}
                            </p>
                            <p className="text-xs text-[var(--text-muted)]">
                              Order
                            </p>
                          </div>
                        </div>
                      )}

                      {type === "verification" && (
                        <div className="grid grid-cols-2 gap-2 text-center text-sm">
                          <div>
                            <p className="font-semibold">
                              {bot.users_count || 0}
                            </p>
                            <p className="text-xs text-[var(--text-muted)]">
                              Users
                            </p>
                          </div>
                          <div>
                            <p className="font-semibold">
                              {bot.verifications_count || 0}
                            </p>
                            <p className="text-xs text-[var(--text-muted)]">
                              Verified
                            </p>
                          </div>
                        </div>
                      )}

                      {type === "points_verify" && (
                        <div className="grid grid-cols-2 gap-2 text-center text-sm">
                          <div>
                            <p className="font-semibold">
                              {bot.users_count || 0}
                            </p>
                            <p className="text-xs text-[var(--text-muted)]">
                              Users
                            </p>
                          </div>
                          <div>
                            <p className="font-semibold">
                              {bot.verifications_count || 0}
                            </p>
                            <p className="text-xs text-[var(--text-muted)]">
                              Verifikasi
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
