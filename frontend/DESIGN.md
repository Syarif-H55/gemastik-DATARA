# DESIGN.md — DATARA Frontend

Arah desain final hasil redesign penuh (session 2026-08-13), seed concept **0743fc77** (kandidat ke-5: "label harga / etalase kedai").

## Arah

- **Canvas:** corporate clean light (Linear / Vercel / Stripe, aplikasi bank Indonesia sebagai tolok rasa).
- **Suara desain — "label harga":** angka bisnis ditampilkan seperti label harga etalase: tabular, monospace, presisi; status/cap biru korporat; kartu putih di atas latar abu sangat halus.
- **Aturan mutlak (contract):** `frontend/src/app/layout.tsx` memuat komentar `DIRECTION CONTRACT` sebagai child pertama `<body>`; pertahankan saat mengubah layout.

## Token (src/app/globals.css)

- Primary: `oklch(0.51 0.22 262)` (biru korporat); background `oklch(0.985 0.003 250)`; card `oklch(1 0 0)`; `--radius: 0.75rem`.
- Semantik: `--success`, `--warning`, `--info` (+ `--color-*` di `@theme inline`). Tidak ada danger khusus — pakai red bawaan shadcn.
- Chart: `chart-1..5` = biru, emerald, amber, indigo, sky.
- Font: Geist UI (`--font-geist-sans`) untuk UI; **JetBrains Mono (`--font-jetbrains-mono`) khusus data** — `.tabular-nums` sengaja memaksa JetBrains Mono (suara label harga). `--font-heading` = Geist.
- Komponen baru di-root shadcn via `npx shadcn@latest add` (sudah terpasang: card, badge, alert, select, tabs, slider, progress, sonner, dll).

## Keputusan yang didokumentasikan

- **Transactions** = POS-card bergaya etalase; status/pencet `Bagikan` diberi stamp biru (`bg-primary`), bukan emerald.
- **Forecasting**: KPI tanpa kartu (`bg-muted/40` borderless) agar tidak nested-card; sumbu chart muted, garis label harga.
- **Pricing**: slider target margin `accent-primary`; keputusan memakai shadcn `Select` (bukan toggle custom).
- **Decisions**: teks status seragam; kartu "sebelum → sesudah" datar.
- **Growth**: chip stage aktif `bg-primary text-primary-foreground`.
- **Auth (login/register)**: brand `text-2xl` (rasio tipografi ≥ 2.0 untuk `flat-type-hierarchy`); error **tanpa** `Alert` ber-border (borderless block). **Pengecualian visual yang diminta owner (2026-08-13):** backdrop gradien biru korporat berjalan (`animate-gradient-pan` + blob `blur-3xl` melayang, GPU-friendly, mati saat `prefers-reduced-motion`) dan kartu **glassmorphism** (`bg-white/70 backdrop-blur-2xl border-white/60`, varian dark `bg-white/5`). Komponen: `src/components/auth/auth-backdrop.tsx`; keyframes di `globals.css` (`--animate-*`).
- **Sidebar toggle (desktop)**: saat sidebar terlipat, tombol minimize **berubah menjadi logo DATARA** (kotak biru + ChartDonut, terpusat di rel; logo link memudar agar tidak dobel). Klik logo = perluas sidebar (`aria-label` "Perluas sidebar"). Implementasi: `src/components/layout/app-brand.tsx`.
  - **Bug yang diperbaiki (2026-08-13):** centering tombol saat collapsed semula memakai `-translate-y-1/2`. Variant bawaan shadcn Button `active:translate-y-px` menimpa properti CSS `translate` yang sama saat tombol ditekan → tombol melompat ~17px → klik tidak terdaftar (mouseup jatuh di luar target). Fix: centering dengan auto-margin (`left-0 right-0 mx-auto` + `-mt-4`), tanpa translate. Jangan kembalikan centering berbasis translate pada tombol ini.
  - **Auth gradient & glass di headless:** headless Chrome melaporkan `prefers-reduced-motion: reduce` — animasi sengaja mati di sana (guard berfungsi). Verifikasi animasi memakai `emulateMediaFeatures`.
