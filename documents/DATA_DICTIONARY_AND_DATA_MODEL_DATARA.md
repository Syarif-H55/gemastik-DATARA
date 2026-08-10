# DATA DICTIONARY & DATA MODEL
## DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM

**Status:** FINAL  
**Scope:** MVP  
**Primary User:** Pemilik UMKM makanan dan minuman skala mikro  
**Purpose:** Menjadi acuan bersama untuk database, backend, API, analytical engine, AI context, dan pengembangan frontend DATARA.

---

# 1. Tujuan Dokumen

Dokumen ini mendefinisikan struktur data utama DATARA, hubungan antar-entity, aturan penyimpanan analytical result, serta batas antara data source, decision engine, dan AI/LLM.

Prinsip utama:

> Backend/Decision Engine menghasilkan angka dan keputusan berbasis data, rule, atau model. AI/LLM menjelaskan hasil tersebut dan memberikan saran dalam bahasa yang mudah dipahami.

AI bukan source of truth untuk angka bisnis.

---

# 2. Prinsip Data Model

- DATARA berorientasi pada satu pemilik UMKM dengan satu business utama pada MVP.
- Data transaksi dan operasional menjadi source data utama.
- Financial metrics seperti Revenue, COGS, Gross Profit, Gross Margin, dan Net Profit dihitung dari source data.
- HPP produk dihitung per unit.
- Fixed Cost dipisahkan sebagai Operating Expense.
- Variable Cost yang berhubungan langsung dengan produk masuk HPP.
- Forecast disimpan sebagai historical result.
- Recommendation disimpan sebagai historical decision.
- Business Health disimpan sebagai historical assessment.
- Business Target ditentukan user dan tidak diubah otomatis oleh sistem.
- Business Context untuk AI dibuat secara runtime berdasarkan data yang relevan.
- AI tidak boleh mengarang angka bisnis.
- Authorization dilakukan di backend berdasarkan business ownership.

---

# 3. User & Business

## 3.1 users

Menyimpan akun pengguna DATARA.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID user |
| name | VARCHAR(100) | NO | | Nama user |
| email | VARCHAR(150) | NO | UNIQUE | Email login |
| password | VARCHAR(255) | NO | | Password hash |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

### Authentication

MVP menggunakan email + password.

Password wajib disimpan dalam bentuk hash dan tidak boleh disimpan plaintext.

## 3.2 businesses

Menyimpan informasi usaha milik user.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID business |
| user_id | BIGINT UNSIGNED | NO | FK, UNIQUE | Pemilik business |
| name | VARCHAR(150) | NO | | Nama usaha |
| business_type | VARCHAR(100) | NO | | Jenis usaha |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

### Relationship

`users 1:1 businesses`

### Access

User hanya dapat mengakses business yang dimilikinya.

MVP tidak menggunakan role Admin/Staff/Manager dalam business domain. Pengguna utama adalah Business Owner.

---

# 4. Business Configuration

## 4.1 business_configurations

Menyimpan konfigurasi yang memengaruhi cara decision engine bekerja.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID configuration |
| business_id | BIGINT UNSIGNED | NO | FK, UNIQUE | Business |
| safety_days | DECIMAL(5,2) | NO | | Safety buffer dalam hari |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

### Safety Days

- Default awal: 3 hari.
- Dapat dikonfigurasi user.
- Validasi MVP: `0 <= safety_days <= 30`.
- Safety Days digunakan oleh Smart Restock.

Relationship:

`businesses 1:1 business_configurations`

---

# 5. Business Target

## 5.1 business_targets

Menyimpan target bisnis yang ditentukan user.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID target |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| target_type | ENUM | NO | | SALES / PROFIT |
| target_value | DECIMAL(15,2) | NO | | Nilai target |
| period_type | ENUM | NO | | MONTHLY |
| start_date | DATE | NO | | Awal periode |
| end_date | DATE | NO | | Akhir periode |
| status | ENUM | NO | | ACTIVE / COMPLETED / CANCELLED |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

