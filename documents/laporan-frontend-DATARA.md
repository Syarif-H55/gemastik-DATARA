# Laporan Menyeluruh Project DATARA — Frontend

> Dokumen ini adalah ringkasan menyeluruh dari **frontend** Project DATARA yang sudah dibangun.
> Tujuan: menjadi konteks tunggal untuk membuat dokumen-dokumen lain (misal: arsitektur backend, API spec, test plan, panduan implementasi, dokumen kompetisi, dsb).
> Disusun dari pembacaan langsung seluruh kode sumber di `frontend/` (Agustus 2026).

---

## 1. Identitas Proyek

| Item | Keterangan |
| --- | --- |
| **Nama Produk** | **DATARA** — *Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM* |
| **Versi PRD** | v1.2 (draft, 9 Agustus 2026) — file `documents/PRD DATARA.docx.md` |
| **Tim** | Pisang — Agil Kurniawan, Syarif Hidayatullah, Raifa Aziz F. P. H. |
| **Product Owner** | [haswa] |
| **Client / Stakeholder** | UMKM (Food & Beverage skala mikro) |
| **Kompetisi** | GEMASTIK |
| **Konsep** | *Decision Support System*: mengolah data penjualan, HPP, biaya, stok, dan profitabilitas menjadi indikator bisnis serta rekomendasi keputusan yang **terjelaskan (explainable)**. |
| **Status saat laporan ini dibuat** | Frontend demo selesai dan dapat dijalankan (`npm run dev`). Backend FastAPI **belum dibuat**. |

### Catatan penting: rebranding KIRA → DATARA
Nama produk sudah direbranding menjadi **DATARA** di seluruh frontend (metadata, landing page, halaman login, dan brand sidebar). Icon wrapper diberi nama `datara-icons.tsx`.

---

## 2. Arsitektur

- **Arsitektur decoupled (terpisah):**
  - **Frontend**: Next.js 16 (App Router) di folder `frontend/` — sudah dibangun, berjalan dengan **mock data** (`src/lib/demo-data.ts`) tanpa backend.
  - **Backend**: FastAPI + Python + MySQL (rencana) — **belum ada kode**.
- Frontend mengonsumsi REST API dari backend melalui `frontend/src/lib/api.ts` (base URL dari `NEXT_PUBLIC_API_URL`, default `http://localhost:8000/api`).
- **Satu actor utama**: `Pemilik UMKM`. Tidak ada role Staff/Owner terpisah di produk (sesuai PRD v1.1–v1.2). Semua halaman berada di route group `(app)` dengan satu sidebar.
- Semua halaman fitur memakai **demo/mock data** yang diimpor langsung dari `src/lib/demo-data.ts` (bukan fetch API). Ini berarti seluruh algoritma analitik saat ini **berjalan di client** (browser).

---

## 3. Tech Stack (Frontend)

| Teknologi | Versi | Keterangan |
| --- | --- | --- |
| Next.js | 16.3.0 | App Router (Catatan: ini Next.js 16 — `params`/`searchParams` berupa `Promise`, route type helpers `PageProps`/`LayoutProps` global tersedia) |
| React | 19.2.8 | |
| TypeScript | ^5 | `strict: true` |
| Tailwind CSS | ^4 (v4) | Konfigurasi CSS-first lewat `@theme inline` di `globals.css`; PostCSS `@tailwindcss/postcss` |
| shadcn/ui | ^4.16.2 (CLI) | Base `radix-ui` ^1.6.7, style `radix-lyra`, icon library `phosphor`; deklarasi di `components.json` |
| recharts | ^3.8.0 | Chart (Area, Bar, Line) |
| @phosphor-icons/react | ^2.1.10 | Icon set |
| next-themes | ^0.4.6 | Tema terang/gelap |
| sonner | ^2.0.7 | Notifikasi toast |
| tw-animate-css | ^1.4.0 | Animasi CSS |
| class-variance-authority, clsx, tailwind-merge | — | Utilitas styling (`cn()` di `src/lib/utils.ts`) |
| Font | Geist, Geist Mono, JetBrains Mono | via `next/font/google` |