- **Landing**: `Buttons` (variasi solid/outline) konsisten; tanpa kartu berlapis.
  - **Landing glassmorphism (2026-08-14, overhaul)**: `src/app/page.tsx` ditulis ulang atas permintaan eksplisit owner menjadi **kanvas glassmorphism** (pengecualian dari identitas korporat light, seperti halnya auth): latar memakai **`AuthBackdrop` yang sama persis dengan login/register** (gradien biru korporat light + varian dark navy, blob biru/sky/indigo, `animate-gradient-pan`); semua kontainer = **glassmorphism** `bg-white/60` (light) / `bg-white/10` (dark) `backdrop-blur-xl border-white/60` / `border-white/20` `rounded-3xl shadow-xl` (`src/components/landing/glass-card.tsx`, hover `scale-[1.02]` + border mencerah); navbar pill glass sticky; CTA utama **glowing** (`GlowButton`: span gradien sky→violet→pink `blur-lg` dengan `animate-glow-breathe` di belakang tombol putih). Copy 6 seksi mengikuti brief owner (hero center + CTA "Coba DATARA Sekarang", problem bento 4 sel asimetris `md:grid-cols-3` (1-2/2-1), solusi blok glass besar, fitur bento 6 sel `md:grid-cols-6` (4-2/2-4/3-3), cara kerja timeline 4 langkah dengan garis putus-putus, final CTA "Mulai Gratis Sekarang!"). **Landing mengikuti tema light/dark aplikasi** (teks `text-slate-900`/`dark:text-white`, chip `text-primary`, ikon tile `bg-primary/5 text-primary`, headline gradien `from-sky-600…`/`dark:from-sky-300…`).
  - **Iterasi 2026-08-14 (final)**: landing kini **selalu light** (tidak ikut tema) sesuai permintaan owner: background = **gradien biru-putih persis halaman login** (`MeshBackground` = versi terang `AuthBackdrop` + blob biru/sky/indigo), **teks hitam polos** (`text-black` heading, `text-black/70` paragraf, `text-black/60` muted — tanpa gradien teks), glass card `bg-white/40 border-white/60 shadow-[0_8px_30px_rgb(0,0,0,0.04)]`, **logo resmi `public/logo_DATARA.png`** (PNG 500x500 transparan, mark biru) dipasang di navbar & footer menggantikan tile Sparkle. CTA: `GlowButton` dihapus → `src/components/landing/cta-button.tsx` (Link pill glass: `bg-white/40 backdrop-blur-xl border-white/70 rounded-full px-8 py-3 text-black`, hover `bg-white/60` + shadow halus — **dibuat polos glassmorphism 2026-08-14 setelah owner menilai gradien biru-ungu tidak kontras**; tanpa glow neon; keyframe `glow-breathe` dihapus dari globals.css). Nav CTA = pill solid `bg-slate-900 text-white rounded-full`.
  - **Penyetaraan warna (2026-08-14)**: atas masukan owner, mesh di-kalem: opacity blob turun drastis (blue-500/15, purple-500/10, pink-500/8), radial atas 0.4 → 0.2, hiasan dekoratif di `solution-panel` dan `final-cta` diturunkan (violet/pink ≤ /12) dan glow-nya dibuat statis. Glow tombol CTA (`GlowButton`) dipertahankan karena itu permintaan eksplisit.
  - **Background menyamai halaman auth (2026-08-14)**: atas permintaan owner, landing sempat memakai `AuthBackdrop` langsung (termasuk varian dark) dengan teks `text-slate-900`/`dark:text-white`. **Diubah lagi di iterasi final** (lihat atas): `MeshBackground` dibuat ulang sebagai versi terang-only gradien login + teks hitam polos + logo resmi, sesuai instruksi "biru putih saja + teks hitam polos".
  - **Motion landing v2**: pindah dari CSS scroll-driven ke **Framer Motion** (`motion` package, import `motion/react`) — `Reveal`/`RevealStagger`/`RevealItem` di `src/components/landing/reveal.tsx` (`whileInView` + stagger, `viewport once`, `useReducedMotion` matikan semua). Hero pakai stagger saat mount. Keyframes CSS dipertahankan hanya untuk mesh/glow (`gradient-pan`, `blob-drift-*`, `glow-breathe`); `rise-in`/`landing-reveal` **dihapus**. Konsekuensi: screenshot fullPage perlu scroll-through (semua `whileInView` terpicu) sebelum capture — di `shots.mjs` flag `unreveal` sekarang melakukan scroll bertahap ke bawah halaman.
  - **Fix hydration mismatch (2026-08-14)**: motion v12 + React 19 membuat elemen `motion.*` merender style awal (`opacity:0`/`translateY`) hanya di client → warning "A tree hydrated but some attributes..." di semua seksi landing. Fix: hook `useMounted()` (`src/components/landing/reveal.tsx`) memakai pola kanonik `useSyncExternalStore` (`getSnapshot=true`, `getServerSnapshot=false`); selama hydration elemen motion ditunda → paint pertama statis tanpa flash, animasi jalan normal setelah mount. Ini juga mengatasi `tabindex="0"` yang ditambahkan Motion pada wrapper `GlowButton` (kini hanya setelah hydration). Verifikasi: console browser 0 warning hydration pada path reduced-motion maupun animasi penuh, semua reveal selesai (0 elemen nyangkut di opacity 0).
