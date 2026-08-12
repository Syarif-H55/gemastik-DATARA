# Laporan Perkembangan Backend DATARA (per Task)

> Status development backend DATARA per 12 Agustus 2026, dipetakan terhadap
> seluruh 14 task di `documents/Task-backend.md`.
> Ditinjau dari: audit kode langsung (services/routes/models/migrations),
> history `git`, `/openapi.json` (smoke test), dan hasil `pytest`.

---

## 1. Rangkuman Eksekutif

| Task | Nama | Status | Catatan |
| --- | --- | --- | --- |
| 01 | Backend Foundation | ✅ Selesai | Commit `1192e02` |
| 02 | Database Models & Migration | ✅ Selesai | 19 model, 5 migrasi |
| 03 | Auth & Business Isolation | ✅ Selesai | Commit `bed23c2` + Google Sign-In |
| 04 | Products, Costs & HPP | ✅ Selesai | `catalog_service.py` |
| 05 | Transactions & Inventory | ✅ Selesai | Sale atomic ✓, `stock_after` ✓; movement type selaras kontrak |
| 06 | Dashboard & Profitability | ✅ Selesai | `INSUFFICIENT_DATA`, label demo dihapus |
| 07 | Smart Pricing | ✅ Selesai | Test deterministik ✓ |
| 08 | Sales Forecasting | ✅ Selesai | 3 metode + confidence dinamis |
| 09 | Smart Restock | ✅ Selesai | Test deterministik ✓ |
| 10 | Decision Recording | ✅ Selesai | Apply & dismiss PENDING/APPLIED ✓ |
| 11 | Decision Monitoring | ✅ Selesai | `UNKNOWN` bila belum ada data pasca-keputusan |
| 12 | Growth Map | ✅ Selesai | Status `next` sudah dihasilkan |
| 13 | Integration & Hardening | ✅ Selesai | 4 endpoint kontrak baru; laporan khusus terpisah |
| 14 | Business Assistant AI | ✅ Selesai | Provider-agnostic + context injection |

Tidak ada task yang ❌ (belum dikerjakan). Dua status ⚠️ adalah gap kecil/desain
yang perlu keputusan tim (detail di bagian 6).

**Angka kunci:** 85 test lulus · 0 test gagal · 4 endpoint kontrak baru ditutup ·
0 `.pyc` ter-track · smoke test `/api/health` & `/api/health/db` = `200 connected`.

---

## 2. Riwayat Commit → Fase Task

| Commit | Tanggal | Isi | Fase |
| --- | --- | --- | --- |
| `1192e02` | 2026-08-11 | Implementasi Fondasi Backend & Pembuatan Model Database | T01–T02 |
| `bed23c2` | 2026-08-11 | Implementasi Login Authentication & Business Isolation | T03 (+T04/05 partial) |
| `b856287` | 2026-08-11 | Integrasi frontend dengan backend API + rebranding KIRA → DATARA | Integrasi |
| `1712b97` | 2026-08-12 | Google Sign-In, AI Assistant context injection, UI Keputusan & Monitoring | T03/T14 |
| `c8e63d6` | 2026-08-12 | Tutup gap task & kontrak (Fase B) | T05/06/08/10/11/12/13 |
| `d954ef9` | 2026-08-12 | Test deterministik business logic (Fase C) | T07/09 |

Pemetaan task 01–14 tidak 1:1 dengan commit; sebagian besar domain (T04–T12)
diimplementasikan bertahap di `1192e02`–`1712b97` dan **disempurnakan** pada
commit `c8e63d6` yang menutup gap terhadap Task & API Contract.

---

## 3. Detail Per-Task

### TASK 01 — Backend Foundation ✅

- **Struktur lengkap** `backend/app/`: `core/` (config, errors, exceptions, security),
  `db/` (base, base_models, session), `models/`, `schemas/`, `api/`, `services/`,
  `repositories/`.
- **FastAPI app** `app/main.py`: CORS, exception handlers, router mount.
- **Config berbasis env** (`app/core/config.py`): `DATABASE_URL`, `JWT_SECRET`,
  `CORS_ORIGINS`, LLM & Google OAuth — tidak ada kredensial di source code.
- **Health check** di luar versioning: `GET /api/health` (200 = ok),
  `GET /api/health/db` (200 connected / 503).
