"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";

interface Bot {
  id: number;
  bot_username: string;
  bot_name: string;
}

interface Transaction {
  id: number;
  order_id: string;
  product_name: string;
  buyer_username: string;
  amount: number;
  status: string;
  payment_method: string;
  created_at: string;
  paid_at: string | null;
}

interface Stats {
  total_transactions: number;
  completed_transactions: number;
  total_revenue: number;
}

export default function TransactionsPage() {
  const [bots, setBots] = useState<Bot[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [stats, setStats] = useState<Stats>({
    total_transactions: 0,
    completed_transactions: 0,
    total_revenue: 0,
  });
  const [selectedBotId, setSelectedBotId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    fetchBots();
  }, []);

  useEffect(() => {
    if (selectedBotId) {
      fetchTransactions(selectedBotId);
    }
  }, [selectedBotId]);

  const fetchBots = async () => {
    const result = await api.getBots();
    if (result.data?.bots) {
      setBots(result.data.bots);
      if (result.data.bots.length > 0) {
        setSelectedBotId(result.data.bots[0].id);
      }
    }
    setIsLoading(false);
  };

  const fetchTransactions = async (botId: number) => {
    const result = await api.getTransactions(botId);
    if (result.data) {
      setTransactions(result.data.transactions || []);
      setStats(
        result.data.stats || {
          total_transactions: 0,
          completed_transactions: 0,
          total_revenue: 0,
        }
      );
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return (
          <span className="px-2 py-1 rounded-lg text-xs text-green-400 bg-green-400/10">
            Sukses
          </span>
        );
      case "pending":
        return (
          <span className="px-2 py-1 rounded-lg text-xs text-yellow-400 bg-yellow-400/10">
            Pending
          </span>
        );
      case "expired":
        return (
          <span className="px-2 py-1 rounded-lg text-xs text-red-400 bg-red-400/10">
            Expired
          </span>
        );
      case "cancelled":
        return (
          <span className="px-2 py-1 rounded-lg text-xs text-gray-400 bg-gray-400/10">
            Dibatalkan
          </span>
        );
      default:
        return (
          <span className="px-2 py-1 rounded-lg text-xs text-gray-400 bg-gray-400/10">
            {status}
          </span>
        );
    }
  };

  const filteredTransactions =
    statusFilter === "all"
      ? transactions
      : transactions.filter((t) => t.status === statusFilter);

  const formatDate = (dateStr: string) => {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleString("id-ID", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

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

  if (bots.length === 0) {
    return (
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
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-xl font-semibold mb-2">Tambah Bot Dulu</h3>
        <p className="text-[var(--text-muted)] mb-6">
          Anda perlu menambahkan bot terlebih dahulu
        </p>
        <a href="/dashboard/bots" className="btn-primary">
          Tambah Bot
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Transaksi</h1>
        <p className="text-[var(--text-muted)]">Riwayat transaksi toko Anda</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-card p-6">
          <p className="text-[var(--text-muted)] text-sm">Total Transaksi</p>
          <p className="text-2xl font-bold mt-1">{stats.total_transactions}</p>
        </div>
        <div className="glass-card p-6">
          <p className="text-[var(--text-muted)] text-sm">Transaksi Sukses</p>
          <p className="text-2xl font-bold mt-1 text-green-400">
            {stats.completed_transactions}
          </p>
        </div>
        <div className="glass-card p-6">
          <p className="text-[var(--text-muted)] text-sm">Total Pendapatan</p>
          <p className="text-2xl font-bold mt-1">
            Rp {stats.total_revenue.toLocaleString("id-ID")}
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium mb-2">Pilih Bot</label>
            <select
              value={selectedBotId || ""}
              onChange={(e) => setSelectedBotId(parseInt(e.target.value))}
              className="w-full px-4 py-2 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
            >
              {bots.map((bot) => (
                <option key={bot.id} value={bot.id}>
                  {bot.bot_name} ({bot.bot_username})
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium mb-2">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-4 py-2 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
            >
              <option value="all">Semua Status</option>
              <option value="completed">Sukses</option>
              <option value="pending">Pending</option>
              <option value="expired">Expired</option>
              <option value="cancelled">Dibatalkan</option>
            </select>
          </div>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="glass-card overflow-hidden">
        {filteredTransactions.length === 0 ? (
          <div className="p-12 text-center">
            <p className="text-[var(--text-muted)]">Belum ada transaksi</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-[var(--bg-dark)]">
                <tr>
                  <th className="text-left px-6 py-4 text-sm font-medium text-[var(--text-muted)]">
                    Order ID
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-[var(--text-muted)]">
                    Produk
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-[var(--text-muted)]">
                    Pembeli
                  </th>
                  <th className="text-right px-6 py-4 text-sm font-medium text-[var(--text-muted)]">
                    Jumlah
                  </th>
                  <th className="text-center px-6 py-4 text-sm font-medium text-[var(--text-muted)]">
                    Status
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-[var(--text-muted)]">
                    Tanggal
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border-color)]">
                {filteredTransactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-[var(--bg-dark)]/50">
                    <td className="px-6 py-4">
                      <span className="font-mono text-sm">{tx.order_id}</span>
                    </td>
                    <td className="px-6 py-4">{tx.product_name || "-"}</td>
                    <td className="px-6 py-4">
                      @{tx.buyer_username || "unknown"}
                    </td>
                    <td className="px-6 py-4 text-right font-medium">
                      Rp {tx.amount.toLocaleString("id-ID")}
                    </td>
                    <td className="px-6 py-4 text-center">
                      {getStatusBadge(tx.status)}
                    </td>
                    <td className="px-6 py-4 text-sm text-[var(--text-muted)]">
                      {formatDate(tx.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
