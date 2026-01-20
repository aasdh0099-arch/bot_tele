import Link from "next/link";

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      {/* Background Effects */}
      <div className="bg-glow-blob blob-1" />
      <div className="bg-glow-blob blob-2" />
      <div className="absolute inset-0 bg-grid opacity-50" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[var(--bg-card)] border border-[var(--border-color)] mb-8">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse-glow" />
          <span className="text-sm text-[var(--text-secondary)]">
            🎉 Gratis untuk semua pengguna baru!
          </span>
        </div>

        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight mb-6">
          Jualan Produk Digital
          <br />
          <span className="gradient-text animate-gradient">
            via Bot Telegram Otomatis
          </span>
        </h1>

        {/* Subheadline */}
        <p className="text-lg sm:text-xl text-[var(--text-secondary)] max-w-2xl mx-auto mb-10">
          Buat toko online Anda di Telegram dalam hitungan menit. Terima
          pembayaran QRIS dan kirim produk secara instan dan otomatis 24/7.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <Link href="/auth/register" className="btn-primary text-lg">
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
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
            Buat Bot Gratis
          </Link>
          <a href="#how-it-works" className="btn-secondary text-lg">
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
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            Lihat Cara Kerja
          </a>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6 max-w-xl mx-auto">
          <div className="text-center">
            <div className="text-3xl sm:text-4xl font-bold gradient-text">
              500+
            </div>
            <div className="text-sm text-[var(--text-muted)]">Seller Aktif</div>
          </div>
          <div className="text-center">
            <div className="text-3xl sm:text-4xl font-bold gradient-text">
              10K+
            </div>
            <div className="text-sm text-[var(--text-muted)]">
              Transaksi/Bulan
            </div>
          </div>
          <div className="text-center">
            <div className="text-3xl sm:text-4xl font-bold gradient-text">
              99.9%
            </div>
            <div className="text-sm text-[var(--text-muted)]">Uptime</div>
          </div>
        </div>
      </div>

      {/* Bottom Gradient Fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[var(--bg-dark)] to-transparent" />
    </section>
  );
}