**Skrip npm (`frontend/package.json`):**
- `npm run dev` — menjalankan dev server (Next.js)
- `npm run build` — build produksi + typecheck
- `npm start` — menjalankan hasil build
- `npm run lint` — ESLint

Tidak ada test suite. Konfigurasi minimal: `next.config.ts` kosong, `tsconfig.json` standar dengan alias `@/* → ./src/*`.

---

## 4. Struktur Direktori Frontend

```
frontend/
├── .gitignore
├── AGENTS.md                  ← aturan proyek + konvensi (baca sebelum edit)
├── CLAUDE.md                  ← alias ke AGENTS.md
├── components.json            ← konfigurasi shadcn/ui (style radix-lyra, icon phosphor)
├── eslint.config.mjs
├── next.config.ts
├── package.json / package-lock.json
├── postcss.config.mjs
├── tsconfig.json
├── public/                    ← aset Next.js default (svg) + favicon
└── src/
    ├── app/
    │   ├── layout.tsx         ← Root layout: ThemeProvider + TooltipProvider + Toaster
    │   ├── page.tsx           ← Landing page (DATARA)
    │   ├── globals.css        ← Tailwind v4 + CSS variables (oklch, light/dark)
    │   ├── login/
    │   │   └── page.tsx       ← Form login (belum terhubung backend)
    │   └── (app)/             ← Route group aplikasi (semua halaman fitur, satu sidebar)
    │       ├── layout.tsx     ← AppShell + navItems + brand + footer akun
    │       ├── dashboard/page.tsx
    │       ├── transactions/page.tsx
    │       ├── forecasting/page.tsx
    │       ├── forecasting/chart-utils.ts
    │       ├── products/page.tsx
    │       ├── pricing/page.tsx
    │       ├── restock/page.tsx
    │       ├── decisions/page.tsx
    │       └── growth/page.tsx
    ├── components/
    │   ├── kira-icons.tsx      ← client wrapper Phosphor icons untuk Server Component
    │   ├── theme-provider.tsx  ← wrapper next-themes
    │   ├── theme-toggle.tsx    ← toggle terang/gelap
    │   ├── page-header.tsx     ← PageHeader + EmptyState + ModuleBadge
    │   ├── layout/
    │   │   ├── app-shell.tsx   ← SidebarProvider + header + main
    │   │   └── app-sidebar.tsx ← Sidebar + navItems (8 menu)
    │   └── ui/                 ← komponen shadcn/ui (lihat Bagian 11)
    ├── hooks/
    │   └── use-mobile.ts       ← hook pendeteksi mobile (untuk sidebar)
    └── lib/
        ├── types.ts            ← domain model / kontrak API
        ├── api.ts              ← REST API client
        ├── format.ts           ← format id-ID (Rupiah, %, angka, tanggal)
        ├── utils.ts            ← cn() (clsx + tailwind-merge)
        └── demo-data.ts        ← mock data + seluruh algoritma analitik demo
```

---

## 5. Routing & Layout

### 5.1 Root layout (`src/app/layout.tsx`)
- Meta default: title `"DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM"`, template `"%s · DATARA"`.
- Menyediakan `ThemeProvider` (default theme `light`, `enableSystem`), `TooltipProvider`, dan `Toaster` (sonner, `richColors`, `closeButton`).
- `lang="id"`, font: `--font-geist-sans`, `--font-mono` (Geist Mono), `--font-mono` di-override JetBrains Mono.

### 5.2 Landing page (`/`, `src/app/page.tsx`) — Server Component
- Hero singkat DATARA + dua aksi: **Masuk Aplikasi** (`/login`) dan **Lihat Demo** (`/dashboard`).

### 5.3 Login (`/login`, `src/app/login/page.tsx`) — Client Component
- Form email + kata sandi, tombol "Masuk" mengarah ke `/dashboard` (tanpa autentikasi nyata).
- Ada keterangan: *"Demo belum terhubung ke backend. Autentikasi akan dihubungkan ke API FastAPI."*

### 5.4 App layout (`src/app/(app)/layout.tsx`) — Server Component
- Membungkus semua halaman fitur dengan `AppShell`.
- `AppBrand`: logo + teks **DATARA** (mengarah ke `/dashboard`).
- `AppFooter`: dropdown akun dengan avatar "PK" — label *Pemilik UMKM*, sub-label *owner*, menu **Keluar** (belum berfungsi).