- **Envelope konsisten**: `{"success": true, "data": {...}}`, field snake_case.
- Verifikasi: smoke test live → `200 {"success":true,"status":"ok"}`.

### TASK 02 — Database Models & Migration ✅

- **19 file model** SQLAlchemy, sesuai Data Dictionary: User, Business,
  BusinessConfiguration, BusinessTarget, Product, ProductCost, InventoryItem,
  InventoryMovement, OperatingExpense, SalesTransaction (+ item), Pricing/ Restock/
  Forecast/ GrowthRecommendation, DecisionApplied, BusinessHealthAssessment,
  AIConversation/AIMessage.
- **5 migrasi Alembic** (`backend/alembic/versions/`):
  - `edb68b91a3a6` — initial schema DATARA MVP
  - `b0c48013c53e` — foreign key constraints
  - `70b0ef316b99` — `stock_after` di inventory_movements
  - `8f4a2c1e5d90` — kolom `reason` di restock_recommendations
  - `c4a1b2d3e5f6` — tambah `UNKNOWN` ke decision_applied status
- **Numeric untuk uang** (tidak floating point di DB): `Numeric(12,2)` untuk
  harga/quantity.
- **Enum terpusat** di `app/models/enums.py` (MovementType, CostType, HealthStatus,
  DecisionAppliedStatus, dll).

### TASK 03 — Auth & Business Isolation ✅

- **Register** (membuat user + business + BusinessConfiguration default),
  **login**, **logout**, **me** (`GET /auth/me`), **Google Sign-In**
  (`POST /auth/google`, ID token diverifikasi backend).
- **Password bcrypt** (`app/core/security.py`) — tidak pernah plaintext, tidak
  dikembalikan di response.
- **JWT Bearer stateless**; dependency `get_current_business` di
  `app/api/deps.py` memvalidasi ownership di server-side — `business_id` dari
  client **tidak dipercaya**.
- Verifikasi: 13 test unit + 10 test integrasi auth (semua lulus); smoke test
  tanpa token → `401`.

### TASK 04 — Products, Costs & HPP ✅

- `app/services/catalog_service.py`:
  - CRUD product (`list`, `get`, `update`, create, deactivate).
  - `compute_unit_hpp` = Bahan Baku + Kemasan + TKL + Overhead Produksi alokasi
    (per unit). Beban tetap (sewa/gaji/administrasi) **terpisah** ke Operating Expense.
  - `costs` read/update per 4 komponen; quick-add HPP tunggal dipetakan ke Raw Material.
  - Profitability per produk dari transaksi aktual 30 hari (`get_profitability`).
- Response produk menyediakan `id, name, sku, selling_price, hpp, stock,
  low_stock_threshold, is_active, created_at, updated_at`.
- Router: `/products`, `/products/{id}`, `/products/{id}/costs`, `/products/profitability`.

### TASK 05 — Transactions & Inventory ⚠️ Sebagian

**Sudah benar:**
- Sale **atomic** (`transaction_service.create_sale`): validasi produk & stok →
  buat transaksi+item → snapshot HPP → movement SALE + kurangi stock → satu commit.
  Rollback penuh bila gagal (ErrorHandler).
- Stok tidak pernah negatif: `new_stock = max(0.0, current - qty)`; stok tidak
  cukup → transaksi ditolak (BusinessError).
- **`stock_after` kini tersimpan** per movement (migrasi `70b0ef316b99`) — sale,
  received, adjustment, dan restock (via apply) semuanya mengisi `stock_after`;
  `list_movements` membaca kolom tersebut (koreksi gap lama yang membaca current stock).
- Menambahinventory: `POST /inventory` (received/waste/adjustment).
- Detail transaksi `GET /transactions/{transaction_id}` + list `GET /transactions`.

**Gap / perlu keputusan (status ⚠️):**
- **Movement type mismatch**: TASK 05 mensyaratkan `received/issued/adjustment/sale`,
  sedangkan enum kode adalah `RESTOCK/WASTE/ADJUSTMENT/SALE` (lihat bagian 6).
- EOF: kolom `inventory_movements.stock_after` belum ada sebelum migrasi ini —
  perlu dipastikan DB produksi sudah `alembic upgrade head`.

### TASK 06 — Dashboard & Profitability ✅

