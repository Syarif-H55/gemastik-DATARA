import Link from "next/link";
import { ChartDonut } from "@/components/kira-icons";

export default function Home() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-8 px-6 py-16 text-center">
      <div className="flex items-center gap-3">
        <span className="flex size-12 items-center justify-center rounded-xl bg-foreground text-background">
          <ChartDonut className="size-6" />
        </span>
        <div className="text-left">
          <p className="text-lg font-semibold tracking-tight">KIRA</p>
          <p className="text-sm text-muted-foreground">Dari Data Menjadi Keputusan</p>
        </div>
      </div>

      <div className="max-w-md space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">
          Sistem Pendukung Keputusan untuk UMKM Food & Beverage
        </h1>
        <p className="text-muted-foreground">
          Olah data penjualan, HPP, biaya operasional, dan stok menjadi indikator bisnis serta rekomendasi
          yang terjelaskan.
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <Link
          href="/login"
          className="inline-flex h-10 items-center justify-center rounded-md bg-foreground px-5 text-sm font-medium text-background transition-colors hover:opacity-90"
        >
          Masuk Aplikasi
        </Link>
        <Link
          href="/dashboard"
          className="inline-flex h-10 items-center justify-center rounded-md border border-border bg-transparent px-5 text-sm font-medium transition-colors hover:bg-muted"
        >
          Lihat Demo
        </Link>
      </div>
    </main>
  );
}
