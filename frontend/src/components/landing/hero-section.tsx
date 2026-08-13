"use client";

import { motion, useReducedMotion } from "motion/react";

import { ArrowRight, Sparkle } from "@/components/datara-icons";
import { CtaButton } from "@/components/landing/cta-button";
import { useMounted } from "@/components/landing/reveal";

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.12, delayChildren: 0.1 } },
};

const item = {
  hidden: { opacity: 0, y: 26 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] as const },
  },
};

export function HeroSection() {
  const reduce = useReducedMotion();
  const mounted = useMounted();

  return (
    <section className="flex min-h-[calc(100svh-96px)] flex-col items-center justify-center px-6 pb-24 pt-16 text-center">
      {mounted ? (
        <motion.div
          className="mx-auto flex max-w-4xl flex-col items-center"
          initial={reduce ? undefined : "hidden"}
          animate={reduce ? undefined : "show"}
          variants={container}
        >
          <motion.span
            variants={item}
            className="inline-flex items-center gap-2 rounded-full border border-white/60 bg-white/40 px-3 py-1 font-mono text-xs uppercase tracking-widest text-black/60 backdrop-blur-xl"
          >
            <Sparkle className="size-3.5" />
            DSS untuk UMKM Food &amp; Beverage
          </motion.span>
          <motion.h1
            variants={item}
            className="mt-6 text-4xl font-bold leading-[1.08] tracking-tight text-black sm:text-5xl md:text-6xl lg:text-7xl"
          >
            Tinggalkan Cara Tebak-Tebakan.
            <span className="mt-2 block">
              Ambil Keputusan Bisnis Berdasarkan Data Nyata.
            </span>
          </motion.h1>
          <motion.p
            variants={item}
            className="mt-6 max-w-2xl text-base leading-relaxed text-black/70 md:text-lg"
          >
            DATARA (Data Analitik dan Rekomendasi) hadir untuk membantu
            pemilik UMKM makanan dan minuman skala mikro. Kami mengubah data
            penjualan harian Anda menjadi rekomendasi bisnis yang
            menguntungkan dan mudah dipahami.
          </motion.p>
          <motion.div variants={item} className="mt-10">
            <CtaButton href="/register">
              Coba DATARA Sekarang
              <ArrowRight className="size-5" />
            </CtaButton>
          </motion.div>
        </motion.div>
      ) : (
        <div className="mx-auto flex max-w-4xl flex-col items-center">
          <span className="inline-flex items-center gap-2 rounded-full border border-white/60 bg-white/40 px-3 py-1 font-mono text-xs uppercase tracking-widest text-black/60 backdrop-blur-xl">
            <Sparkle className="size-3.5" />
            DSS untuk UMKM Food &amp; Beverage
          </span>
          <h1 className="mt-6 text-4xl font-bold leading-[1.08] tracking-tight text-black sm:text-5xl md:text-6xl lg:text-7xl">
            Tinggalkan Cara Tebak-Tebakan.
            <span className="mt-2 block">
              Ambil Keputusan Bisnis Berdasarkan Data Nyata.
            </span>
          </h1>
          <p className="mt-6 max-w-2xl text-base leading-relaxed text-black/70 md:text-lg">
            DATARA (Data Analitik dan Rekomendasi) hadir untuk membantu
            pemilik UMKM makanan dan minuman skala mikro. Kami mengubah data
            penjualan harian Anda menjadi rekomendasi bisnis yang
            menguntungkan dan mudah dipahami.
          </p>
          <div className="mt-10">
            <CtaButton href="/register">
              Coba DATARA Sekarang
              <ArrowRight className="size-5" />
            </CtaButton>
          </div>
        </div>
      )}
    </section>
  );
}