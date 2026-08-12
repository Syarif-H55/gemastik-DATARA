# Laporan Backend DATARA — Integration & Hardening (TASK 13)

> Konteks tunggal hasil verifikasi akhir backend DATARA per `documents/Task-backend.md` TASK 13.
> Metode: audit kode (`c8e63d6`, `d954ef9`) + `pytest` + live smoke test (uvicorn + MySQL lokal).
> Tanggal verifikasi: 12 Agustus 2026.

---

## Implemented

Backend lengkap (FastAPI + SQLAlchemy 2 + Alembic + MySQL) dengan domain:

| Domain | Endpoint | Status |
| --- | --- | --- |
| Auth & Business Isolation | `/auth/*` (register, login, google, me, logout), `GET /business` | ✅ |
| Products, Costs, HPP | `/products`, `/products/{id}`, `/products/{id}/costs`, `/products/profitability` | ✅ |
| Transactions & Inventory | `/transactions` (+ `/transactions/{transaction_id}` detail), `/inventory`, `/inventory/movements` | ✅ |
| Finance | `/finance/summary`, `/finance/expenses` (CRUD) | ✅ |
| Dashboard | `/dashboard` | ✅ |
| Smart Pricing | `/pricing/recommendations`, `/pricing/apply`, `/pricing/dismiss` | ✅ |
| Forecasting | `/forecasting/products`, `/forecasting/products/{id}`, `/forecasting/refresh` | ✅ |
| Smart Restock | `/restock/recommendations`, `/restock/apply`, `/restock/dismiss` | ✅ |
| Decision Recording & Monitoring | `/decisions`, `/decisions/{id}`, `/decisions/{id}/apply`, `/decisions/{id}/dismiss` | ✅ |
| Growth Map | `/growth` | ✅ |
| Business Assistant AI | `/ai/chat`, `/ai/conversations` | ✅ |
| Health | `/api/health`, `/api/health/db` | ✅ |

Gap kontrak yang ditutup di Fase B:
- `GET /transactions/{transaction_id}` — detail transaksi.
- `CRUD /finance/expenses` — routing + `expense_repository.py` + `expense_service.py`.
- `POST /forecasting/refresh` — recompute forecast.
- `POST /decisions/{decision_id}/apply` — apply decision secara atomic.

Gap task yang ditutup di Fase B:
- `inventory_movements.stock_after` (migrasi `70b0ef316b99`), laporan stok per movement tidak lagi membaca current stock.
- Label "Cukup" dihapus; business tanpa data → `INSUFFICIENT_DATA` (dashboard tidak lagi `BERISIKO` saat data kosong).
- Forecasting: kombinasi Simple Average + Moving Average + Exponential Smoothing, confidence dinamis (tidak hardcode 76/88).
- `dismiss` decision di-persist; monitoring pasca-keputusan → `UNKNOWN`/limited saat belum ada data (enum `c4a1b2d3e5f6`).
- Growth Map menghasilkan status `next` (tidak hanya done/current/upcoming).

## Verified

- **pytest backend:** `67 passed` (unit auth, integrasi auth auto-run karena MySQL tersedia, models, health, config, business_logic_pure, pricing/restock deterministik).
- **Compile check:** `python -m compileall -q app scripts tests` → OK.
- **Smoke test live (uvicorn :8000):**
  - `GET /api/health` → `200 {"success":true,"status":"ok"}`.
  - `GET /api/health/db` → `200 {"success":true,"database":"connected"}`.
  - OpenAPI `/openapi.json` memuat seluruh endpoint di atas termasuk 4 kontrak baru.
  - Tanpa token: `/products` → `401` (auth guard bekerja).
  - Register + login: envelope `{"success":true,"data":{...}}`, `access_token` valid.
  - Empty-state business: dashboard `business_health.status=INSUFFICIENT_DATA`, products/forecast/transactions empty array; growth stages `current → next → upcoming → upcoming`.
- **Hygiene:** 60 `.pyc` ter-track sudah dihapus dari git; `git status` bersih setelah verifikasi.
- **Envelope & casing:** semua response `{"success", "data"}` dengan field snake_case.

## Remaining

- Frontend belum diverifikasi terhadap kontrak final (lint/build frontend di luar scope Fase D ini; frontend dikerjakan terpisah — lihat `laporan-frontend-DATARA.md`).
- `pricing/apply`, `restock/apply`, `decisions/{id}/apply` di-smoke hanya melalui OpenAPI (keberadaan route), belum uji end-to-end dengan data produk nyata.
- Test integrasi MySQL tersedia di `tests/` dan auto-run bila DB bisa diakses; disarankan dijalankan di environment CI dengan DB terisolasi.
- Hasil smoke register membentuk data test `smoketest@datara.local` di DB lokal — dapat dihapus bila tidak diinginkan.

## Potential Risks

- **Consistency model Decision**: kolom `decision_applied.status` kini memiliki nilai `UNKNOWN` hasil keputusan desain Fase B — pastikan frontend `types.ts` mengenali status tersebut.
- **Role enum inkonsisten**: `frontend/src/lib/types.ts` masih mendefinisikan `Role = "owner" | "staff"` sedangkan PRD v1.2 hanya satu actor (`Pemilik UMKM`). Tidak memengaruhi backend, tapi perlu diselaraskan di frontend.
- **Deprecation warning**: `starlette.testclient` menyarankan `httpx2` (warning saat pytest) — minor, non-blokir.
- **Forecast & monitoring** bergantung pada kualitas data aktual; status `UNKNOWN`/confidence rendah akan sering muncul pada UMKM baru dengan sedikit transaksi — perilaku yang diharapkan, bukan bug.