### 5.5 AppShell (`src/components/layout/app-shell.tsx`)
- `SidebarProvider` → `AppSidebar` + `SidebarInset`.
- Header: `SidebarTrigger` (hamburger), separator vertikal, `ThemeToggle` di kanan.
- Main: padding responsif `p-4 md:p-6 lg:p-8`.

### 5.6 AppSidebar & navigasi (`src/components/layout/app-sidebar.tsx`)
- Sidebar collapsible (`collapsible="icon"`), dengan deteksi active item berdasarkan `pathname`.
- `navItems` (8 menu):

| Menu | Route | Icon |
| --- | --- | --- |
| Business Dashboard | `/dashboard` | ChartLineUp |
| Catat Transaksi | `/transactions` | ShoppingCart |
| Sales Forecasting | `/forecasting` | LineSegments |
| Product Profitability | `/products` | ChartPieSlice |
| Smart Pricing | `/pricing` | Target |
| Smart Restock | `/restock` | Package |
| Keputusan & Monitoring | `/decisions` | ClipboardText |
| Roadmap Pertumbuhan | `/growth` | Signpost |

> Konvensi penting: file `"use client"` boleh mengimpor langsung dari `@phosphor-icons/react`, sedangkan Server Component **harus** memakai `src/components/datara-icons.tsx` (client wrapper). Nama export Phosphor sering berbeda dari tebakan (contoh: `TrendUp`, `SignOut`, `ArrowsDownUp`, `WarningCircle`).

---

## 6. Detail Fitur per Halaman

Semua halaman di bawah adalah **Client Component** (`"use client"`) dan memakai mock data dari `demo-data.ts`.

### 6.1 Business Dashboard (`/dashboard`)
- **Tujuan**: Ringkasan kesehatan bisnis (FR-001).
- **UI**: `PageHeader` dengan badge periode "Juni 2025" + badge status health; kartu **Business Health Score** (angka + Progress bar); 4 kartu metrik utama; 2 kartu aktivitas; AreaChart "Tren Pendapatan" (omzet & laba 7 hari); BarChart "Kontribusi Kategori" (Makanan/Minuman/Camilan).
- **Metrik utama**: Omzet, Laba, HPP, Margin Rata-rata.
- **Metrik aktivitas**: Jumlah Transaksi, Produk terjual.
- **Data**: `getDashboardMetrics()` — dihitung dari profitabilitas produk + transaksi demo.

### 6.2 Catat Transaksi (`/transactions`)
- **Tujuan**: Pencatatan penjualan harian; stok terpotong otomatis (workflow PRD 6.1).
- **UI**: Grid `[daftar produk | keranjang]` + panel "Ringkasan" sticky. Setiap produk adalah tombol yang bisa diklik untuk menambah ke keranjang (tampilan tombol berubah jika sudah masuk keranjang, lengkap dengan jumlah).
- **Fitur keranjang**: tambah/kurang qty (`changeQty`), hapus item, validasi stok (tidak boleh melebihi stok — menampilkan toast "Stok tidak cukup"), field Nama Pelanggan (opsional) dan Uang Diterima.
- **Interaksi**: tombol **Simpan Transaksi** memvalidasi keranjang kosong (toast error) dan menampilkan toast sukses dengan total; kemudian mereset keranjang. **Belum ada penyimpanan nyata / update stok asli** (hanya simulasi).
- **Penanda stok rendah**: label stok berwarna merah jika `stock <= low_stock_threshold`.

### 6.3 Sales Forecasting (`/forecasting`)
- **Tujuan**: Prediksi penjualan per produk periode berikutnya (FR-006); dasar Smart Restock.
- **UI**: Dropdown pilih produk (Select), 3 kartu ringkas (Prediksi Periode, Estimasi Penjualan dalam unit, Kepercayaan model), LineChart aktual vs forecast (garis padat = aktual, putus-putus = prediksi) dengan ReferenceLine pemisah, badge tren + blok reasoning.
- **Interaksi**: ganti produk di dropdown → seluruh isi berubah sesuai `getProductForecasts()`.
- **Badge tren**: Tren Naik (emerald), Tren Menurun (red), Stabil (slate) — lihat `chart-utils.ts`.

