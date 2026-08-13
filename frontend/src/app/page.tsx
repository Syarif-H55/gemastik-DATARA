import Link from "next/link";
import { ChartDonut } from "@/components/datara-icons";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-8 px-6 py-16 text-center">
      <div className="flex items-center gap-3">
        <span className="flex size-12 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm">
          <ChartDonut className="size-6" />
        </span>
        <div className="text-left">
          <p className="text-lg font-semibold tracking-tight">DATARA</p>
          <p className="text-sm text-muted-foreground">Dari Data Menjadi Keputusan</p>
        </div>
      </div>

      <div className="max-w-md space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">
          Sistem Pendukung Keputusan untuk UMKM Food &amp; Beverage
        </h1>
        <p className="text-muted-foreground">
          Olah data penjualan, HPP, biaya operasional, dan stok menjadi indikator bisnis serta rekomendasi
          yang terjelaskan.
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <Button asChild size="lg">
          <Link href="/login">Masuk Aplikasi</Link>
        </Button>
        <Button asChild size="lg" variant="outline">
          <Link href="/dashboard">Lihat Demo</Link>
        </Button>
      </div>
    </main>
  );
}