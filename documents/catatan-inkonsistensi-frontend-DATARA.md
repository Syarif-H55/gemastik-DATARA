# CATATAN INKONSISTENSI FRONTEND vs DOKUMEN DATARA

**Pembaca:** Developer Frontend (Next.js)
**Penulis:** Developer Backend (FastAPI)
**Status:** Catatan kerja — item bertanda "perlu keputusan" belum final

---

# 1. Tujuan Dokumen

Dokumen ini mencatat perbedaan antara **kontrak data yang dipakai frontend saat ini** (`frontend/src/lib/types.ts`) dengan acuan produk resmi:

- `documents/DATA_DICTIONARY_AND_DATA_MODEL_DATARA.md` — status **FINAL**
- `documents/bussiness-rule-dan-decision-logic.md` — status **FINAL, v1.0**

**Prinsip yang disepakati:**

> Frontend **tidak diubah** pada tahap ini. Backend yang menyesuaikan kontrak API agar sesuai kebutuhan UI, selagi tidak melanggar aturan bisnis dan data model.

Catatan ini membantu frontend developer memahami **apa yang akan backend sediakan** di respons API (snake_case), sehingga saat integrasi nyata tiba, `api.ts` dapat dipakai tanpa perubahan besar.

---

# 2. Ringkasan Inkonsistensi

| # | Interface Frontend | Lokasi | Singkatan Masalah |
|---|---|---|---|
| 1 | `Role = "owner" \| "staff"` | `types.ts:1,7` | Role ganda tidak dipakai; produk hanya 1 actor |
| 2 | `Product.sku`, `hpp`, `stock`, `low_stock_threshold` | `types.ts:12-23` | Field tidak ada di tabel `products` |
| 3 | `Product` tanpa `unit`, `business_id` | `types.ts:12-23` | Field ada di data dictionary |
| 4 | ~~`ProductMovementType = received/issued/adjustment/sale`~~ | `types.ts:10` | ✅ Resolved → `received/waste/adjustment/sale` |
| 5 | `InventoryLog.stock_after`, `note` | `types.ts:39-48` | Tidak ada di `inventory_movements` |
| 6 | `Transaction.reference_number`, `customer_name`, `subtotal`, `discount`, `total` | `types.ts:56-66` | Tidak ada di `sales_transactions` |
| 7 | Tidak ada `status` transaksi | — | Business Rules 6.3 butuh transaksi batal |
| 8 | `TransactionItem` tanpa `unit_hpp` | `types.ts:50-54` | Ada di `sales_transaction_items` |
| 9 | `Cost` generic (category, occurs_at, notes) | `types.ts:68-76` | Tidak cocok dengan `product_costs`/`operating_expenses` |
| 10 | `Decision` generic + `DecisionStatus` | `types.ts:78-89` | Berbeda dari tabel recommendation |
| 11 | `PricingRecommendation.target_margin_percent`, `reasoning` | `types.ts:91-101` | Target margin tidak tersimpan di DB |
| 12 | `RestockRecommendation.low_stock_threshold`, `days_of_supply`, `urgency` | `types.ts:103-113` | Field & status beda |
| 13 | `BusinessHealth.label` ("Cukup") | `types.ts:115-118` | Enumerasi health beda |
| 14 | `ProductForecast.confidence`, `trend`, `points[]`, `method`, `reasoning` | `types.ts:140-152` | Banyak field derived, tak tersimpan |
| 15 | Forecast tanpa status INSUFFICIENT | `types.ts:140-152` | Business Rules 8.3 butuh INSUFFICIENT |
| 16 | `ProductClass = profitable/potential/evaluate` | `types.ts:154` | Nama klasifikasi beda dengan rule |
| 17 | `DecisionRecord` (applied + monitoring) | `types.ts:156-167` | Tidak ada tabel di data dictionary |
| 18 | `GrowthStage` (roadmap) | `types.ts:169-178` | Sangat beda dari `growth_recommendations` |
| 19 | SKU prefix (MIN/FOOD/SNK) = kategori | `demo-data.ts` | Tidak ada field sku/kategori di data dictionary |
| 20 | `business_configurations` hanya `safety_days` | — | Business Rules butuh lead_time & target_margin |

---

# 3. Detail Per Item

