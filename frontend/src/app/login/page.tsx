"use client";

import * as React from "react";
import { ChartDonut } from "@/components/kira-icons";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";

export default function LoginPage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-8 px-6 py-16">
      <div className="flex items-center gap-3">
        <span className="flex size-10 items-center justify-center rounded-xl bg-foreground text-background">
          <ChartDonut className="size-5" />
        </span>
        <div className="text-left">
          <p className="text-lg font-semibold tracking-tight">KIRA</p>
          <p className="text-sm text-muted-foreground">Dari Data Menjadi Keputusan</p>
        </div>
      </div>

      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Masuk</CardTitle>
          <CardDescription>Masuk sebagai Pemilik UMKM</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="nama@umkm.id" autoComplete="email" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Kata Sandi</Label>
            <Input id="password" type="password" autoComplete="current-password" />
          </div>

          <Button asChild className="w-full">
            <Link href="/dashboard">Masuk</Link>
          </Button>

          <p className="text-center text-xs text-muted-foreground">
            Demo belum terhubung ke backend. Autentikasi akan dihubungkan ke API FastAPI.
          </p>
        </CardContent>
      </Card>
    </main>
  );
}