import Link from "next/link";
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export function CtaButton({
  href,
  children,
  className,
}: {
  href: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <Link
      href={href}
      className={cn(
        "group inline-flex items-center gap-2 rounded-full border border-white/70 bg-white/40 px-8 py-3 font-semibold text-black shadow-[0_8px_30px_rgb(0,0,0,0.04)] backdrop-blur-xl transition-all duration-300 hover:border-white/90 hover:bg-white/60 hover:shadow-[0_12px_40px_rgb(0,0,0,0.08)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 active:scale-95",
        className,
      )}
    >
      {children}
    </Link>
  );
}