> Kolom **Rekomendasi Backend** = arah yang akan backend lakukan di kontrak API (belum tentu sudah final).

## 3.1 Role ganda

**Frontend:** `Role = "owner" | "staff"` (types.ts:1,7); `User.role`; footer menampilkan "owner".

**Dokumen:** Data Dictionary tidak mendefinisikan role; PRD v1.1 & Business Rules 2.2 menetapkan satu actor — **Pemilik UMKM**. Tidak ada role Staff/Admin.

**Rekomendasi Backend:** Respons `user` tidak akan mengirim field `role` (atau dikirim konstan `"owner"` bila frontend tetap membutuhkannya). Frontend disarankan segera melepas dependensi terhadap `role` agar tidak ambigu.

---

## 3.2 Product — field `sku`, `hpp`, `stock`, `low_stock_threshold`

**Frontend:** `Product` butuh `sku`, `selling_price`, `hpp`, `stock`, `low_stock_threshold`, `is_active` (types.ts:12-23).

**Dokumen:** Tabel `products` (Data Dictionary 6.1) hanya punya: `name`, `selling_price`, `unit`, `is_active`, timestamps.

- **`hpp`** — TIDAK disimpan di `products`; dihitung dari `product_costs`.
- **`stock`** — TIDAK disimpan di `products`; diambil dari `inventory_items.current_stock`.
- **`sku`** — tidak ada kolom SKU di data dictionary.
- **`low_stock_threshold`** — tidak ada field ambang stok rendah di seluruh data model.

**Rekomendasi Backend:** Endpoint `GET /products` akan mengembalikan objek **gabungan (aggregate)**:

```json
{
  "id": 1,
  "name": "Es Teh Manis",
  "sku": "MIN-001",
  "selling_price": 5000,
  "unit": "cup",
  "hpp": 1500,
  "stock": 12,
  "low_stock_threshold": 10,
  "is_active": true,
  "business_id": 1
}
```

- `hpp` & `stock` dihitung runtime (join `product_costs`, `inventory_items`).
- `sku` & `low_stock_threshold` adalah **kontrak tambahan** yang belum ada di data dictionary → **perlu keputusan**: apakah ditambah ke tabel, atau tetap derived/sidecar.

---

## 3.3 Product — field `unit` & `business_id` hilang di frontend

**Frontend:** tidak memakai `unit` maupun `business_id`.

**Dokumen:** keduanya wajib ada di tabel `products`.

**Rekomendasi Backend:** backend tetap menyimpan & mengembalikan `unit` (data dictionary). Tidak masalah bila frontend mengabaikannya; ditulis di sini agar backend tidak menghapus kolom hanya karena tidak dipakai UI.

---

## 3.4 Enumerasi `ProductMovementType` — ✅ RESOLVED

**Keputusan:** API Contract bab 9.2 adalah acuan — terminology lowercase
`received / waste / adjustment / sale`. Backend menerima & mengembalikan nilai
lowercase yang sama (response konsisten dengan request), dipetakan ke enum DB
`RESTOCK / SALE / ADJUSTMENT / WASTE` di `inventory_service.py`. Frontend
`types.ts` diselaraskan menjadi `"received" | "waste" | "adjustment" | "sale"`
(alias `issued` dihapus). Implementasi: commit Fase D — lihat
`documents/laporan-backend-reconciliation-DATARA.md`.

**Status sebelumnya (referensi):**
- Frontend: `"received" | "issued" | "adjustment" | "sale"` (types.ts:10).
- Dokumen: `inventory_movements.movement_type` = `RESTOCK / SALE / ADJUSTMENT / WASTE` (Data Dictionary 9.2).
- `issued` → tidak ada padanan; `WASTE` → tidak ada padanan di frontend.

---

## 3.5 `InventoryLog.stock_after` dan `note`

**Frontend:** `InventoryLog` butuh `stock_after` dan `note` (types.ts:39-48). Demo memakai `quantity` negatif untuk penjualan.

**Dokumen:** `inventory_movements` punya `quantity` (jumlah perubahan), `movement_date`, `reference_id`; **tidak ada** `stock_after` / `note`.