### Target MVP

- `SALES`
- `PROFIT`

Periode MVP:

- `MONTHLY`

Target ditentukan user dan tidak diubah otomatis oleh sistem.

### Target Achievement

Sales Achievement:

`Actual Sales / Target Sales × 100%`

Profit Achievement:

`Actual Profit / Target Profit × 100%`

---

# 6. Product

## 6.1 products

Menyimpan produk yang dijual business.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID produk |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| name | VARCHAR(150) | NO | | Nama produk |
| selling_price | DECIMAL(15,2) | NO | | Harga jual saat ini |
| unit | VARCHAR(30) | NO | | Satuan produk |
| is_active | BOOLEAN | NO | | Status produk |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

Produk yang tidak lagi dijual sebaiknya dinonaktifkan daripada menghapus historical record.

---

# 7. Product Cost & HPP

## 7.1 product_costs

Menyimpan komponen biaya produk yang digunakan untuk menghitung HPP.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID cost |
| product_id | BIGINT UNSIGNED | NO | FK | Produk |
| cost_type | ENUM | NO | | RAW_MATERIAL / PACKAGING / DIRECT_LABOR / PRODUCTION_OVERHEAD |
| name | VARCHAR(150) | NO | | Nama komponen biaya |
| cost_per_unit | DECIMAL(15,2) | NO | | Biaya per unit |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

### HPP

HPP/unit:

`Bahan Baku + Kemasan + Tenaga Kerja Langsung + Alokasi Overhead Produksi`

### Cost Classification

**Masuk HPP:**
- Bahan baku.
- Kemasan.
- Tenaga kerja langsung.
- Overhead produksi yang dialokasikan.

**Tidak masuk HPP:**
- Sewa.
- Gaji tetap.
- Administrasi.
- Operating expense lainnya.

Biaya seperti listrik/gas yang sulit ditelusuri langsung ke satu produk dapat dimasukkan sebagai production overhead dengan alokasi sederhana.

---

# 8. Sales Transaction

## 8.1 sales_transactions

Menyimpan transaksi penjualan.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID transaksi |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| transaction_date | DATETIME | NO | | Waktu transaksi |
| total_amount | DECIMAL(15,2) | NO | | Total transaksi |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

## 8.2 sales_transaction_items

Menyimpan produk di dalam transaksi.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID item |
| transaction_id | BIGINT UNSIGNED | NO | FK | Transaksi |
| product_id | BIGINT UNSIGNED | NO | FK | Produk |
| quantity | DECIMAL(12,2) | NO | | Jumlah |
| unit_price | DECIMAL(15,2) | NO | | Harga saat transaksi |
| subtotal | DECIMAL(15,2) | NO | | Quantity × Unit Price |
| unit_hpp | DECIMAL(15,2) | NO | | HPP/unit yang digunakan |
| created_at | TIMESTAMP | NO | | Waktu dibuat |

`unit_hpp` dapat disimpan sebagai snapshot agar historical profitability tidak berubah hanya karena HPP produk diperbarui di kemudian hari.

---

# 9. Inventory

## 9.1 inventory_items

Menyimpan kondisi stok produk.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID inventory |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| product_id | BIGINT UNSIGNED | NO | FK, UNIQUE | Produk |
| current_stock | DECIMAL(12,2) | NO | | Stok saat ini |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

## 9.2 inventory_movements

Menyimpan riwayat perubahan stok.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID movement |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| product_id | BIGINT UNSIGNED | NO | FK | Produk |
| movement_type | ENUM | NO | | RESTOCK / SALE / ADJUSTMENT / WASTE |
| quantity | DECIMAL(12,2) | NO | | Jumlah perubahan |
| movement_date | DATETIME | NO | | Waktu movement |
| reference_id | BIGINT UNSIGNED | YES | | ID sumber jika ada |
| created_at | TIMESTAMP | NO | | Waktu dibuat |