### 6.4 Product Profitability (`/products`)
- **Tujuan**: Klasifikasi produk menguntungkan / berpotensi / perlu dievaluasi (FR-004, FR-011).
- **UI**: 3 kartu ringkas berisi jumlah produk per klasifikasi; tabel produk dengan kolom Produk, Harga Jual, HPP, Laba/Unit, Margin, Terjual, Total Laba, Klasifikasi (badge + alasan).
- **Fitur tabel**: pencarian (nama/SKU), filter kategori (Semua/Minuman/Makanan/Camilan berdasarkan prefix SKU `MIN`/`FOOD`/`SNK`), filter klasifikasi, dan sortir per kolom (klik header, toggle asc/desc; icon `ArrowsDownUp`).
- **Tone warna margin**: ≥40 emerald, ≥25 amber, sisanya merah. Klasifikasi: `profitable` emerald, `potential` blue, `evaluate` red.

### 6.5 Smart Pricing (`/pricing`)
- **Tujuan**: Rekomendasi harga jual berbasis HPP, biaya, dan target margin (FR-005, FR-008).
- **UI**: Slider **Target Margin Kotor** (10–60%, default 30%) + tombol "Terapkan Semua Rekomendasi"; tabel rekomendasi (Produk, Harga Saat Ini, HPP, Margin Aktual, Harga Rekomendasi, Alasan).
- **Interaksi**: menggeser slider → semua harga rekomendasi dihitung ulang live. Baris dengan perubahan harga ditandai (`bg-primary/5`); margin aktual di bawah target diberi badge destructive.
- **Rumus**: `harga_rekomendasi = ceil(HPP ÷ (1 − targetMargin))` lalu dibulatkan ke kelipatan Rp 500. Alasan auto-generated dalam Bahasa Indonesia.

### 6.6 Smart Restock (`/restock`)
- **Tujuan**: Rekomendasi waktu & jumlah restock berdasarkan stok, riwayat penjualan, dan forecast (FR-007, FR-008).
- **UI**: Badge peringatan di header bila ada produk kritis; dropdown filter prioritas (Semua/Kritis/Perlu Restock/Aman); tabel (Produk, Stok, Forecast, Hari Persediaan, Rekomendasi Restock, Prioritas, Alasan, aksi Restock).
- **Interaksi**: tombol **Restock** per baris → toast sukses (belum ada aksi nyata).
- **Rumus**:
  - `days_of_supply = stok ÷ rata-rata penjualan harian (dari forecast)`
  - `suggested_qty = max(0, (rata-rata harian × lead time 3 hari) − stok + ambang minimum)`
  - Urgency: `critical` jika `stok ≤ low_stock_threshold`; `low` jika `days_of_supply ≤ lead time + 2`; selain itu `healthy`.

### 6.7 Keputusan & Monitoring (`/decisions`)
- **Tujuan**: Rekap rekomendasi yang diterapkan + perkembangan indikator setelahnya (FR-009, FR-010).
- **UI**: Daftar kartu keputusan. Tiap kartu: badge tipe (Smart Pricing / Smart Restock), judul, ringkasan, tanggal diterapkan, badge status hasil, blok "Alasan & Data Pendukung", 3 kartu delta indikator (Omzet, Margin, Stok: nilai sekarang + selisih vs sebelum keputusan), dan catatan hasil.
- **Status**: `improved` (Membaik, emerald), `regressed` (Menurun, red), `flat` (Stabil, slate) — catatan: ada juga key `restricted` (Terbatas) di `statusMeta` yang tidak dipakai data demo saat ini.
- **Data**: `demoDecisions` (3 keputusan contoh).