**Rekomendasi Backend:** `stock_after` dapat dihitung runtime (current_stock + jejak movement) atau ditambahkan sebagai kolom snapshot. `note` untuk keterangan bebas perlu kolom baru. **Perlu keputusan**: tambah kolom `note` ke `inventory_movements`.

---

## 3.6 `Transaction` — field tambahan

**Frontend:** `reference_number`, `customer_name`, `subtotal`, `discount`, `total` (types.ts:56-66).

**Dokumen:** `sales_transactions` hanya: `transaction_date`, `total_amount`, timestamps. TIDAK ada: reference_number, customer_name, discount, subtotal, status.

**Rekomendasi Backend:** Endpoint transaksi akan mengembalikan field frontend:
- `total` → diisi dari `total_amount` (alias), atau kolom `total` dipakai menggantikan `total_amount`.
- `subtotal`, `discount` → perlu kolom baru bila transaksi memang punya diskon.
- `reference_number` → bisa dibangkitkan backend dari pola `TRX-{date}-{seq}`.
- `customer_name` → perlu kolom baru (nullable).

**Perlu keputusan**: apakah MVP menyimpan diskon & nama pelanggan.

---

## 3.7 Tidak ada `status` transaksi (gap Business Rules)

**Frontend:** tidak ada field status transaksi.

**Dokumen:** Business Rules 6.3 menyatakan transaksi yang dibatalkan **tidak** dipakai dalam revenue, analisis, forecast, dan perhitungan stok. Namun Data Dictionary `sales_transactions` **tidak memiliki kolom `status`**.

**Rekomendasi Backend:** Tambah kolom `status` pada `sales_transactions` (mis. `COMPLETED` / `CANCELLED`). Semua query analitik wajib memfilter hanya transaksi valid. **Gap di dokumen — perlu disinkronkan ke Data Dictionary.**

---

## 3.8 `TransactionItem` tanpa `unit_hpp`

**Frontend:** `TransactionItem` hanya `product_id`, `quantity`, `unit_price` (types.ts:50-54).

**Dokumen:** `sales_transaction_items` menyimpan `subtotal` dan `unit_hpp` (snapshot HPP agar profitabilitas historis tidak berubah).

**Rekomendasi Backend:** backend akan **menyimpan** `unit_hpp` & `subtotal` di DB (sesuai data dictionary) dan tetap mengembalikan field yang frontend butuhkan. Tidak ada konflik — hanya catatan bahwa backend butuh data ekstra ini.

---

## 3.9 `Cost` generic vs dua tabel biaya

**Frontend:** `Cost` generic: `name`, `amount`, `category`, `occurs_at`, `notes` (types.ts:68-76).

**Dokumen:** memisahkan dua entitas:
- `product_costs` — komponen HPP per produk (`cost_type`, `cost_per_unit`).
- `operating_expenses` — biaya operasional (`expense_type`, `amount`, `expense_date`).

**Rekomendasi Backend:** Dua endpoint terpisah (`/product-costs`, `/operating-expenses`). Jika frontend ingin satu daftar "biaya", backend sediakan endpoint gabungan read-only. **Perlu keputusan**: apakah UI biaya menampilkan keduanya dalam satu halaman.

---

## 3.10 `Decision` generic vs tabel recommendation

**Frontend:** `Decision` generic dengan `type ("pricing"|"restock")`, `status ("recommended"|"applied"|"dismissed")`, `payload` (types.ts:78-89).

**Dokumen:** dua tabel terpisah:
- `pricing_recommendations` — status PENDING/ACCEPTED/DISMISSED/EXPIRED.
- `restock_recommendations` — status yang sama.

**Rekomendasi Backend:** Backend tetap memakai tabel data dictionary, tetapi endpoint list rekomendasi dapat memetakan ke bentuk `Decision` frontend. Nilai status perlu disinkronkan: `recommended` → `PENDING`, `applied` → `ACCEPTED`. **Perlu keputusan**: skema penggabungan dua rekomendasi dalam satu list.

---

## 3.11 `PricingRecommendation` — target margin

**Frontend:** `target_margin_percent`, `actual_margin_percent`, `reasoning` (types.ts:91-101). Halaman pricing punya slider target margin.