- **Sidebar collapse** (shadcn): transition `width/height/padding` sengaja dipertahankan (gesture user, satu elemen rail) — **dikecualikan** dari detector `layout-transition` lewat `frontend/.impeccable/config.json` (lihat catatan di bawah). Semua transisi lain memakai properti eksplisit (color/opacity/transform), bukan `transition-all`.

## Detector (skills/impeccable)

- Scan URL: `node "…/impeccable/scripts/detect.mjs" --json --no-advisory <url>`; butuh puppeteer (`C:\Users\raifa aziz\.agents`, system Chrome; `PUPPETEER_SKIP_DOWNLOAD=1` saat install).
- **`frontend/.impeccable/config.json`**: `ignoreRules: ["layout-transition"]` — satu-satunya sumber flag adalah utilitas collapse sidebar (statis di CSS bundle); diverifikasi runtime 2026-08-13 bahwa tidak ada animasi layout lain di aplikasi.
- Hasil scan 12 halaman per 2026-08-13: **0 finding**.

## Bug nyata yang ditemukan & diperbaiki (bonus dari pass verifikasi)

- **`AuthGuard` hydration race** (`src/components/layout/auth-guard.tsx`): pada full page load, `useSyncExternalStore` memakai `getServerSnapshot` (`false`) saat hydration → effect `router.replace("/login")` terpicu walau token ada → halaman login (yang punya efek "sudah authed → /dashboard") melempar user ke /dashboard. Efek: refresh halaman app mana pun selalu berakhir di /dashboard. Diperbaiki dengan gate `hydrated` via `useSyncExternalStore` (pola kanonik; lulus ESLint `react-hooks` baru).

## Catatan teknis verifikasi (2026-08-13)

- Screenshot suite demo memakai puppeteer + request interception (API `localhost:8000` di-respond data demo + header CORS lengkap; token di-`localStorage`; halaman auth tanpa token agar tidak ke-redirect).
- Halaman app di-verifikasi via marker teks + pathname (bukan visual; lihat `C:\Users\RAIFAA~1\AppData\Local\Temp\opencode\shots\*.png`).
- Dev server Next.js 16.3.0 (Turbopack): `npm run dev` di `frontend/`; build + lint bersih.