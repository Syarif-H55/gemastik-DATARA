"use client";

import { ArrowRight } from "@/components/datara-icons";
import { CtaButton } from "@/components/landing/cta-button";
import { GlassCard } from "@/components/landing/glass-card";
import { Reveal } from "@/components/landing/reveal";

export function FinalCta() {
  return (
    <section id="daftar" className="mx-auto max-w-6xl scroll-mt-24 px-6 py-24">
      <Reveal>
        <GlassCard className="relative overflow-hidden px-6 py-16 text-center md:py-20">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent"
          />
          <span
            aria-hidden
            className="pointer-events-none absolute left-1/2 top-1/2 size-[32rem] -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-to-r from-blue-400/15 via-sky-400/15 to-indigo-400/15 blur-3xl"
          />
          <div className="relative">
            <h2 className="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-black md:text-4xl">
              Siap Bawa Bisnis F&amp;B Anda Naik Kelas?
            </h2>
            <p className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-black/70 md:text-lg">
              Berhenti mereka-reka strategi. Mulai manfaatkan data Anda secara
              optimal untuk keuntungan maksimal bersama DATARA.
            </p>
            <div className="mt-10 flex justify-center">
              <CtaButton href="/register">
                Mulai Gratis Sekarang!
                <ArrowRight className="size-5" />
              </CtaButton>
            </div>
          </div>
        </GlassCard>
      </Reveal>
    </section>
  );
}