**Dokumen:** `pricing_recommendations` punya `current_price`, `current_hpp`, `recommended_price`, `estimated_margin`, `reason_code`, `reason`. **Target margin TIDAK tersimpan di mana pun** di data dictionary (Business Rules 4.8 menyebut target margin ditentukan user).

**Rekomendasi Backend:** `target_margin_percent` harus menjadi parameter input (query/body), bukan disimpan per rekomendasi. Atau ditambah kolom di `business_configurations`. `reasoning` → dihasilkan dari `reason`/`reason_code`. **Gap di dokumen — perlu keputusan.**

---

## 3.12 `RestockRecommendation` — field & status

**Frontend:** `low_stock_threshold`, `days_of_supply`, `suggested_quantity`, `urgency ("critical"|"low"|"healthy")`, `reasoning` (types.ts:103-113).

**Dokumen:** `restock_recommendations` punya `current_stock`, `forecasted_demand`, `safety_days`, `recommended_quantity`, `reason_code`, `status`. Status stok menurut Business Rules 8.5: **Aman / Perlu Restock / Prioritas Restock**.

**Perbedaan:**
- `urgency` ("critical"/"low"/"healthy") vs status stok (Aman/Perlu Restock/Prioritas Restock) — dua bahasa berbeda.
- `low_stock_threshold`, `days_of_supply` — tidak ada di data dictionary (derived).
- `suggested_quantity` ↔ `recommended_quantity` (perlu alias).

**Rekomendasi Backend:** Endpoint `GET /restock-recommendations` mengembalikan field frontend; backend memetakan status stok internal ke `urgency`: Prioritas Restock → `critical`, Perlu Restock → `low`, Aman → `healthy`. **Perlu keputusan**: apakah frontend memakai terminologi Aman/Perlu/Prioritas atau tetap critical/low/healthy.

---

## 3.13 `BusinessHealth.label` ("Cukup")

**Frontend:** `BusinessHealth = { score, label }` (types.ts:115-118). Demo memakai label "Sehat" / "Cukup" / "Perlu Perhatian".

**Dokumen:** `business_health_assessments.health_status` = `SEHAT / PERLU_PERHATIAN / BERISIKO` (Data Dictionary 15.1). Business Rules 13.12 menambah `INSUFFICIENT_DATA` untuk data kurang.

**Rekomendasi Backend:** API mengirim `health_status` sesuai data dictionary. Frontend perlu memetakan: SEHAT → "Sehat", PERLU_PERHATIAN → "Perlu Perhatian", BERISIKO → "Berisiko". Label "Cukup" dari demo **tidak valid** — harus diganti. Score opsional dikirim bila tersedia.

---

## 3.14 `ProductForecast` — field derived

**Frontend:** `model`, `method`, `next_period`, `predicted_units`, `confidence`, `trend`, `points[]`, `reasoning` (types.ts:140-152).

**Dokumen:** `forecast_results` hanya menyimpan snapshot: `forecast_date`, `predicted_quantity`, `model_version`, `generated_at`. Field `confidence`, `trend`, `points[]` (deret waktu), `method`, `reasoning` **tidak tersimpan**.

**Rekomendasi Backend:** Field derived dihitung runtime dari data riwayat + hasil forecast:
- `predicted_units` ↔ `predicted_quantity`.
- `model`/`model_version` → dikirim dari kolom `model_version`.
- `points[]` (actual + forecast per periode) → dibangun backend dari riwayat penjualan + prediksi.
- `confidence`, `trend`, `reasoning` → hasil komputasi engine (tidak disimpan permanen).

---

## 3.15 Forecast — status INSUFFICIENT

**Frontend:** `ProductForecast` tidak punya status khusus.

**Dokumen:** Business Rules 8.3 & 13.11: jika data penjualan < 14 hari, `Forecast = NULL` + `Forecast Status = INSUFFICIENT`. Jangan pernah memproduksi angka palsu.

**Rekomendasi Backend:** Saat data tidak cukup, endpoint forecast mengembalikan `predicted_units: null` + flag `insufficient: true` (atau field `status: "INSUFFICIENT"`). **Perlu keputusan**: penambahan field `status`/`insufficient` di kontrak frontend.

---

## 3.16 `ProductClass` enum

**Frontend:** `ProductClass = "profitable" | "potential" | "evaluate"` (types.ts:154); label "Menguntungkan"/"Berpotensi"/"Perlu Evaluasi".

