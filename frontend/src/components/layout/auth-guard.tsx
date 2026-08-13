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

function subscribeNothing(): () => void {
  return () => {};
}

function getHydratedSnapshot(): boolean {
  return true;
}

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const hydrated = React.useSyncExternalStore(subscribeNothing, getHydratedSnapshot, () => false);
  const authed = React.useSyncExternalStore(subscribeAuth, getAuthSnapshot, () => false);

  React.useEffect(() => {
    if (hydrated && !authed) {
      router.replace("/login");
    }
  }, [hydrated, authed, router]);

  if (!hydrated || !authed) return null;
  return <>{children}</>;
}