- `analytics_service.py`:
  - Dashboard: `total_revenue, total_profit, total_cogs, avg_margin_percent,
    transactions_count, products_sold, business_health, revenue_trend (7 hari),
    category_breakdown`.
  - Finance summary: revenue, cogs, gross_profit, gross_margin, operating_expense,
    net_profit (30 hari).
  - Business Health: `SEHAT / PERLU_PERHATIAN / BERISIKO` **dan** `INSUFFICIENT_DATA`
    bila `tx_count == 0` — label demo lama ("Cukup") sudah dihapus.
- Profitability per produk: `unit_profit, margin_percent, qty_sold, total_revenue,
  total_cost, total_profit` dari data transaksi **aktual**, bukan demo.
- **Periode dinamis** (datetime.now()), bukan hardcode Juni 2025.
- Verifikasi smoke test: business kosong → `status: "INSUFFICIENT_DATA"`.

### TASK 07 — Smart Pricing ✅

- `pricing_service.py`: rekomendasi `HPP ÷ (1 − target_margin)` dibulatkan ke
  kelipatan Rp 500; tetap profit; tanda `margin_below_target`, `already_healthy`,
  `incomplete_hpp` (HPP belum lengkap → tidak paksa harga).
- Rekomendasi **tidak mengubah harga** — perubahan hanya lewat `/pricing/apply`.
- Router: `GET/POST /pricing/recommendations`, `POST /pricing/apply`,
  `POST /pricing/dismiss`.
- Test deterministik: `tests/test_pricing_restock_deterministic.py` (11 test) +
  evaluasi harga per produk di context AI Assistant.

### TASK 08 — Sales Forecasting ✅

- `forecasting_service.py`: kombinasi **Simple Average / Moving Average /
  Exponential Smoothing** dipilih berdasar kecukupan data dalam jendela 14 hari:
  - 0 hari terisi → `INSUFFICIENT` (prediksi 0, confidence rendah)
  - 1–6 hari → Simple Average (LOW)
  - 7–13 hari → Moving Average (MEDIUM)
  - ≥14 hari → Exponential Smoothing (HIGH, alpha 0.3)
- **Confidence dinamis** dari volume + stabilitas (coefficient of variation) —
  **tidak** hardcode 76/88 seperti demo. Range 5–92.
- Output: `model, method, next_period, predicted_units, confidence, trend, points,
  reasoning`, `status` (sudah ditambahkan).
- Router: `/forecasting/products`, `/forecasting/products/{id}`, dan
  **`POST /forecasting/refresh`** (persist ke `forecast_results`, gap kontrak ditutup).

### TASK 09 — Smart Restock ✅

- `restock_service.py`: `Forecast Demand + Current Stock + Safety Days (default 3)
  + Lead Time`. Urgency `critical / low / healthy`; `suggested_quantity` dijamin
  bukan negatif.
- Rekomendasi **tidak menambah stok** — perubahan hanya lewat `/restock/apply`.
- Configurable via `BusinessConfiguration` (safety_days/lead_time/target_margin).
- Router: `/restock/recommendations`, `/restock/apply`, `/restock/dismiss`.
- Test deterministik: `test_pricing_restock_deterministic.py`.

### TASK 10 — Decision Recording ⚠️ Sebagian

**Sudah benar:**
- Apply pricing: record decision + update harga, **atomic** — git `ConflictError`
  bila rekomendasi bukan PENDING (anti duplicate).
- Apply restock: record decision + movement RESTOCK + naikkan stok, **atomic**.
- Dismiss rekomendasi (pricing/restock) di-**persist** ke status `DISMISSED`
  (`dismiss_pricing`/`dismiss_restock`).
- Router: `/decisions`, `/decisions/{id}`, `/decisions/{id}/apply` (gap kontrak
  ditutup), `/decisions/{id}/dismiss`.

**Gap / desain (status ⚠️):**
- `POST /decisions/{id}/dismiss` **menolak hard** (`ConflictError`) pada decision
  yang sudah applied — keputusan yang sudah diterapkan tidak bisa di-dismiss.
  Ini sesuai flow "Dismiss hanya untuk rekomendasi PENDING", tapi perlu konfirmasi:
  apakah frontend mengirim dismiss ke `/decisions/{id}/dismiss` atau ke
  `/pricing/dismiss` / `/restock/dismiss`. (Lihat bagian 6.)

