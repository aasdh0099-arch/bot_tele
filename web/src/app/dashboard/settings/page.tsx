"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth";

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState("profile");
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  const [profile, setProfile] = useState({
    name: "",
    email: "",
    phone: "",
    telegram_id: "",
  });

  const [passwords, setPasswords] = useState({
    current: "",
    new: "",
    confirm: "",
  });

  useEffect(() => {
    if (user) {
      setProfile({
        name: user.name || "",
        email: user.email || "",
        phone: "",
        telegram_id: "",
      });
    }
  }, [user]);

  const tabs = [
    { id: "profile", name: "Profil", icon: "👤" },
    { id: "payment", name: "Payment", icon: "💳" },
    { id: "notifications", name: "Notifikasi", icon: "🔔" },
    { id: "security", name: "Keamanan", icon: "🔒" },
  ];

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setMessage(null);

    // TODO: Implement profile update API
    await new Promise((resolve) => setTimeout(resolve, 500));

    setMessage({ type: "success", text: "Profil berhasil disimpan" });
    setIsSaving(false);
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setMessage(null);

    if (passwords.new !== passwords.confirm) {
      setMessage({ type: "error", text: "Password baru tidak sama" });
      setIsSaving(false);
      return;
    }

    // TODO: Implement password change API
    await new Promise((resolve) => setTimeout(resolve, 500));

    setMessage({ type: "success", text: "Password berhasil diubah" });
    setPasswords({ current: "", new: "", confirm: "" });
    setIsSaving(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Pengaturan</h1>
        <p className="text-[var(--text-muted)]">
          Kelola akun dan preferensi Anda
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Tabs */}
        <div className="glass-card p-4 lg:col-span-1 h-fit">
          <nav className="space-y-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setMessage(null);
                }}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-colors ${
                  activeTab === tab.id
                    ? "bg-[var(--color-primary)] text-white"
                    : "hover:bg-[var(--bg-dark)] text-[var(--text-muted)]"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="glass-card p-6 lg:col-span-3">
          {message && (
            <div
              className={`mb-4 p-3 rounded-lg text-sm ${
                message.type === "success"
                  ? "bg-green-500/10 border border-green-500/30 text-green-400"
                  : "bg-red-500/10 border border-red-500/30 text-red-400"
              }`}
            >
              {message.text}
            </div>
          )}

          {/* Profile Tab */}
          {activeTab === "profile" && (
            <div>
              <h2 className="text-lg font-semibold mb-6">Informasi Profil</h2>

              <div className="flex items-center gap-4 mb-6">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-secondary)] flex items-center justify-center text-white text-2xl font-bold">
                  {profile.name?.charAt(0)?.toUpperCase() || "U"}
                </div>
                <button className="btn-secondary">Ganti Foto</button>
              </div>

              <form onSubmit={handleProfileSave} className="space-y-4 max-w-lg">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Nama Lengkap
                    </label>
                    <input
                      type="text"
                      className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                      value={profile.name}
                      onChange={(e) =>
                        setProfile({ ...profile, name: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none opacity-50"
                      value={profile.email}
                      disabled
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      No. Telepon
                    </label>
                    <input
                      type="tel"
                      placeholder="+62 812 3456 7890"
                      className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                      value={profile.phone}
                      onChange={(e) =>
                        setProfile({ ...profile, phone: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Telegram ID
                    </label>
                    <input
                      type="text"
                      placeholder="@username"
                      className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                      value={profile.telegram_id}
                      onChange={(e) =>
                        setProfile({ ...profile, telegram_id: e.target.value })
                      }
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn-primary"
                  disabled={isSaving}
                >
                  {isSaving ? "Menyimpan..." : "Simpan Perubahan"}
                </button>
              </form>
            </div>
          )}

          {/* Payment Tab */}
          {activeTab === "payment" && (
            <div>
              <h2 className="text-lg font-semibold mb-6">Pengaturan Payment</h2>
              <p className="text-[var(--text-muted)] mb-6">
                Hubungkan akun Pakasir Anda untuk menerima pembayaran QRIS
              </p>

              <form className="space-y-4 max-w-lg">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Pakasir Project Slug
                  </label>
                  <input
                    type="text"
                    placeholder="my-store"
                    className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                  />
                  <p className="text-xs text-[var(--text-muted)] mt-1">
                    Dapatkan dari dashboard Pakasir
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Pakasir API Key
                  </label>
                  <input
                    type="password"
                    placeholder="••••••••••••••••"
                    className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                  />
                </div>

                <button type="submit" className="btn-primary">
                  Simpan Konfigurasi
                </button>
              </form>
            </div>
          )}

          {/* Notifications Tab */}
          {activeTab === "notifications" && (
            <div>
              <h2 className="text-lg font-semibold mb-6">Notifikasi</h2>

              <div className="space-y-4 max-w-lg">
                {[
                  {
                    id: "new_order",
                    label: "Order Baru",
                    desc: "Notifikasi saat ada order masuk",
                  },
                  {
                    id: "payment",
                    label: "Pembayaran",
                    desc: "Notifikasi saat pembayaran sukses",
                  },
                  {
                    id: "low_stock",
                    label: "Stock Habis",
                    desc: "Peringatan saat stock menipis",
                  },
                ].map((item) => (
                  <div
                    key={item.id}
                    className="flex items-center justify-between p-4 rounded-xl bg-[var(--bg-dark)]"
                  >
                    <div>
                      <p className="font-medium">{item.label}</p>
                      <p className="text-sm text-[var(--text-muted)]">
                        {item.desc}
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        className="sr-only peer"
                        defaultChecked
                      />
                      <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--color-primary)]"></div>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === "security" && (
            <div>
              <h2 className="text-lg font-semibold mb-6">Keamanan</h2>

              <form
                onSubmit={handlePasswordChange}
                className="space-y-4 max-w-lg"
              >
                <h3 className="font-medium">Ganti Password</h3>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Password Lama
                  </label>
                  <input
                    type="password"
                    required
                    className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                    value={passwords.current}
                    onChange={(e) =>
                      setPasswords({ ...passwords, current: e.target.value })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Password Baru
                  </label>
                  <input
                    type="password"
                    required
                    className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                    value={passwords.new}
                    onChange={(e) =>
                      setPasswords({ ...passwords, new: e.target.value })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Konfirmasi Password Baru
                  </label>
                  <input
                    type="password"
                    required
                    className="w-full px-4 py-3 rounded-xl bg-[var(--bg-dark)] border border-[var(--border-color)] focus:border-[var(--color-primary)] focus:outline-none"
                    value={passwords.confirm}
                    onChange={(e) =>
                      setPasswords({ ...passwords, confirm: e.target.value })
                    }
                  />
                </div>

                <button
                  type="submit"
                  className="btn-primary"
                  disabled={isSaving}
                >
                  {isSaving ? "Mengubah..." : "Ganti Password"}
                </button>
              </form>

              <hr className="my-8 border-[var(--border-color)]" />

              <div>
                <h3 className="font-medium text-red-400 mb-4">Zona Bahaya</h3>
                <button
                  onClick={() => logout()}
                  className="px-4 py-2 rounded-xl border border-red-500/30 text-red-400 hover:bg-red-500/10 transition-colors"
                >
                  Logout dari Akun
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