Inventory menjadi source data untuk Smart Restock.

---

# 10. Operating Expense

## 10.1 operating_expenses

Menyimpan biaya operasional yang tidak dimasukkan sebagai HPP produk.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID expense |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| expense_type | ENUM | NO | | RENT / FIXED_SALARY / ADMINISTRATIVE / OTHER |
| name | VARCHAR(150) | NO | | Nama biaya |
| amount | DECIMAL(15,2) | NO | | Nilai biaya |
| expense_date | DATE | NO | | Tanggal biaya |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

Fixed Cost seperti sewa dan gaji tetap dicatat di sini.

---

# 11. Financial Metrics

DATARA tidak menyimpan financial metrics utama sebagai source table terpisah pada MVP.

Nilai dihitung dari source data.

### Revenue

`Σ sales_transaction_items.subtotal`

### COGS

`Σ sales_transaction_items.quantity × unit_hpp`

### Gross Profit

`Revenue - COGS`

### Gross Margin

`Gross Profit / Revenue × 100%`

### Net Profit

`Gross Profit - Operating Expense`

Financial metrics dapat dihitung per periode, terutama bulanan.

---

# 12. Forecast Result

## 12.1 forecast_results

Menyimpan hasil forecasting.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID forecast |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| product_id | BIGINT UNSIGNED | NO | FK | Produk |
| forecast_date | DATE | NO | | Tanggal prediksi |
| predicted_quantity | DECIMAL(12,2) | NO | | Prediksi penjualan |
| model_version | VARCHAR(50) | YES | | Versi model |
| generated_at | TIMESTAMP | NO | | Waktu forecast dibuat |
| created_at | TIMESTAMP | NO | | Waktu record dibuat |

Forecast disimpan sebagai snapshot historical. Forecast baru tidak menimpa forecast lama.

Forecast dibuat per produk dan tanggal.

---

# 13. Smart Restock Recommendation

## 13.1 restock_recommendations

Menyimpan rekomendasi Smart Restock.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID recommendation |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| product_id | BIGINT UNSIGNED | NO | FK | Produk |
| generated_at | TIMESTAMP | NO | | Waktu recommendation |
| current_stock | DECIMAL(12,2) | NO | | Stok saat recommendation |
| forecasted_demand | DECIMAL(12,2) | NO | | Prediksi kebutuhan |
| safety_days | DECIMAL(5,2) | NO | | Safety Days saat recommendation |
| recommended_quantity | DECIMAL(12,2) | NO | | Jumlah restock |
| reason_code | VARCHAR(50) | YES | | Alasan terstruktur |
| status | ENUM | NO | | Status recommendation |

Status:

- `PENDING`
- `ACCEPTED`
- `DISMISSED`
- `EXPIRED`

Recommendation bukan actual restock. Actual restock tetap tercatat sebagai `inventory_movements`.

---

# 14. Smart Pricing Recommendation

## 14.1 pricing_recommendations

Menyimpan historical recommendation Smart Pricing.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID recommendation |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| product_id | BIGINT UNSIGNED | NO | FK | Produk |
| generated_at | TIMESTAMP | NO | | Waktu recommendation |
| current_price | DECIMAL(15,2) | NO | | Harga saat recommendation |
| current_hpp | DECIMAL(15,2) | NO | | HPP saat recommendation |
| recommended_price | DECIMAL(15,2) | NO | | Harga rekomendasi |
| estimated_margin | DECIMAL(5,2) | NO | | Estimasi margin |
| reason_code | VARCHAR(50) | YES | | Alasan terstruktur |
| reason | TEXT | YES | | Penjelasan rule-based |
| status | ENUM | NO | | Status |

Status:

- `PENDING`
- `ACCEPTED`
- `DISMISSED`
- `EXPIRED`