### TASK 11 — Decision Monitoring ✅

- `decision_service.py`:
  - `metrics_before` disimpan saat apply; `metrics_after` dihitung **dari data
    aktual saat dibaca** (revenue, margin, stock 30 hari) — bukan prediksi.
  - Outcome `improved / flat / regressed` via `_derive_status`.
  - **Tidak memaksa conclusion**: bila belum ada transaksi setelah keputusan
    (`_has_post_decision_data`), status = `UNKNOWN` dan
    `monitoring_available: false` dengan note penjelas (migrasi enum `c4a1b2d3e5f6`).
- Tidak ada `demoDecisions` / before-after hardcode.

### TASK 12 — Growth Map ✅

- `growth_service.py`: 4 tahap (Catat & Konsisten → Pahami Profitabilitas →
  Keputusan Berbasis Data → Perluas Menuju Pertumbuhan) berbasis **rule**
  (transaksi/minggu, produk ber-HPP, keputusan applied, omzet bulanan) dari data
  aktual — bukan LLM.
- Status **`done / current / next / upcoming`** — `next` sudah dihasilkan
  (gap lama hanya done/current/upcoming); jika semua tahap selesai, tahap terakhir → current.
- Verifikasi smoke test: stages = `current → next → upcoming → upcoming`.

### TASK 13 — Integration & Hardening ✅

- **4 endpoint kontrak yang hilang ditutup**:
  1. `GET /transactions/{transaction_id}` — detail transaksi (+ items, HPP snapshot).
  2. `CRUD /finance/expenses` — `expense_service.py` + `expense_repository.py`
     (list/create/update/delete).
  3. `POST /forecasting/refresh` — recompute + persist forecast.
  4. `POST /decisions/{decision_id}/apply` — apply generic (resolve id → pricing/restock).
- Audit endpoint: seluruh rute `/api/v1/*` termuat di `app/api/v1/router.py`
  (auth, business, products, transactions, inventory, finance, dashboard,
  forecasting, pricing, restock, business_health, decisions, growth, assistant).
- Envelope & snake_case konsisten; semua rute business melewati
  `get_current_business` (auth + ownership).
- Verifikasi menyeluruh dilakukan pada Fase D — lihat file khusus
  **`documents/laporan-backend-integration-hardening-DATARA.md`**.

### TASK 14 — Business Assistant AI ✅

- `assistant_service.py` + `llm_service.py` (adapter provider-agnostic, saat ini
  Gemini via REST).
- **Context injection**: data bisnis aktual (finansial, health, produk+HPP+harga+
  margin+qty+status evaluasi, stok kritis) disusun backend menjadi teks
  terstruktur, disuntikkan sebagai system instruction. LLM tidak pernah
  menyentuh database / tidak mengarang angka.
- **Grounding rules** dalam prompt: bahasa Indonesia, ≤ ~180 kata, tolak di luar
  domain bisnis, tidak mengklaim tindakan (hanya rekomendasi).
- Percakapan **dipersist** (`ai_conversations`/`ai_messages`), list & get
  conversation per business (ownership check).
- Tanpa `GEMINI_API_KEY` → error 502 yang jelas (bukan hasil palsu).
- Router: `/ai/chat`, `/ai/conversations`, `/ai/conversations/{id}`.

---

## 4. Peta Endpoint `/api/v1` (dari `/openapi.json`)

```
/auth/register, /auth/login, /auth/google, /auth/me, /auth/logout
/business
/products, /products/{product_id}, /products/{product_id}/costs, /products/profitability
/transactions, /transactions/{transaction_id}
/inventory, /inventory/movements
/finance/summary, /finance/expenses, /finance/expenses/{expense_id}
/dashboard
/forecasting/products, /forecasting/products/{product_id}, /forecasting/refresh
/pricing/recommendations, /pricing/apply, /pricing/dismiss
/restock/recommendations, /restock/apply, /restock/dismiss
/decisions, /decisions/{decision_id}, /decisions/{decision_id}/apply, /decisions/{decision_id}/dismiss
/growth
/ai/chat, /ai/conversations, /ai/conversations/{conversation_id}
/health (business health, prefix /health di dalam v1)
```

Health endpoint (di luar versioning): `/api/health`, `/api/health/db`.

