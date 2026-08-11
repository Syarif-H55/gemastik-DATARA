# AGENTS.md

## Repo state

- Project: **DATARA** ("Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM") — Decision Support System untuk UMKM Food & Beverage skala mikro (kompetisi Gemastik).
- Monorepo decoupled: `frontend/` (Next.js) mengonsumsi REST API `backend/` (FastAPI + SQLAlchemy + Alembic + MySQL). **Backend sudah ada dan berjalan** — jangan anggap belum dibuat.
- Spesifikasi & kontrak ada di `documents/`. Baca dokumen relevan sebelum mengubah struktur/feature. Nama file aktual:
  - `documents/PRD DATARA.docx.md` (v1.2)
  - `documents/DATA_DICTIONARY_AND_DATA_MODEL_DATARA.md` (skema DB)
  - `documents/bussiness-rule-dan-decision-logic.md`
  - `documents/API_CONTRACT_API_SPECIFICATION_DATARA.md`
  - `documents/AI_ML_SPECIFICATION_DATARA.md`, `documents/UI_UX_SPECIFICATION_DATARA.md`, `documents/SYSTEM_ARCHITECTURE_TECHNICAL_SPECIFICATION_DATARA.md`, `documents/AGENT_CONTEXT_AI_DEVELOPMENT_GUIDELINES_DATARA.md`
- **Backend adalah source of truth** untuk semua kalkulasi bisnis (HPP, margin, pricing, restock, forecast, health, growth). LLM/AI hanya menjelaskan hasil — bukan sumber angka, tidak boleh mengubah DB/harga. Urutan prioritas saat dokumen konflik: lihat `backend/AGENTS.md`.
- Satu actor `Pemilik UMKM` (PRD v1.2), tanpa role Staff/Owner terpisah. Catatan: `frontend/src/lib/types.ts` masih mendefinisikan `Role = "owner" | "staff"` — inkonsistensi yang diketahui (lihat `documents/catatan-inkonsistensi-frontend-DATARA.md`).

## Frontend (`frontend/`)

- Stack: Next.js 16 (App Router), React 19, Tailwind CSS v4, shadcn/ui (radix), TypeScript.
- **Ini Next.js 16**, bukan 13–15: `params`/`searchParams` berupa `Promise` (harus `await`), route helpers `PageProps`/`LayoutProps` global. Baca `frontend/node_modules/next/dist/docs/` sebelum menulis kode App Router.
- `frontend/AGENTS.md` **auto-generated oleh `next dev`** — jangan diedit manual.
- Perintah: `npm run dev`, `npm run build` (typecheck), `npm run lint`. Tidak ada test suite; jalankan lint + build setelah perubahan.

### Konvensi & gotchas

- **Phosphor icons tidak boleh diimport langsung di Server Component** — pakai `src/components/datara-icons.tsx` (client wrapper). File `"use client"` aman mengimpor dari `@phosphor-icons/react`.
- Nama export Phosphor bend: `TrendUp` (bukan `TrendingUp`), `SignOut` (bukan `Sign`), `ArrowsDownUp` (bukan `ArrowUpDown`), `WarningCircle` (bukan `CircleWarning`). Nama lain sering beda tipis — cek `node_modules/@phosphor-icons/react/dist/index.es.js` bila build gagal.
- Tambah komponen shadcn dengan `npx shadcn@latest add <komponen>` (base radix).
- API diakses lewat `src/lib/api.ts`: base URL dari `NEXT_PUBLIC_API_URL`, default **`http://localhost:8000/api/v1`** (sudah di `.env.local`). JWT token + user disimpan di localStorage (`datara_token`/`datara_user`, lihat `src/lib/auth.ts`); 401 memicu redirect `/login` (`src/components/layout/auth-guard.tsx`).
- Format Rupiah di `src/lib/format.ts`; mock data demo di `src/lib/demo-data.ts`.

## Backend (`backend/`)

- Stack: FastAPI + SQLAlchemy 2 + Alembic + MySQL (PyMySQL) + Pydantic v2, auth JWT + bcrypt.
- Setup (dari `backend/`): `pip install -r requirements.txt`, salin `.env.example` → `.env` (**wajib** isi `DATABASE_URL` dan `JWT_SECRET` min 32 char), `alembic upgrade head`, lalu `uvicorn app.main:app --reload --port 8000`. OpenAPI di `http://localhost:8000/docs`.
- Test: `pytest` (dari `backend/`). Unit test jalan tanpa DB; test integrasi auto-skip bila MySQL tidak dapat diakses.
- Struktur: `app/main.py`; `app/core/` (config/errors/security); `app/db/` (engine/session); `app/models/` (SQLAlchemy, sesuai Data Dictionary); `app/schemas/` (Pydantic); `app/api/v1/routes/` (rute bisnis); `app/services/` (business logic = source of truth); `app/repositories/` (akses data).
- Endpoint: business API di prefix **`/api/v1`** (daftar router: `app/api/v1/router.py`); health di `/api/health` & `/api/health/db` (di luar versioning). Response envelope `{"success": ..., "data": ...}`, field **snake_case**.
- Auth: JWT Bearer, password bcrypt. Ada endpoint `POST /api/v1/auth/register` (membuat user + business). Seed akun: `python -m scripts.seed_demo_user --email owner@umkm.id --name "Budi" --password <pw> --business "Kedai Contoh"`.
- Migrasi: `alembic revision --autogenerate -m "..."` setelah mengubah model; verifikasi tanpa DB: `alembic upgrade head --sql`.
- Setiap rute business data wajib lewat autentikasi + ownership business — jangan percaya `business_id` dari client (lihat `app/api/deps.py`).
