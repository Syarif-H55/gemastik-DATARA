# AGENTS.md

## Repo state

- Project: **DATARA** ("Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM") — Decision Support System untuk UMKM Food & Beverage skala mikro (kompetisi Gemastik).
- Arsitektur decoupled: **frontend** (Next.js) mengonsumsi REST API dari **backend** (FastAPI + Python + MySQL) yang belum ada di repo ini.
- Requirements spec: **`PRD DATARA.docx.md`** (v1.1, 9 Agustus 2026). Baca sebelum mengubah struktur/feature.
- Frontend (`frontend/`) sudah dapat dijalankan: `npm run dev`. Backend FastAPI belum dibuat.

## Frontend (`frontend/`)

- Stack: Next.js 16 (App Router), React 19, Tailwind CSS v4, shadcn/ui (base radix), TypeScript.
- Ini **Next.js 16** — bukan Next 13–15. Breaking changes: `params`/`searchParams` adalah `Promise` (harus `await`), route type helpers `PageProps`/`LayoutProps` global tersedia. Baca `frontend/node_modules/next/dist/docs/` sebelum menulis kode App Router.
- Jalankan `npm run lint` dan `npm run build` (typecheck) setelah perubahan. Tidak ada test suite.
- Perintah: `npm run dev` (dev), `npm run build`, `npm start`, `npm run lint`.

### Konvensi & gotchas

- **Phosphor icons tidak boleh diimport langsung di Server Component** — pakai `src/components/kira-icons.tsx` (client wrapper) di file SC. File `"use client"` aman mengimpor dari `@phosphor-icons/react`.
- Nama export Phosphor bend: `TrendUp` (bukan `TrendingUp`), `SignOut` (bukan `Sign`), `ArrowsDownUp` (bukan `ArrowUpDown`), `WarningCircle` (bukan `CircleWarning`). Nama lain sering beda tipis dari tebakan — cek `node_modules/@phosphor-icons/react/dist/index.es.js` bila build gagal.
- Jalankan shadcn dengan `npx shadcn@latest add <komponen>` (shadcn v4, base `radix`).
- API FastAPI diakses lewat `frontend/src/lib/api.ts` (base URL dari `NEXT_PUBLIC_API_URL`, default `http://localhost:8000/api`). Kontrak domain di `frontend/src/lib/types.ts`, format Rupiah di `frontend/src/lib/format.ts`.
- **Tidak ada role Staff/Owner terpisah** (per PRD v1.1): satu actor `Pemilik UMKM`. Semua halaman di route group `(app)` dengan satu sidebar (`@/components/layout/app-sidebar.tsx`). Halaman demo memakai mock data di `frontend/src/lib/demo-data.ts`.
- `.env.local` berisi `NEXT_PUBLIC_API_URL`; contoh di `.env.example`.

## Backend (belum ada)

- Belum ada kode backend. Rencana: FastAPI + SQLAlchemy + MySQL, entitas Users/Roles, Products, Inventory_Logs, Transactions, Transaction_Details, Costs, Decisions_Applied (+ dukungan Sales Forecasting & monitoring). Sebelum men-scaffold, pastikan kontrak API konsisten dengan `frontend/src/lib/types.ts`.