### 6.8 Roadmap Pertumbuhan (`/growth`)
- **Tujuan**: Evaluasi perkembangan usaha + langkah menuju target berikutnya (FR-011, FR-012).
- **UI**: Grid 2 kolom kartu tahapan. Tiap kartu: nomor urut, judul, deskripsi, badge status, metrik dengan Progress bar, dan teks "Target tercapai" atau "Langkah berikutnya: …".
- **Status tahapan**: `done` (Selesai), `current` (Sedang Berjalan, kartu disorot), `next`, `upcoming`.
- **Data**: `getGrowthStages()` — 4 tahapan: Catat & Konsisten, Pahami Profitabilitas, Keputusan Berbasis Data, Perluas Menuju Pertumbuhan.

---

## 7. Domain Model — Kontrak API (`src/lib/types.ts`)

Ini adalah kontrak data yang harus disepakati backend FastAPI. Semua field berikut dipakai frontend saat ini:

| Interface | Field utama | Catatan |
| --- | --- | --- |
| `Role` | `"owner" \| "staff"` | **Masih ada**, padahal produk memakai satu actor. Backend dapat menyediakan, frontend belum menggunakannya. |
| `User` | `id, name, email, role` | |
| `ProductMovementType` | `"received" \| "issued" \| "adjustment" \| "sale"` | |
| `Product` | `id, name, sku, selling_price, hpp, stock, low_stock_threshold, is_active, created_at, updated_at` | |
| `ProductProfitability` | `product_id, name, sku, selling_price, hpp, unit_profit, margin_percent, qty_sold, total_revenue, total_cost, total_profit` | |
| `InventoryLog` | `id, product_id, product_name?, movement_type, quantity, stock_after, note, created_at` | `product_name` opsional |
| `TransactionItem` | `product_id, quantity, unit_price` | |
| `Transaction` | `id, reference_number, customer_name?, transaction_date, subtotal, discount, total, items[]` | |
| `Cost` | `id, name, amount, category, occurs_at, notes, created_at` | |
| `DecisionType` | `"pricing" \| "restock"` | |
| `DecisionStatus` | `"recommended" \| "applied" \| "dismissed"` | |
| `Decision` | `id, type, title, explanation, payload, status, created_at` | `payload` adalah `Record<string, unknown>` |
| `PricingRecommendation` | `product_id, name, sku, current_price, recommended_price, hpp, target_margin_percent, actual_margin_percent, reasoning` | |
| `RestockRecommendation` | `product_id, name, sku, current_stock, low_stock_threshold, days_of_supply, suggested_quantity, urgency ("critical"\|"low"\|"healthy"), reasoning` | |
| `BusinessHealth` | `score, label` | |
| `DashboardMetrics` | `total_revenue, total_profit, total_cogs, avg_margin_percent, transactions_count, products_sold, business_health, revenue_trend[], category_breakdown[]` | |
| `ForecastPoint` | `period, actual, forecast, lower?, upper?` | |
| `ProductForecast` | `product_id, name, sku, model, method, next_period, predicted_units, confidence, trend ("up"\|"down"\|"flat"), points[], reasoning` | |
| `ProductClass` | `"profitable" \| "potential" \| "evaluate"` | |
| `DecisionRecord` | `id, type, title, summary, reasoning, applied_at, metrics_before, metrics_after, status ("improved"\|"flat"\|"regressed"), outcome_notes` | `metrics_*` berisi `{revenue, margin, stock}` |
| `GrowthStage` | `id, label, description, status ("done"\|"current"\|"next"\|"upcoming"), metric_1, metric_1_value, metric_1_target, next_step` | |

**Relasi antar entitas (pola yang dipakai demo):**
- `Product` ↔ `InventoryLog` (1:N, via `product_id`).
- `Transaction` ↔ `TransactionItem` ↔ `Product`.
- `ProductProfitability`, `PricingRecommendation`, `RestockRecommendation`, `ProductForecast` dihitung per `product_id`.
- `Decision` (recommendation) vs `DecisionRecord` (yang sudah diterapkan + monitoring).

---

## 8. Algoritma & Logika Demo (`src/lib/demo-data.ts`)

Seluruh logika bisnis saat ini ada di sini (client-side). Backend nanti harus menghasilkan hasil yang sama/setara.

**Konstanta demo**: `TARGET_MARGIN = 0.3` (30%), `LEAD_TIME_DAYS = 3`.

