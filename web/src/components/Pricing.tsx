import Link from "next/link";

const plans = [
  {
    name: "Starter",
    price: "Gratis",
    period: "selamanya",
    description: "Untuk pemula yang baru mulai jualan",
    features: [
      "1 Bot Telegram",
      "50 Produk",
      "Unlimited Transaksi",
      "QRIS Payment",
      "Dashboard Basic",
    ],
    cta: "Mulai Gratis",
    popular: false,
  },
  {
    name: "Pro",
    price: "Rp 49K",
    period: "/bulan",
    description: "Untuk seller serius dengan volume tinggi",
    features: [
      "Unlimited Bot",
      "Unlimited Produk",
      "Unlimited Transaksi",
      "QRIS + VA Payment",
      "Dashboard Advanced",
      "Broadcast Massal",
      "Priority Support",
      "Custom Bot Branding",
    ],
    cta: "Upgrade ke Pro",
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "Solusi khusus untuk bisnis besar",
    features: [
      "Semua fitur Pro",
      "API Access",
      "White Label",
      "Dedicated Support",
      "SLA Guarantee",
    ],
    cta: "Hubungi Kami",
    popular: false,
  },
];

export default function Pricing() {
  return (
    <section id="pricing" className="relative py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">
            Harga <span className="gradient-text">Simpel & Transparan</span>
          </h2>
          <p className="text-lg text-[var(--text-secondary)] max-w-2xl mx-auto">
            Tidak ada biaya tersembunyi. Mulai gratis sekarang.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`relative glass-card p-8 ${
                plan.popular ? "border-[var(--color-primary)] scale-105" : ""
              }`}
            >
              {/* Popular Badge */}
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-secondary)] rounded-full text-sm font-medium">
                  Paling Populer
                </div>
              )}

              {/* Plan Name */}
              <h3 className="text-xl font-semibold mb-2">{plan.name}</h3>
              <p className="text-[var(--text-muted)] text-sm mb-4">
                {plan.description}
              </p>

              {/* Price */}
              <div className="mb-6">
                <span className="text-4xl font-bold">{plan.price}</span>
                <span className="text-[var(--text-muted)]">{plan.period}</span>
              </div>

              {/* Features */}
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-3">
                    <svg
                      className="w-5 h-5 text-green-400 flex-shrink-0"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                    <span className="text-[var(--text-secondary)]">
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>

              {/* CTA Button */}
              <Link
                href="/auth/register"
                className={`block text-center w-full ${
                  plan.popular ? "btn-primary" : "btn-secondary"
                }`}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>

        {/* Payment Methods */}
        <div className="mt-16 text-center">
          <p className="text-[var(--text-muted)] mb-4">
            Metode Pembayaran yang Didukung
          </p>
          <div className="flex justify-center gap-6 items-center opacity-60">
            <span className="text-2xl font-bold">QRIS</span>
            <span className="text-xl">BCA</span>
            <span className="text-xl">BNI</span>
            <span className="text-xl">BRI</span>
            <span className="text-xl">Mandiri</span>
          </div>
        </div>
      </div>
    </section>
  );
}
