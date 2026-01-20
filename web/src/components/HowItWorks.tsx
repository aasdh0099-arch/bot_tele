const steps = [
  {
    number: "01",
    title: "Daftar Akun Gratis",
    description:
      "Buat akun BotStore dalam 30 detik. Tidak perlu kartu kredit atau verifikasi ribet.",
    icon: (
      <svg
        className="w-10 h-10"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
        />
      </svg>
    ),
  },
  {
    number: "02",
    title: "Buat Bot & Tambah Produk",
    description:
      "Hubungkan bot Telegram Anda, upload produk (kredensial/voucher), atur harga.",
    icon: (
      <svg
        className="w-10 h-10"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
        />
      </svg>
    ),
  },
  {
    number: "03",
    title: "Share & Mulai Jualan!",
    description:
      "Bagikan link bot ke pelanggan. Transaksi otomatis 24/7, cuan mengalir terus!",
    icon: (
      <svg
        className="w-10 h-10"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M13 10V3L4 14h7v7l9-11h-7z"
        />
      </svg>
    ),
  },
];

export default function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="relative py-24 bg-[rgba(15,15,30,0.5)]"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">
            Mulai dalam <span className="gradient-text">3 Langkah Mudah</span>
          </h2>
          <p className="text-lg text-[var(--text-secondary)] max-w-2xl mx-auto">
            Tidak perlu skill coding atau sewa server mahal. Siapapun bisa mulai
            jualan dalam hitungan menit.
          </p>
        </div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-20 left-1/2 w-full h-[2px] bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-secondary)] opacity-30" />
              )}

              <div className="glass-card p-8 text-center relative">
                {/* Step Number */}
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-secondary)] flex items-center justify-center text-sm font-bold">
                  {step.number}
                </div>

                {/* Icon */}
                <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-[var(--color-primary)]/20 to-[var(--color-secondary)]/20 border border-[var(--border-color)] flex items-center justify-center text-[var(--color-primary)] mb-6 mt-4">
                  {step.icon}
                </div>

                <h3 className="text-xl font-semibold mb-3">{step.title}</h3>
                <p className="text-[var(--text-secondary)]">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
