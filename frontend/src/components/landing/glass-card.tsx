import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export function GlassCard({
  children,
  className,
  hover = true,
}: {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}) {
  return (
    <div
      className={cn(
        "relative rounded-3xl border border-white/60 bg-white/40 shadow-[0_8px_30px_rgb(0,0,0,0.04)] backdrop-blur-xl",
        hover &&
          "transition-all duration-300 ease-out hover:-translate-y-1 hover:scale-[1.02] hover:border-white/80 hover:shadow-[0_12px_40px_rgb(0,0,0,0.08)]",
        className,
      )}
    >
      {children}
    </div>
  );
}