**Data demo utama:**
- `demoProducts` — 8 produk (3 minuman, 2 makanan, 2 camilan, 1 air mineral) dengan harga, HPP, stok, dan ambang stok rendah.
- `demoInventoryLogs` — 10 log pergerakan stok (sale/received/adjustment).
- `demoTransactions` — 4 transaksi dengan item & diskon.
- `demoDecisions` — 3 keputusan terapan dengan metrik sebelum/sesudah.

### 8.1 Profitabilitas produk — `getProductProfitability()`
Untuk tiap produk:
- `qty_sold` = jumlah absolut qty log bertipe `sale`.
- `total_revenue = qty_sold × selling_price`; `total_cost = qty_sold × hpp`.
- `unit_profit = selling_price − hpp`; `margin_percent = unit_profit ÷ selling_price × 100`.
- `total_profit = total_revenue − total_cost`.

### 8.2 Smart Pricing — `getPricingRecommendations(targetMargin)`
- `costBasedPrice = hpp ÷ (1 − targetMargin/100)`; dibulatkan ke kelipatan 500 (`Math.ceil(costBasedPrice/500)*500`).
- Bandingkan harga rekomendasi vs harga saat ini untuk membentuk `reasoning` (naikkan harga / tidak perlu perubahan).

### 8.3 Sales Forecasting — `getProductForecasts()`
- Tiap produk punya konfigurasi tren (`up`/`down`/`flat`) + base.
- Deret 7 hari dibangkitkan dengan fungsi `buildForecastSeries(base, trend)`: level = base + drift per hari, ditambah gelombang `sin(i/1.7)×2.5`.
- Metode ditentukan dari tren: `flat` → "Moving Average (7 hari)" (model `moving-average`); `up`/`down` → "Simple Exponential Smoothing" (model `linear-trend`).
- `confidence`: 88% untuk `flat`, 76% untuk lainnya. `reasoning` dihasilkan sesuai tren.
- `next_period` demo: `"2025-06-11"`.

### 8.4 Smart Restock — `getRestockRecommendations(leadTime)`
- Ambil forecast tiap produk; `avgDailySold = max(1, predicted_units)` (fallback: `round(stock×0.35)`).
- `daysOfSupply`, `suggestedQuantity`, `urgency`, dan `reasoning` sesuai rumus di Bagian 6.6.

### 8.5 Klasifikasi produk — `getProductClass(p)`
Aturan (berdasarkan margin & qty sold):
- `margin ≥ 35` = margin baik; `margin < 20` = margin rendah; `qty ≥ 10` = penjualan tinggi; `qty < 4` = penjualan rendah.
- Penjualan tinggi + margin baik → **profitable** (Menguntungkan).
- Penjualan rendah + margin baik → **potential** (Berpotensi).
- Penjualan tinggi + margin rendah → **evaluate** (Perlu Evaluasi).
- Selain itu → **evaluate**.

### 8.6 Dashboard metrics — `getDashboardMetrics()`
- `total_revenue`, `total_cogs`, `total_profit`, `avg_margin_percent` = agregat dari profitabilitas.
- `transactions_count` = jumlah transaksi demo; `products_sold` = jumlah produk dengan qty>0.
- `revenue_trend` = 7 titik tanggal keras (tanggal 4–10 Juni 2025, omzet & laba).
- `category_breakdown` = agregat omzet per prefix SKU (FOOD/MIN/SNK).
- **Business Health Score**: `rawScore = 40 + avg_margin + (products_sold/total_products)×20`, diclamp 0–100; label: `≥75` Sehat, `≥50` Cukup, selainnya Perlu Perhatian.

### 8.7 Growth stages — `getGrowthStages()`
- 4 tahap: Catat & Konsisten (done), Pahami Profitabilitas (done), Keputusan Berbasis Data (current), Perluas Menuju Pertumbuhan (upcoming) — masing-masing dengan metrik, nilai/target, dan langkah berikutnya.

---

## 9. API Client (`src/lib/api.ts`)