**Dokumen:** Business Rules 13.6 & PRD FR-004 menyebut klasifikasi produk (margin & penjualan) namun **tidak menetapkan nama enum baku**. Klasifikasi bersifat derived dari decision engine.

**Rekomendasi Backend:** Backend mengembalikan `classification` sesuai enum frontend (`profitable`/`potential`/`evaluate`) + `label` + `reason`. Threshold margin/sales menjadi konstanta engine yang bisa disepakati.

---

## 3.17 `DecisionRecord` / `Decisions_Applied` (gap dokumen)

**Frontend:** `DecisionRecord` = rekomendasi yang **sudah diterapkan** + monitoring (`applied_at`, `metrics_before`, `metrics_after`, `status improved/flat/regressed`, `outcome_notes`) (types.ts:156-167). Halaman `/decisions` memakainya.

**Dokumen:** Data Dictionary **tidak memiliki tabel** untuk keputusan terapan. AGENTS.md menyebut rencana entitas `Decisions_Applied`, tetapi belum masuk data dictionary.

**Rekomendasi Backend:** Tambah tabel `decisions_applied` (atau `applied_decisions`) berisi: type, title, summary, reasoning, applied_at, metrics_before (JSON), metrics_after (JSON), status, outcome_notes + FK ke business & (opsional) recommendation asal. **Gap di dokumen — perlu keputusan & sinkronisasi Data Dictionary.**

---

## 3.18 `GrowthStage` vs `growth_recommendations`

**Frontend:** `GrowthStage` = **roadmap/tahapan** pertumbuhan: `status ("done"|"current"|"next"|"upcoming")`, `metric_1`, `metric_1_value`, `metric_1_target`, `next_step` (types.ts:169-178). Halaman `/growth` menampilkan progress per tahap.

**Dokumen:** `growth_recommendations` = **daftar rekomendasi**: `category`, `title`, `description`, `priority (LOW/MEDIUM/HIGH)`, `status (ACTIVE/COMPLETED/DISMISSED/EXPIRED)`.

**Perbedaan:** bentuk data sangat berbeda — roadmap vs list rekomendasi.

**Rekomendasi Backend:** Dua kemungkinan (pilih bersama):
1. Backend sediakan endpoint `GET /growth/stages` yang menghitung progress tahapan dari metrik nyata (revenue, margin, dst.) → sesuai UI frontend saat ini.
2. Backend sediakan `growth_recommendations` (data dictionary) dan frontend mengubah halaman `/growth` menjadi list rekomendasi.

**Perlu keputusan besar** — memengaruhi desain UI dan backend.

---

## 3.19 SKU prefix = kategori (MIN/FOOD/SNK)

**Frontend:** SKU memakai prefix kategori `MIN`/`FOOD`/`SNK` yang dipakai untuk filter produk (`/products`), class, dan `category_breakdown` di dashboard (demo-data.ts; laporan-frontend point 7).

**Dokumen:** Data Dictionary **tidak memiliki** field `sku` maupun `category`/kategori produk. `category_breakdown` tidak bisa direproduksi dari struktur yang ada.

**Rekomendasi Backend:** Dua opsi:
1. Tambah field `sku` (atau `category`) pada `products` agar breakdown & filter bisa diserve backend.
2. Backend sediakan `category_breakdown` sebagai endpoint agregat (derived), tanpa kolom kategori.

**Perlu keputusan** — opsi 1 lebih aman karena frontend memakai prefix SKU sebagai identitas kategori.

---

## 3.20 `business_configurations` hanya `safety_days`

**Frontend:** Demo memakai konstanta `TARGET_MARGIN = 0.3` dan `LEAD_TIME_DAYS = 3` (demo-data.ts:16-17) sebagai nilai default.

**Dokumen:** `business_configurations` hanya menyimpan `safety_days` (default 3, rentang 0–30). Business Rules 7.3 (`lead_time`), 7.4 (`safety_days`), 4.8 (`target margin` user) **tidak semua** diwakili kolom.

**Rekomendasi Backend:** Tambah kolom `lead_time` (default 3) dan `target_margin` (default 30%) ke `business_configurations`. Konstanta demo frontend akan diganti oleh nilai konfigurasi dari backend. **Gap di dokumen — perlu keputusan.**