Smart Pricing harus tetap realistis dan dapat menghasilkan profit. User input menjadi faktor utama, sementara faktor pendukung dapat digunakan oleh decision engine.

---

# 15. Business Health Assessment

## 15.1 business_health_assessments

Menyimpan historical assessment kondisi bisnis.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID assessment |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| period_start | DATE | NO | | Awal periode |
| period_end | DATE | NO | | Akhir periode |
| health_status | ENUM | NO | | SEHAT / PERLU_PERHATIAN / BERISIKO |
| score | DECIMAL(5,2) | YES | | Internal score |
| generated_at | TIMESTAMP | NO | | Waktu assessment |
| created_at | TIMESTAMP | NO | | Waktu dibuat |

Business Health menggunakan kombinasi indikator, misalnya:

- Revenue.
- Profit.
- Margin.
- Sales Trend.
- Target Achievement.

UI hanya perlu menampilkan tiga status:

- `SEHAT`
- `PERLU_PERHATIAN`
- `BERISIKO`

Score internal tidak wajib ditampilkan.

---

# 16. Growth Recommendation

## 16.1 growth_recommendations

Menyimpan rekomendasi strategis yang dihasilkan Growth Map.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID recommendation |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| generated_at | TIMESTAMP | NO | | Waktu dibuat |
| category | ENUM | NO | | PRICING / SALES / INVENTORY / PROFITABILITY |
| title | VARCHAR(200) | NO | | Judul |
| description | TEXT | NO | | Penjelasan |
| priority | ENUM | NO | | LOW / MEDIUM / HIGH |
| status | ENUM | NO | | ACTIVE / COMPLETED / DISMISSED / EXPIRED |

Growth Map menggunakan:

- Historical Performance.
- Target.
- Business Health.
- Sales Trend.
- Profitability.
- Recommendation dari decision engine.

Growth Map diarahkan untuk membantu pertumbuhan bisnis, misalnya peningkatan keuntungan atau pencapaian target penjualan dibanding periode sebelumnya.

---

# 17. AI Business Assistant

## 17.1 ai_conversations

Menyimpan sesi percakapan.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID conversation |
| business_id | BIGINT UNSIGNED | NO | FK | Business |
| title | VARCHAR(150) | YES | | Judul conversation |
| status | ENUM | NO | | ACTIVE / ARCHIVED |
| created_at | TIMESTAMP | NO | | Waktu dibuat |
| updated_at | TIMESTAMP | NO | | Waktu diperbarui |

## 17.2 ai_messages

Menyimpan pesan conversation.

| Field | Type | Null | Key | Description |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | PK | ID message |
| conversation_id | BIGINT UNSIGNED | NO | FK | Conversation |
| role | ENUM | NO | | USER / ASSISTANT |
| content | TEXT | NO | | Isi pesan |
| created_at | TIMESTAMP | NO | | Waktu pesan |

---

# 18. AI Context Architecture

Business context dibuat secara runtime.

```text
User Question
      ↓
Backend Context Builder
      ↓
Relevant Business Data
      +
Recent Conversation History
      ↓
Structured Context
      ↓
LLM
      ↓
Explanation / Advice
```

Tidak perlu menyimpan generated context sebagai entity domain pada MVP.

## AI Scope

AI boleh:

- Menjelaskan kondisi bisnis.
- Menjelaskan recommendation DATARA.
- Menjawab pertanyaan tentang penjualan, stok, harga, HPP, profit, dan bisnis.
- Memberikan saran bisnis umum yang masih relevan.

AI tidak boleh:

- Mengarang angka bisnis.
- Menggantikan decision engine.
- Mengambil data business lain.
- Menjadi source of truth financial calculation.

Jika data tidak tersedia, AI harus menyatakan keterbatasan data.

---

# 19. Reason Code

Recommendation menggunakan structured reason code agar backend dan AI memiliki konteks yang konsisten.

