"use client";

import { motion, useReducedMotion } from "motion/react";
import { useSyncExternalStore, type ReactNode } from "react";

const subscribeNothing = () => () => {};

/**
 * Gate hydration: selama proses hydration SSR, Framer Motion merender
 * style awal (opacity 0 / translateY) hanya di client sehingga atribut
 * tidak cocok dengan HTML server (React 19 + motion). Komponen motion
 * baru dirender setelah mount (pola kanonik useSyncExternalStore,
 * getSnapshot=true / getServerSnapshot=false) sehingga paint pertama
 * tetap statis tanpa flash.
 */
export function useMounted() {
  return useSyncExternalStore(subscribeNothing, () => true, () => false);
}

export function Reveal({
  children,
  className,
  delay = 0,
  y = 24,
}: {
  children: ReactNode;
  className?: string;
  delay?: number;
  y?: number;
}) {
  const reduce = useReducedMotion();
  const mounted = useMounted();
  if (!mounted) {
    return <div className={className}>{children}</div>;
  }
  return (
    <motion.div
      className={className}
      initial={reduce ? undefined : { opacity: 0, y }}
      whileInView={reduce ? undefined : { opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-70px" }}
      transition={{ duration: 0.6, delay, ease: [0.16, 1, 0.3, 1] as const }}
    >
      {children}
    </motion.div>
  );
}

export function RevealStagger({
  children,
  className,
  step = 0.08,
}: {
  children: ReactNode;
  className?: string;
  step?: number;
}) {
  const reduce = useReducedMotion();
  const mounted = useMounted();
  if (!mounted) {
    return <div className={className}>{children}</div>;
  }
  return (
    <motion.div
      className={className}
      initial={reduce ? undefined : "hidden"}
      whileInView={reduce ? undefined : "show"}
      viewport={{ once: true, margin: "-70px" }}
      variants={
        reduce
          ? undefined
          : {
              hidden: {},
              show: {
                transition: { staggerChildren: step, delayChildren: 0.05 },
              },
            }
      }
    >
      {children}
    </motion.div>
  );
}

export function RevealItem({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  const reduce = useReducedMotion();
  const mounted = useMounted();
  if (!mounted) {
    return <div className={className}>{children}</div>;
  }
  return (
    <motion.div
      className={className}
      variants={
        reduce
          ? undefined
          : {
              hidden: { opacity: 0, y: 22 },
              show: {
                opacity: 1,
                y: 0,
                transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] as const },
              },
            }
      }
    >
      {children}
    </motion.div>
  );
}