---

# 4. Daftar Keputusan yang Dibutuhkan

Ringkasan item yang butuh kesepakatan bersama (frontend + backend + tim produk):

| # | Topik | Opsi Singkat |
|---|---|---|
| A | `sku` & `low_stock_threshold` produk | Kolom DB baru vs derived |
| B | Enum movement type | ✅ Decided → lowercase `received/waste/adjustment/sale` (API Contract 9.2) |
| C | `note` di inventory_movements | Tambah kolom vs tanpa note |
| D | Diskon & customer_name transaksi | Simpan di DB vs tidak (MVP) |
| E | Kolom `status` transaksi | Wajib (COMPLETED/CANCELLED) |
| F | Target margin & lead_time config | Tambah kolom `business_configurations` |
| G | Tabel `decisions_applied` | Tambah tabel baru |
| H | Growth: roadmap (`/growth/stages`) vs list `growth_recommendations` | Pilih bentuk data |
| I | Kategori produk (SKU prefix) | Tambah kolom sku/category vs endpoint agregat |
| J | Status INSUFFICIENT di kontrak forecast | Tambah field `status`/`insufficient` |
| K | Status restock: urgency vs Aman/Perlu/Prioritas | Pilih terminologi API |

---

# 5. Lampiran — Peta Field Frontend → Sumber Backend

| Field Frontend | Tabel / Sumber Backend | Tersimpan? |
|---|---|---|
| `User.role` | — | Tidak ada (hapus/monovalue) |
| `Product.sku` | `products.sku` (baru) / derived | **Perlu keputusan** |
| `Product.hpp` | computed dari `product_costs` | Tidak (runtime) |
| `Product.stock` | `inventory_items.current_stock` | Ya (di tabel lain) |
| `Product.low_stock_threshold` | `products.low_stock_threshold` (baru) | **Perlu keputusan** |
| `InventoryLog.stock_after` | computed / kolom snapshot | **Perlu keputusan** |
| `InventoryLog.note` | `inventory_movements.note` (baru) | **Perlu keputusan** |
| `Transaction.reference_number` | `sales_transactions.reference_number` (baru) | **Perlu keputusan** |
| `Transaction.customer_name` | `sales_transactions.customer_name` (baru) | **Perlu keputusan** |
| `Transaction.subtotal` | `sales_transactions.subtotal` (baru) | **Perlu keputusan** |
| `Transaction.discount` | `sales_transactions.discount` (baru) | **Perlu keputusan** |
| `Transaction.total` | `sales_transactions.total_amount` (alias) | Ya |
| `TransactionItem.unit_price` | `sales_transaction_items.unit_price` | Ya |
| `TransactionItem.quantity` | `sales_transaction_items.quantity` | Ya |
| `Cost.*` | `product_costs` + `operating_expenses` | Ya (dua tabel) |
| `PricingRecommendation.recommended_price` | `pricing_recommendations.recommended_price` | Ya |
| `PricingRecommendation.target_margin_percent` | `business_configurations.target_margin` (baru) / input | **Perlu keputusan** |
| `RestockRecommendation.suggested_quantity` | `restock_recommendations.recommended_quantity` (alias) | Ya |
| `RestockRecommendation.urgency` | mapping dari status stok (Aman/Perlu/Prioritas) | Derived |
| `BusinessHealth.label` | `business_health_assessments.health_status` | Ya |
| `ProductForecast.predicted_units` | `forecast_results.predicted_quantity` (alias) | Ya |
| `ProductForecast.points[]` | computed dari riwayat + forecast | Derived |
| `DecisionRecord.*` | `decisions_applied` (tabel baru) | **Perlu keputusan** |
| `GrowthStage.*` | `growth_recommendations` / endpoint stages | **Perlu keputusan** |

---

# 6. Catatan Penutup

- Dokumen ini **tidak mengubah** `frontend/src/lib/types.ts` maupun `demo-data.ts`.
- Backend akan membangun skema & kontrak API **mengacu Data Dictionary sebagai baseline**, dengan penyesuaian di atas.
- Setiap item **Perlu keputusan** harus dirapatkan bersama sebelum API dikunci agar tidak ada rework dua arah.