- `API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api"`.
- Wrapper `request<T>(path, options)`: menambahkan header `Accept`/`Content-Type: application/json`, body di-`JSON.stringify` bila ada, `cache: "no-store"`.
- Menangani error: membaca `message` dari respons JSON bila ada, membungkus ke `ApiError` (`status`, `message`, `details`).
- Menangani `204 No Content` → return `undefined`.
- Method tersedia: `get`, `post`, `patch`, `put`, `delete` (generik).
- **Saat ini belum digunakan oleh halaman apa pun** — semua halaman memakai `demo-data.ts`. Halaman login menyebut akan terhubung ke FastAPI.
- Contoh `.env`: `NEXT_PUBLIC_API_URL` (belum ada file `.env` di repo).

---

## 10. Formatting Helpers (`src/lib/format.ts`)

Semua memakai locale `id-ID`:
- `formatRupiah(value)` — mata uang IDR, tanpa desimal.
- `formatPercent(value, digits=1)` — `"30.0%"`.
- `formatNumber(value)` — pemisah ribuan Indonesia.
- `formatDate(value)` — `dd MMM yyyy`.
- `formatDateTime(value)` — `dd MMM yyyy, HH:mm`.

---

## 11. Komponen UI

### 11.1 Komponen shadcn/ui terpasang (`src/components/ui/`)
`alert`, `alert-dialog`, `avatar`, `badge`, `button`, `card`, `chart`, `dialog`, `dropdown-menu`, `input`, `label`, `progress`, `select`, `separator`, `sheet`, `sidebar`, `skeleton`, `sonner`, `table`, `tabs`, `textarea`, `tooltip`.

### 11.2 Komponen internal
- `datara-icons.tsx` — re-export client untuk: `CashRegister, ChartDonut, ChartPieSlice, Receipt, SignOut, ShoppingCart, TrendUp, Wallet, Warehouse`. **Wajib dipakai di Server Component.**
- `page-header.tsx` — `PageHeader` (title/description/actions), `EmptyState`, `ModuleBadge`.
- `app-shell.tsx`, `app-sidebar.tsx` — kerangka aplikasi (Bagian 5).
- `theme-provider.tsx`, `theme-toggle.tsx` — mode terang/gelap (ikon Sun/MoonStars).
- `hooks/use-mobile.ts` — deteksi ukuran layar untuk sidebar.

---

## 12. Gap Analysis vs PRD (FR Table v1.2)

### 12.1 Sudah diimplementasikan (UI demo frontend)
| FR | Fitur | Status UI |
| --- | --- | --- |
| FR-001 | Business Dashboard (omzet, laba, HPP, margin, transaksi, health) | ✅ `/dashboard` |
| FR-002 | Perhitungan HPP | ✅ dihitung di `demo-data.ts` (tampil di `/products`, `/pricing`) |
| FR-003 | Analisis performa penjualan per periode/produk | ✅ `/products` (terjual, total laba) + `/dashboard` tren |
| FR-004 | Profitabilitas per produk (pendapatan, HPP, laba, margin) | ✅ `/products` |
| FR-005 | Rekomendasi harga jual + target margin | ✅ `/pricing` (slider target margin) |
| FR-006 | Prediksi penjualan (Sales Forecasting) | ✅ `/forecasting` (mock) |
| FR-007 | Rekomendasi restock (waktu & jumlah) | ✅ `/restock` |
| FR-008 | Alasan & data pendukung setiap rekomendasi | ✅ `reasoning` pada pricing/restock/forecast/klasifikasi |
| FR-009 | Mencatat rekomendasi/keputusan yang dipilih | ⚠️ `/pricing` & `/restock` punya tombol terapkan/restock (hanya toast) |
| FR-010 | Memantau indikator setelah keputusan diterapkan | ✅ `/decisions` (data statis) |
| FR-011 | Evaluasi perkembangan bisnis + posisi usaha | ✅ `/growth` + `/dashboard` |
| FR-012 | Informasi target/langkah pertumbuhan berikutnya | ✅ `/growth` |

### 12.2 Belum diimplementasikan
- **Backend FastAPI + MySQL** (belum ada kode sama sekali).
- **Autentikasi nyata** (login saat ini langsung redirect ke `/dashboard`).
- **CRUD data** (produk, transaksi, biaya, stok) — saat ini semua mock/statis.
- **Penyimpanan & pembaruan stok nyata** saat transaksi disimpan (hanya simulasi + toast).
- Persistensi data (semua di-reset saat reload).

