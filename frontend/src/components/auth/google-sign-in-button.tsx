"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import Script from "next/script";
import { saveSession } from "@/lib/auth";
import { loginWithGoogle } from "@/lib/datara";
import type { GoogleCredentialResponse } from "@/types/google-accounts";

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID ?? "";

/**
 * Tombol "Lanjutkan dengan Google" (Google Identity Services).
 *
 * GIS mengembalikan ID token (JWT) di sisi client; token dikirim ke
 * POST /api/v1/auth/google untuk diverifikasi backend (signature, aud, exp)
 * sebelum sesi DATARA dibuat. Backend tetap source of truth.
 */
export function GoogleSignInButton({
  onError,
}: {
  onError?: (message: string) => void;
}) {
  const router = useRouter();
  const buttonRef = React.useRef<HTMLDivElement>(null);
  const [rendered, setRendered] = React.useState(false);
  const busyRef = React.useRef(false);

  const handleCredential = React.useCallback(
    async (response: GoogleCredentialResponse) => {
      if (busyRef.current) return;
      busyRef.current = true;
      try {
        const session = await loginWithGoogle(response.credential);
        saveSession(session);
        router.replace("/dashboard");
      } catch (err) {
        onError?.(err instanceof Error ? err.message : "Gagal masuk dengan Google. Coba lagi.");
      } finally {
        busyRef.current = false;
      }
    },
    [router, onError]
  );

  const initGoogleButton = React.useCallback(() => {
    if (
      rendered ||
      !GOOGLE_CLIENT_ID ||
      !window.google?.accounts ||
      !buttonRef.current
    ) {
      return;
    }
    window.google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID,
      callback: handleCredential,
    });
    window.google.accounts.id.renderButton(buttonRef.current, {
      theme: "outline",
      size: "large",
      text: "continue_with",
      shape: "rectangular",
      width: 320,
    });
    setRendered(true);
  }, [rendered, handleCredential]);

  React.useEffect(() => {
    if (window.google?.accounts) {
      initGoogleButton();
    }
  }, [initGoogleButton]);

  if (!GOOGLE_CLIENT_ID) return null;

  return (
    <>
      <Script
        src="https://accounts.google.com/gsi/client"
        strategy="afterInteractive"
        onLoad={initGoogleButton}
      />
      <div ref={buttonRef} className="flex w-full justify-center" />
    </>
  );
}
