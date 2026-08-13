import Link from "next/link";

export function LandingFooter() {
  return (
    <footer className="relative border-t border-slate-900/10 py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 md:flex-row">
        <Link href="/" className="flex items-center gap-2.5">
          <img
            src="/logo_DATARA.svg"
            alt="Logo DATARA"
            className="size-7 shrink-0"
          />
          <span className="font-semibold tracking-tight text-black">
            DATARA
          </span>
        </Link>
        <p className="text-sm text-black/60">
          Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM
        </p>
        <div className="flex items-center gap-5 text-sm text-black/60">
          <Link href="/login" className="transition-colors hover:text-black">
            Masuk
          </Link>
          <Link href="/register" className="transition-colors hover:text-black">
            Daftar
          </Link>
        </div>
      </div>
    </footer>
  );
}