"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";

interface Bot {
  id: number;
  bot_username: string;
  bot_name: string;
}

interface Broadcast {
  id: number;
  message: string;
  recipients_count: number;
  status: string;
  created_at: string;
}

export default function BroadcastPage() {
  const [bots, setBots] = useState<Bot[]>([]);
  const [broadcasts, setBroadcasts] = useState<Broadcast[]>([]);
  const [selectedBotId, setSelectedBotId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [result, setResult] = useState<{
    success: boolean;
    message: string;
  } | null>(null);

  useEffect(() => {
    fetchBots();
  }, []);

  useEffect(() => {
    if (selectedBotId) {
      fetchBroadcasts(selectedBotId);
    }
  }, [selectedBotId]);

  const fetchBots = async () => {
    const res = await api.getBots();
    if (res.data?.bots) {
      setBots(res.data.bots);
      if (res.data.bots.length > 0) {
        setSelectedBotId(res.data.bots[0].id);
      }
    }
    setIsLoading(false);
  };

  const fetchBroadcasts = async (botId: number) => {
    const res = await api.getBroadcasts(botId);
    if (res.data?.broadcasts) {
      setBroadcasts(res.data.broadcasts);
    }
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedBotId || !message.trim()) return;

    setIsSending(true);
    setResult(null);

    const res = await api.sendBroadcast(selectedBotId, message);

    if (res.error) {
      setResult({ success: false, message: res.error });
    } else {
      setResult({
        success: true,
        message: res.data?.message || "Broadcast berhasil dikirim!",
      });
      setMessage("");
      await fetchBroadcasts(selectedBotId);
    }

    setIsSending(false);
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleString("id-ID", {
      day: "numeric",
      month: "short",
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
              d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"
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
        <h1 className="text-2xl font-bold">Broadcast</h1>
        <p className="text-[var(--text-muted)]">
          Kirim pesan ke semua user bot Anda
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Compose Section */}
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold mb-4">Tulis Pesan</h2>

          <form onSubmit={handleSend} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Pilih Bot
              </label>
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

            <div>
              <label className="block text-sm font-medium mb-2">Pesan</label>
              <textarea
                rows={6}
                required
                placeholder="Tulis pesan broadcast Anda di sini..."
                className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none resize-none"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                maxLength={4096}
              />
              <p className="text-xs text-[var(--text-muted)] mt-1 text-right">
                {message.length}/4096
              </p>
            </div>

            {result && (
              <div
                className={`p-3 rounded-lg text-sm ${
                  result.success
                    ? "bg-green-500/10 border border-green-500/30 text-green-400"
                    : "bg-red-500/10 border border-red-500/30 text-red-400"
                }`}
              >
                {result.message}
              </div>
            )}

            <button
              type="submit"
              disabled={isSending || !message.trim()}
              className="btn-primary w-full"
            >
              {isSending ? (
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
                  Mengirim...
                </span>
              ) : (
                <>
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
                      d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                    />
                  </svg>
                  Kirim Broadcast
                </>
              )}
            </button>
          </form>

          <div className="mt-6 p-4 rounded-xl bg-[var(--bg-dark)]">
            <h3 className="text-sm font-medium mb-2">💡 Tips</h3>
            <ul className="text-xs text-[var(--text-muted)] space-y-1">
              <li>
                • Gunakan HTML untuk format: &lt;b&gt;bold&lt;/b&gt;,
                &lt;i&gt;italic&lt;/i&gt;
              </li>
              <li>• Pesan dikirim ke semua user yang pernah start bot Anda</li>
              <li>• User yang block bot tidak akan menerima pesan</li>
            </ul>
          </div>
        </div>

        {/* History Section */}
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold mb-4">Riwayat Broadcast</h2>

          {broadcasts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-[var(--text-muted)]">
                Belum ada riwayat broadcast
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {broadcasts.map((bc) => (
                <div key={bc.id} className="p-4 rounded-xl bg-[var(--bg-dark)]">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <span className="text-xs text-[var(--text-muted)]">
                      {formatDate(bc.created_at)}
                    </span>
                    <span className="px-2 py-1 text-xs rounded-lg text-green-400 bg-green-400/10">
                      {bc.recipients_count} penerima
                    </span>
                  </div>
                  <p className="text-sm">{bc.message}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
