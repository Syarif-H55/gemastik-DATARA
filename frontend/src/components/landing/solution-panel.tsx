"use client";

import { Sparkle } from "@/components/datara-icons";
import { GlassCard } from "@/components/landing/glass-card";
import { Reveal } from "@/components/landing/reveal";

export function SolutionPanel() {
  return (
    <section id="solusi" className="mx-auto max-w-6xl scroll-mt-24 px-6 py-24">
      <Reveal>
        <GlassCard className="relative overflow-hidden p-10 text-center md:p-16">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent"
          />
          <span
            aria-hidden
            className="pointer-events-none absolute -right-24 -top-24 size-64 rounded-full bg-blue-400/15 blur-3xl"
          />
          <span
            aria-hidden
            className="pointer-events-none absolute -bottom-28 -left-24 size-64 rounded-full bg-sky-400/15 blur-3xl"
          />
          <div className="relative">
            <span className="mx-auto flex size-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-600/30">
              <Sparkle className="size-7" />
            </span>
            <h2 className="mx-auto mt-6 max-w-2xl text-3xl font-bold tracking-tight text-black md:text-4xl">
              Kenalkan DATARA: Otak di Balik Pertumbuhan UMKM Anda
            </h2>
            <p className="mx-auto mt-5 max-w-3xl text-base leading-relaxed text-black/70 md:text-lg">
              DATARA bukan sekadar dasbor pencatat biasa. Sistem kami
              menganalisis data penjualan, HPP, biaya, dan persediaan Anda
              untuk memberikan gambaran kesehatan bisnis yang utuh. Hebatnya
              lagi, DATARA tidak membiarkan Anda menafsirkan data sendirian.
              Kami memberikan rekomendasi keputusan bisnis yang jelas, lengkap
              dengan alasan logis dan data pendukung yang transparan.
            </p>
          </div>
        </GlassCard>
      </Reveal>
    </section>
  );
}