"use client";

import {
  ChartBar,
  ChartPieSlice,
  Question,
  Warehouse,
} from "@/components/datara-icons";
import { GlassCard } from "@/components/landing/glass-card";
import {
  RevealItem,
  RevealStagger,
} from "@/components/landing/reveal";
import { SectionHeader } from "@/components/landing/section-header";

const problems = [
  {
    icon: ChartBar,
    title: "Harga jual serba salah",
    desc: "Kesulitan menentukan harga jual yang pas karena bingung menghitung Harga Pokok Penjualan (HPP)?",
    span: "md:col-span-1",
  },
  {
    icon: Warehouse,
    title: "Stok hanya perkiraan",
    desc: "Mengelola stok bahan baku hanya mengandalkan perkiraan, sehingga sering kehabisan atau justru menumpuk?",
    span: "md:col-span-2",
  },
  {
    icon: ChartPieSlice,
    title: "Menu yang untung tak jelas",
    desc: "Bingung mengevaluasi menu mana yang sebenarnya paling memberikan keuntungan?",
    span: "md:col-span-2",
  },
  {
    icon: Question,
    title: "Keputusan feeling semata",
    desc: "Risiko keuntungan menurun karena keputusan bisnis masih bergantung pada tebakan atau feeling semata.",
    span: "md:col-span-1",
  },
];

export function ProblemBento() {
  return (
    <section id="masalah" className="mx-auto max-w-6xl scroll-mt-24 px-6 py-24">
      <SectionHeader
        chip="Permasalahan"
        title="Sering Mengalami Kendala Ini di Bisnis Kuliner Anda?"
        sub={'Jika jawabannya sering "ya", Anda tidak sendirian. Masalah ini umum dialami UMKM F&B yang mengelola usahanya tanpa data.'}
      />
      <RevealStagger className="grid grid-cols-1 gap-5 md:grid-cols-3">
        {problems.map((problem) => (
          <RevealItem key={problem.title} className={problem.span}>
            <GlassCard className="flex h-full flex-col gap-4 p-6 md:p-8">
              <span className="flex size-11 items-center justify-center rounded-2xl border border-primary/10 bg-primary/10 text-primary shadow-inner">
                <problem.icon className="size-5" />
              </span>
              <div>
                <h3 className="text-lg font-bold text-black">
                  {problem.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-black/70">
                  {problem.desc}
                </p>
              </div>
            </GlassCard>
          </RevealItem>
        ))}
      </RevealStagger>
    </section>
  );
}