### 12.3 Out of Scope (v1) — tidak perlu dibuat untuk MVP
- What-If Simulator, Smart Alert, Action Center, Business Assistant, integrasi eksternal (marketplace/payment/POS), dan otomatisasi operasional (pemesanan/ubah harga otomatis).

---

## 13. Catatan Penting untuk Developer / ChatGPT

1. **Rebranding KIRA → DATARA sudah tuntas.** Semua branding (metadata, landing page, login, `AppBrand`, `AGENTS.md`) memakai **DATARA** dengan tagline PRD *"Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM"*. Icon wrapper bernama `datara-icons.tsx`.
2. **Role ganda**: `types.ts` masih mendefinisikan `Role = "owner" | "staff"` dan footer menampilkan sub-label "owner", padahal PRD v1.1–1.2 menetapkan **satu actor (Pemilik UMKM)**. Backend boleh menyediakan kolom role, tetapi frontend tidak boleh bergantung pada dua role.
3. **Kontrak API harus konsisten dengan `types.ts`.** Sebelum men-scaffold backend, pastikan nama field JSON sesuai (snake_case seperti `selling_price`, `low_stock_threshold`, `predicted_units`, dst.) agar `api.ts` bekerja tanpa perubahan.
4. **Konvensi icon**: Server Component tidak boleh mengimpor `@phosphor-icons/react` langsung — wajib lewat `datara-icons.tsx`. Nama export Phosphor perlu dicek bila build gagal (lihat AGENTS.md frontend).
5. **Konvensi Next.js 16**: `params`/`searchParams` adalah `Promise` (harus `await`); type helpers `PageProps`/`LayoutProps` tersedia global.
6. **Verifikasi**: tidak ada test suite. Jalankan `npm run lint` dan `npm run build` setelah perubahan.
7. **skema data penting**: SKU memakai prefix kategori `MIN`/`FOOD`/`SNK` yang juga berfungsi sebagai kategori (dipakai di filter & breakdown kategori).
8. **Tanggal demo** memakai tahun 2025 (Juni 2025) meski PRD bertanggal 2026 — data mock tidak harus sinkron, tetapi backend nanti harus mengelola tanggal dinamis.

---

## 14. Lampiran — Daftar File Sumber

```
documents/PRD DATARA.docx.md              ← spesifikasi produk (PRD v1.2)
AGENTS.md                                 ← panduan proyek (root)
frontend/package.json                     ← dependensi & skrip
frontend/components.json                  ← konfigurasi shadcn/ui
frontend/tsconfig.json                    ← alias @/*
frontend/src/app/layout.tsx               ← root layout
frontend/src/app/page.tsx                 ← landing
frontend/src/app/globals.css              ← Tailwind v4 + tema oklch
frontend/src/app/login/page.tsx           ← login (belum terhubung)
frontend/src/app/(app)/layout.tsx         ← kerangka aplikasi
frontend/src/app/(app)/dashboard/page.tsx
frontend/src/app/(app)/transactions/page.tsx
frontend/src/app/(app)/forecasting/page.tsx
frontend/src/app/(app)/forecasting/chart-utils.ts
frontend/src/app/(app)/products/page.tsx
frontend/src/app/(app)/pricing/page.tsx
frontend/src/app/(app)/restock/page.tsx
frontend/src/app/(app)/decisions/page.tsx
frontend/src/app/(app)/growth/page.tsx
frontend/src/components/layout/app-shell.tsx
frontend/src/components/layout/app-sidebar.tsx
frontend/src/components/datara-icons.tsx
frontend/src/components/page-header.tsx
frontend/src/components/theme-provider.tsx
frontend/src/components/theme-toggle.tsx
frontend/src/components/ui/*                ← 21 komponen shadcn/ui
frontend/src/hooks/use-mobile.ts
frontend/src/lib/types.ts                  ← domain model / kontrak API
frontend/src/lib/api.ts                    ← API client
frontend/src/lib/format.ts                 ← format id-ID
frontend/src/lib/utils.ts                  ← cn()
frontend/src/lib/demo-data.ts              ← mock data + algoritma analitik
```
