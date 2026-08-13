import Image from "next/image";
import Link from "next/link";

const links = [
  { href: "#masalah", label: "Masalah" },
  { href: "#solusi", label: "Solusi" },
  { href: "#fitur", label: "Fitur" },
  { href: "#cara-kerja", label: "Cara Kerja" },
];

export function LandingNav() {
  return (
    <header className="sticky top-4 z-50 px-4">
      <nav className="mx-auto flex max-w-6xl items-center justify-between rounded-2xl border border-white/60 bg-white/40 px-4 py-3 shadow-[0_8px_30px_rgb(0,0,0,0.04)] backdrop-blur-xl">
        <Link href="/" className="flex items-center gap-2.5">
          <Image
            src="/logo_DATARA.png"
            alt="Logo DATARA"
            width={500}
            height={500}
            sizes="32px"
            className="size-8 shrink-0"
          />
          <span className="font-semibold tracking-tight text-black">
            DATARA
          </span>
        </Link>
        <div className="hidden items-center gap-1 md:flex">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="rounded-lg px-3 py-1.5 text-sm text-black/70 transition-colors hover:bg-white/60 hover:text-black"
            >
              {link.label}
            </Link>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/login"
            className="rounded-lg px-3 py-1.5 text-sm font-medium text-black/70 transition-colors hover:bg-white/60 hover:text-black"
          >
            Masuk
          </Link>
          <Link
            href="/register"
            className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-all duration-300 hover:bg-slate-800 hover:shadow-md"
          >
            Coba DATARA
          </Link>
        </div>
      </nav>
    </header>
  );
}