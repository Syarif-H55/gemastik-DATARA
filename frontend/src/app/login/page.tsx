"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { GoogleSignInButton } from "@/components/auth/google-sign-in-button";
import { AuthBackdrop } from "@/components/auth/auth-backdrop";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { login } from "@/lib/datara";
import { saveSession, isAuthenticated } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (isAuthenticated()) {
      router.replace("/dashboard");
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Email dan kata sandi wajib diisi.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const session = await login(email, password);
      saveSession(session);
      router.replace("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gagal masuk. Coba lagi.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-8 px-6 py-16">
      <AuthBackdrop />

      <div className="flex items-center gap-3">
        <img
          src="/logo_DATARA.svg"
          alt="Logo DATARA"
          className="size-10 shrink-0"
        />
        <div className="text-left">
          <p className="text-2xl font-semibold tracking-tight">DATARA</p>
          <p className="text-sm text-muted-foreground">Dari Data Menjadi Keputusan</p>
        </div>
      </div>

      <Card className="w-full max-w-sm border-white/60 bg-white/70 shadow-[0_24px_70px_-24px_rgba(30,64,175,0.4)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/5 dark:shadow-none">
        <CardHeader>
          <CardTitle>Masuk</CardTitle>
          <CardDescription>Masuk sebagai Pemilik UMKM</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="nama@umkm.id"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Kata Sandi</Label>
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {error ? (
              <div className="rounded-lg bg-destructive/10 px-3 py-2 text-xs text-destructive">{error}</div>
            ) : null}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Memeriksa..." : "Masuk"}
            </Button>
          </form>

          <div className="my-4 flex items-center gap-3">
            <div className="h-px flex-1 bg-border" />
            <span className="text-xs text-muted-foreground">atau masuk dengan</span>
            <div className="h-px flex-1 bg-border" />
          </div>

          <GoogleSignInButton onError={setError} />

          <p className="mt-4 text-center text-sm text-muted-foreground">
            Belum punya akun?{" "}
            <Link href="/register" className="font-medium text-foreground underline-offset-4 hover:underline">
              Daftar
            </Link>
          </p>
        </CardContent>
      </Card>
    </main>
  );
}