---

## 5. Verifikasi yang Sudah Dilakukan

| Item | Hasil |
| --- | --- |
| `pytest` (backend) | **85 passed**, 0 gagal; 1 warning deprecation (httpx/starlette) |
| `python -m compileall` | OK |
| Smoke server (uvicorn :8000) | `/api/health` 200 ok · `/api/health/db` 200 connected |
| Auth guard | Request tanpa token → `401` |
| Register + login | 201 / 200, `access_token` valid, envelope `success` |
| Empty-state business | dashboard `INSUFFICIENT_DATA`, products/forecast/transactions `[]`, growth `current→next→upcoming` |
| OpenAPI | Semua endpoint v1 + 4 kontrak baru terdaftar |
| Hygiene | 0 `.pyc` ter-track; `git status` bersih |

Distribusi test: auth_integration 10, auth_unit 13, business_logic_pure 15,
pricing_restock_deterministic 11, models 9, config 5, health 4,
reconciliation_semantics 18.

---

## 6. Temuan & Risiko yang Perlu Keputusan

1. **Movement type (T05)** — ✅ **Resolved** (lihat
   `documents/laporan-backend-reconciliation-DATARA.md`). API
   (`POST/GET /inventory/movements`) memakai terminology lowercase
   `received | waste | adjustment | sale` sesuai API Contract bab 9.2; dipetakan ke
   enum DB `RESTOCK / SALE / ADJUSTMENT / WASTE` di service. Response konsisten
   (lowercase roundtrip), tidak ada alias `issued`.
2. **Semantik dismiss (T10)** — ✅ **Resolved**. Hanya rekomendasi `PENDING` yang
   dapat di-dismiss (`/pricing/dismiss`, `/restock/dismiss`, dan generic
   `/decisions/{id}/dismiss`); rekomendasi `ACCEPTED`/keputusan ter-apply ditolak
   `ConflictError`. `dismiss` generic simetris dengan `apply_generic`.
3. **`Role` inkonsisten di frontend** — `frontend/src/lib/types.ts` masih
   `"owner" | "staff"` sedangkan PRD v1.2 satu actor `Pemilik UMKM`. Tidak
   memengaruhi backend, tapi perlu diselaraskan.
4. **`.env` belum lengkap** — `GEMINI_API_KEY` dan `GOOGLE_CLIENT_ID` masih kosong
   sehingga `/ai/chat` (502) dan login Google (401) non-aktif sampai diisi.
5. **Warning deprecation pytest** — `starlette.testclient` menyarankan `httpx2`
   (minor, non-blokir).
6. **Data smoke test di DB lokal** — akun `smoketest@datara.local` tertinggal di
   MySQL lokal hasil verifikasi; dapat dihapus bila tidak diinginkan.

---

## 7. Rekomendasi Langkah Berikut

1. ✅ Movement type & dismiss semantics telah diselaraskan (Fase D — lihat
   `documents/laporan-backend-reconciliation-DATARA.md`).
2. Tambah test deterministik untuk **decision monitoring** (improved/flat/regressed/UNKNOWN)
   mengikuti gaya `test_pricing_restock_deterministic.py`.
3. Isi `GEMINI_API_KEY` & `GOOGLE_CLIENT_ID` di `.env` bila fitur AI/Google mau aktif.
4. Sinkronkan `Role` di `frontend/src/lib/types.ts` (satu actor `Pemilik UMKM`).
5. Lakukan integrasi end-to-end frontend ↔ backend untuk alur
   Pricing/Restock/Decision menggunakan data produk nyata.

---

## Lampiran — Struktur File Kunci Backend

```
backend/app/
├── main.py                        # FastAPI app (CORS, handlers, router)
├── core/                          # config, errors, exceptions, security
├── db/                            # base, base_models, session
├── models/                        # 19 entity SQLAlchemy + enums.py
├── schemas/                       # Pydantic v2
├── api/deps.py                    # get_current_business (ownership)
├── api/router.py                  # mount v1 + health
├── api/v1/router.py               # registrasi 14 router bisnis
├── api/v1/routes/                 # 14 file route
├── services/                      # source of truth business logic
└── repositories/                  # akses data per entitas
backend/alembic/versions/          # 5 migrasi
backend/tests/                     # 7 file test (67 function)
```