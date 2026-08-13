"use client";

import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

import { Reveal } from "@/components/landing/reveal";

export function SectionHeader({
  chip,
  title,
  sub,
  className,
}: {
  chip: string;
  title: ReactNode;
  sub?: string;
  className?: string;
}) {
  return (
    <Reveal className={cn("mx-auto mb-14 max-w-3xl text-center", className)}>
      <span className="inline-flex items-center gap-2 rounded-full border border-white/60 bg-white/40 px-3 py-1 font-mono text-xs uppercase tracking-widest text-black/60 backdrop-blur-xl">
        {chip}
      </span>
      <h2 className="mt-5 text-3xl font-bold tracking-tight text-black md:text-4xl">
        {title}
      </h2>
      {sub ? (
        <p className="mt-4 text-base leading-relaxed text-black/70 md:text-lg">
          {sub}
        </p>
      ) : null}
    </Reveal>
  );
}