Contoh:

- `LOW_MARGIN`
- `HIGH_DEMAND`
- `LOW_STOCK`
- `DECLINING_SALES`
- `TARGET_BEHIND`

Reason code dapat dikembangkan sesuai kebutuhan decision engine.

---

# 20. Entity Relationship

```text
users
  │
  └── 1:1 ── businesses
                │
                ├── 1:1 ── business_configurations
                │
                ├── 1:N ── business_targets
                │
                ├── 1:N ── products
                │              │
                │              └── 1:N ── product_costs
                │
                ├── 1:N ── sales_transactions
                │              │
                │              └── 1:N ── sales_transaction_items
                │
                ├── 1:N ── inventory_items
                │
                ├── 1:N ── inventory_movements
                │
                ├── 1:N ── operating_expenses
                │
                ├── 1:N ── forecast_results
                │
                ├── 1:N ── restock_recommendations
                │
                ├── 1:N ── pricing_recommendations
                │
                ├── 1:N ── business_health_assessments
                │
                ├── 1:N ── growth_recommendations
                │
                └── 1:N ── ai_conversations
                                  │
                                  └── 1:N ── ai_messages
```

---

# 21. Analytical Data Flow

```text
Products + Product Costs
          │
          ↓
       HPP/Unit
          │
          ↓
    Smart Pricing
          │
          ↓
Pricing Recommendation


Sales Transactions
          │
          ↓
  Sales Forecasting
          │
          ↓
 Inventory + Safety Days
          │
          ↓
 Smart Restock Recommendation


Sales + HPP + Operating Expenses
          │
          ↓
 Financial Analysis
          │
          ├── Revenue
          ├── COGS
          ├── Gross Profit
          ├── Gross Margin
          └── Net Profit
          │
          ↓
 Business Health
          │
          ↓
      Growth Map
          │
          ↓
 Business Recommendations
          │
          ↓
   Business Assistant
          │
          ↓
          AI
```

---

# 22. Source of Truth

| Data / Decision | Source of Truth |
|---|---|
| Product | Backend database |
| HPP | Product cost data + backend calculation |
| Revenue | Sales transactions |
| COGS | Transaction items + HPP snapshot |
| Gross Profit | Backend calculation |
| Net Profit | Backend calculation |
| Inventory | Inventory records + movements |
| Forecast | Forecasting engine |
| Smart Restock | Decision engine |
| Smart Pricing | Decision engine |
| Business Health | Rule-based analytical engine |
| Growth Recommendation | Decision engine |
| Business Target | User input |
| AI Explanation | LLM, grounded on backend context |

---

# 23. Constraints & Validation

## User

- Email must be unique.
- Password must be hashed.

## Business

- `user_id` unique for MVP.
- User can only access owned business.

## Business Configuration

- One configuration per business.
- `0 <= safety_days <= 30`.

## Business Target

- `target_value > 0`.
- `start_date <= end_date`.
- MVP target type: SALES / PROFIT.
- MVP period: MONTHLY.

## Product

- Selling price should be non-negative.
- Product can be inactive without deleting historical transaction data.

## Product Cost

- Cost should be non-negative.
- HPP calculated per unit.

## Sales

- Quantity must be positive.
- Unit price should be non-negative.
- Subtotal = quantity × unit_price.

## Inventory

- Quantity must be valid according to movement type.
- Historical movement should not be deleted casually.

## Operating Expense

- Amount must be positive.
- Expense belongs to one business.

## Recommendations

- Recommendation belongs to one business and product where applicable.
- Recommendation status must use defined enum values.
- Actual restock is recorded separately from recommendation.

---

# 24. Index Recommendations

Recommended indexes:

