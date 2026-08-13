"use client";

import {
  ArrowUpRight,
  Lightbulb,
  Receipt,
  Target,
} from "@/components/datara-icons";
import { GlassCard } from "@/components/landing/glass-card";
import {
  RevealItem,
  RevealStagger,
} from "@/components/landing/reveal";
import { SectionHeader } from "@/components/landing/section-header";

const steps = [
  {
    icon: Receipt,
    num: "01",
    title: "Input Data Dasar",
    desc: "Masukkan data produk, transaksi harian, biaya, dan stok Anda ke dalam sistem.",
  },
  {
    icon: Lightbulb,
    num: "02",
    title: "Analisis Otomatis",
    desc: "Mesin pintar DATARA akan mengolah data Anda di latar belakang.",
  },
  {
    icon: Target,
    num: "03",
    title: "Terima Rekomendasi",
    desc: "Dapatkan saran konkret (seperti menaikkan harga atau menambah stok) beserta alasannya.",
  },
  {
    icon: ArrowUpRight,
    num: "04",
    title: "Pantau Hasilnya",
    desc: "Terapkan rekomendasi tersebut dan pantau peningkatan profitabilitas usaha Anda langsung dari dasbor.",
  },
];

export function HowItWorks() {
  return (
    <section id="cara-kerja" className="mx-auto max-w-6xl scroll-mt-24 px-6 py-24">
      <SectionHeader
        chip="Cara Kerja"
        title="Bagaimana DATARA Membantu Anda?"
        sub="Empat langkah sederhana, dari data mentah hingga keputusan yang bisa Anda jalankan hari ini."
      />
      <RevealStagger
        step={0.12}
        className="relative grid grid-cols-1 gap-5 md:grid-cols-4"
      >
        <div
          aria-hidden
          className="absolute inset-x-10 top-10 hidden border-t-2 border-dashed border-primary/20 md:block"
        />
        {steps.map((step) => (
          <RevealItem key={step.num}>
            <GlassCard className="flex h-full flex-col gap-4 p-6">
              <div className="flex items-center justify-between">
                <span className="flex size-12 items-center justify-center rounded-2xl border border-primary/10 bg-primary/10 text-primary shadow-inner">
                  <step.icon className="size-5" />
                </span>
                <span className="font-mono text-sm text-black/40">
                  {step.num}
                </span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-black">
                  {step.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-black/70">
                  {step.desc}
                </p>
              </div>
            </GlassCard>
          </RevealItem>
        ))}
      </RevealStagger>
    </section>
  );
}