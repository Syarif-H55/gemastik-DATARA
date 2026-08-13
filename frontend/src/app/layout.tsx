import type { Metadata } from "next";
import { Geist, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/sonner";

const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains-mono" });

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM",
    template: "%s · DATARA",
  },
  description:
    "Sistem Pendukung Keputusan untuk UMKM Food & Beverage: olah penjualan, HPP, biaya operasional, dan stok menjadi indikator bisnis serta rekomendasi yang terjelaskan.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="id"
      suppressHydrationWarning
      className={cn("h-full", "antialiased", geistSans.variable, jetbrainsMono.variable, "font-sans")}
    >
      <body className="min-h-full flex flex-col">
        {/* DIRECTION CONTRACT · DATARA "Etalase" · seed 0743fc77
        THESIS: corporate clean light SaaS — satu aksen biru korporat di atas kertas putih, dengan jiwa "label harga kedai": angka tabular monospace dan cap status sebagai identitas data.
        OWN-WORLD: kertas putih/off-white, tinta slate gelap, aksen biru tunggal, radius lembut (12px kartu, 8px kontrol), angka JetBrains Mono, badge seperti label & stempel.
        STORY: pemilik UMKM membaca kondisi bisnisnya serapi membaca rekening koran, lalu meninjau rekomendasi dan memutuskan (apply/ignore) dengan percaya diri.
        FIRST VIEWPORT: sidebar putih dengan navigasi biru aktif + dashboard: kartu health score, 4 KPI, area chart tren omzet/laba, bar chart kontribusi kategori.
        FORM: etalase label-harga di kanvas corporate clean (candidate 5, assigned by roll). FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, and DESIGN.md */}
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
          <TooltipProvider>{children}</TooltipProvider>
          <Toaster richColors closeButton />
        </ThemeProvider>
      </body>
    </html>
  );
}