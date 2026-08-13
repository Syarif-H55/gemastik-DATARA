"use client";

import {
  Calculator,
  ChartLine,
  Gauge,
  MapTrifold,
  SealCheck,
  TrendUp,
} from "@/components/datara-icons";
import { GlassCard } from "@/components/landing/glass-card";
import {
  RevealItem,
  RevealStagger,
} from "@/components/landing/reveal";
import { SectionHeader } from "@/components/landing/section-header";

const features = [
  {
    icon: Gauge,
    title: "Business Dashboard",
    desc: "Pantau omzet, laba, HPP, margin, jumlah transaksi, dan indikator kesehatan bisnis Anda dalam satu layar interaktif.",
    span: "md:col-span-4",
  },
  {
    icon: TrendUp,
    title: "Product Profitability",
    desc: "Identifikasi dengan cepat produk mana yang paling menguntungkan, memiliki potensi berkembang, atau justru perlu segera dievaluasi.",
    span: "md:col-span-2",
  },
  {
    icon: Calculator,
    title: "Smart Pricing",
    desc: "Jangan salah kasih harga! Dapatkan rekomendasi harga jual terbaik yang dihitung otomatis berdasarkan HPP, biaya operasional, target margin, dan performa penjualan.",
    span: "md:col-span-2",
  },
  {
    icon: ChartLine,
    title: "Sales Forecasting & Smart Restock",
    desc: "Sistem akan memprediksi penjualan Anda ke depan dan memberikan rekomendasi kapan serta berapa banyak stok yang harus ditambah.",
    span: "md:col-span-4",
  },
  {
    icon: SealCheck,
    title: "Decision Engine",
    desc: "Terima rekomendasi tindakan yang bisa dijelaskan (Explainable Recommendation). Anda akan selalu tahu mengapa sebuah keputusan disarankan oleh sistem.",
    span: "md:col-span-3",
  },
  {
    icon: MapTrifold,
    title: "Roadmap & Monitoring",
    desc: "Pantau pergerakan indikator bisnis Anda setelah menerapkan sebuah keputusan, dan dapatkan arah menuju target pertumbuhan usaha selanjutnya.",
    span: "md:col-span-3",
  },
];

export function FeaturesBento() {
  return (
    <section id="fitur" className="mx-auto max-w-6xl scroll-mt-24 px-6 py-24">
      <SectionHeader
        chip="Fitur"
        title="Fitur Cerdas untuk Mendongkrak Profit Anda"
        sub="Enam kemampuan inti yang bekerja bersama: dari memantau angka harian hingga memberi tahu langkah selanjutnya."
      />
      <RevealStagger
        step={0.09}
        className="grid grid-cols-1 gap-5 md:grid-cols-6"
      >
        {features.map((feature) => (
          <RevealItem key={feature.title} className={feature.span}>
            <GlassCard className="flex h-full flex-col gap-4 p-6 md:p-8">
              <span className="flex size-11 items-center justify-center rounded-2xl border border-primary/10 bg-primary/10 text-primary shadow-inner">
                <feature.icon className="size-5" />
              </span>
              <div>
                <h3 className="text-lg font-bold text-black">
                  {feature.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-black/70">
                  {feature.desc}
                </p>
              </div>
            </GlassCard>
          </RevealItem>
        ))}
      </RevealStagger>
    </section>
  );
}