```text
users:
  UNIQUE(email)

businesses:
  UNIQUE(user_id)

business_configurations:
  UNIQUE(business_id)

business_targets:
  INDEX(business_id)
  INDEX(business_id, target_type)
  INDEX(start_date, end_date)

products:
  INDEX(business_id)
  INDEX(business_id, is_active)

product_costs:
  INDEX(product_id)

sales_transactions:
  INDEX(business_id, transaction_date)

sales_transaction_items:
  INDEX(transaction_id)
  INDEX(product_id)

inventory_items:
  UNIQUE(business_id, product_id)

inventory_movements:
  INDEX(business_id, product_id)
  INDEX(movement_date)

operating_expenses:
  INDEX(business_id, expense_date)

forecast_results:
  INDEX(business_id, product_id, forecast_date)

restock_recommendations:
  INDEX(business_id, product_id)
  INDEX(status)

pricing_recommendations:
  INDEX(business_id, product_id)
  INDEX(status)

business_health_assessments:
  INDEX(business_id, period_start, period_end)

growth_recommendations:
  INDEX(business_id, status)

ai_conversations:
  INDEX(business_id)

ai_messages:
  INDEX(conversation_id, created_at)
```

---

# 25. MVP Table Summary

DATARA MVP menggunakan domain tables berikut:

1. `users`
2. `businesses`
3. `business_configurations`
4. `business_targets`
5. `products`
6. `product_costs`
7. `sales_transactions`
8. `sales_transaction_items`
9. `inventory_items`
10. `inventory_movements`
11. `operating_expenses`
12. `forecast_results`
13. `restock_recommendations`
14. `pricing_recommendations`
15. `business_health_assessments`
16. `growth_recommendations`
17. `ai_conversations`
18. `ai_messages`

---

# 26. Data Model Boundary

Beberapa hal sengaja tidak dibuat sebagai tabel MVP:

- Monthly financial snapshot.
- AI context.
- AI memory.
- AI embeddings.
- AI agent.
- Prompt template.
- Separate admin business role.
- Multiple business per user.
- Complex product category hierarchy.
- Complex accounting ledger.

Alasannya adalah menjaga scope DATARA tetap fokus pada:

```text
Input Business Data
        ↓
Analysis
        ↓
Recommendation
        ↓
Business Decision
```

---

# 27. Final Architecture Principle

Struktur data DATARA mengikuti prinsip:

```text
             USER
               │
               ↓
            BUSINESS
               │
       ┌───────┼────────┐
       ↓       ↓        ↓
    PRODUCTS  SALES   EXPENSES
       │       │        │
       ↓       ↓        ↓
      HPP   FORECAST  PROFIT
       │       │        │
       ↓       ↓        │
    PRICING RESTOCK     │
       │       │        │
       └───────┼────────┘
               ↓
        BUSINESS HEALTH
               ↓
           GROWTH MAP
               ↓
       BUSINESS ASSISTANT
               ↓
              AI
```

---

# 28. Final Design Principle

DATARA memisahkan tiga lapisan:

### Layer 1 — Data

```text
Transactions
Products
Costs
Inventory
Expenses
Targets
```

### Layer 2 — Intelligence / Decision

```text
HPP Calculation
Financial Analysis
Forecasting
Smart Pricing
Smart Restock
Business Health
Growth Map
```

### Layer 3 — AI Interaction

```text
Business Assistant
Explanation
Business Advice
Natural Language Interaction
```

Dengan pemisahan ini, AI tidak mengambil alih fungsi backend. AI menjadi antarmuka cerdas yang membantu user memahami dan menggunakan hasil analisis DATARA.

---

# 29. Document Status

**DATA DICTIONARY & DATA MODEL: FINAL**

Dokumen ini menjadi acuan untuk:

- Database schema.
- Backend model/entity.
- API design.
- Validation.
- Decision engine.
- Forecasting pipeline.
- AI context builder.
- Frontend data requirements.

Perubahan struktur setelah dokumen ini dikunci harus dianggap sebagai perubahan desain dan perlu diperbarui pada dokumen terkait.
