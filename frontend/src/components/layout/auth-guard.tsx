"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";

function subscribeAuth(callback: () => void): () => void {
  window.addEventListener("storage", callback);
  return () => window.removeEventListener("storage", callback);
}

function getAuthSnapshot(): boolean {
  return isAuthenticated();
}

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const authed = React.useSyncExternalStore(subscribeAuth, getAuthSnapshot, () => false);

  React.useEffect(() => {
    if (!authed) {
      router.replace("/login");
    }
  }, [authed, router]);

  if (!authed) return null;
  return <>{children}</>;
}
