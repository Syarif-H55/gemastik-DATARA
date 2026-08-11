# API CONTRACT / API SPECIFICATION
## DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM

**Status:** FINAL  
**API Version:** v1  
**Base Path:** `/api/v1`  
**Protocol:** HTTPS/HTTP  
**Style:** REST API  
**Backend:** FastAPI  
**Database:** MySQL  
**Data Format:** JSON  
**Naming:** snake_case

---

# 1. API Overview

API DATARA menjadi penghubung antara frontend dan backend.

```text
Frontend
   ↓
REST API
   ↓
FastAPI
   ↓
Business Service / Decision Engine
   ↓
MySQL
```

Backend merupakan source of truth untuk:

- Business data.
- Product data.
- Transaction data.
- Inventory.
- HPP.
- Financial metrics.
- Forecasting.
- Pricing recommendation.
- Restock recommendation.
- Business Health.
- Decision history.
- Growth recommendation.

Frontend tidak mengakses database secara langsung.

---

# 2. API Design Principles

## 2.1 RESTful

Endpoint menggunakan resource-oriented URL.

```text
GET    /products
POST   /products
GET    /products/{id}
PUT    /products/{id}
DELETE /products/{id}
```

Action endpoint digunakan ketika operasi tidak tepat direpresentasikan sebagai CRUD biasa.

Contoh:

```text
POST /pricing/apply
POST /restock/apply
POST /decisions/{id}/apply
```

## 2.2 Versioning

Semua endpoint MVP menggunakan:

```text
/api/v1
```

Contoh:

```text
/api/v1/products
```

## 2.3 JSON

Request dan response menggunakan JSON.

## 2.4 snake_case

Field API menggunakan `snake_case`.

```json
{
  "product_id": 12,
  "current_stock": 25,
  "recommended_quantity": 40
}
```

## 2.5 Backend as Source of Truth

Frontend hanya mengirim input dan menampilkan hasil.

Business calculation dilakukan backend.

## 2.6 Authentication & Authorization

Protected endpoint membutuhkan authenticated user.

Backend wajib melakukan business ownership check.

```text
Authentication
      ↓
Authorization
      ↓
Business Ownership
      ↓
Request Processing
```

---

# 3. Common Response Structure

## 3.1 Success Response

Single resource:

```json
{
  "success": true,
  "data": {}
}
```

List:

```json
{
  "success": true,
  "data": [],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

## 3.2 Error Response

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "selling_price": [
      "Selling price must be greater than or equal to 0."
    ]
  }
}
```

## 3.3 HTTP Status

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Successful request without body |
| 400 | Invalid request |
| 401 | Unauthenticated |
| 403 | Unauthorized |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation error |
| 500 | Internal server error |

---

# 4. Authentication API

## 4.1 Login

```http
POST /api/v1/auth/login
```

Request:

```json
{
  "email": "owner@example.com",
  "password": "password"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "name": "Business Owner",
      "email": "owner@example.com"
    },
    "access_token": "..."
  }
}
```

## 4.2 Current User

```http
GET /api/v1/auth/me
```

Response:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Business Owner",
    "email": "owner@example.com"
  }
}
```

## 4.3 Logout

```http
POST /api/v1/auth/logout
```

Response:

```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

# 5. Business API

## 5.1 Get Business

```http
GET /api/v1/business
```

Response:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Kedai Contoh",
    "business_type": "food_beverage",
    "safety_days": 3
  }
}
```

## 5.2 Update Business

```http
PUT /api/v1/business
```

Request:

```json
{
  "name": "Kedai Contoh",
  "business_type": "food_beverage",
  "safety_days": 3
}
```

`Safety Days` dapat dikonfigurasi user dengan default yang ditentukan sistem.

---

# 6. Product API

## 6.1 List Products

```http
GET /api/v1/products
```

Optional query:

```text
?page=1&per_page=20&search=kopi
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Es Kopi Susu",
      "selling_price": 12000,
      "unit_hpp": 5500,
      "current_stock": 25,
      "stock_unit": "cup",
      "is_active": true
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 1
  }
}
```

## 6.2 Create Product

```http
POST /api/v1/products
```

Request:

```json
{
  "name": "Es Kopi Susu",
  "selling_price": 12000,
  "stock_unit": "cup",
  "current_stock": 25
}
```

Response: `201`

## 6.3 Get Product

```http
GET /api/v1/products/{product_id}
```

## 6.4 Update Product

```http
PUT /api/v1/products/{product_id}
```

## 6.5 Delete / Deactivate Product

```http
DELETE /api/v1/products/{product_id}
```

Deletion should preferably be implemented as deactivation when historical transactions reference the product.

---

# 7. Product Cost & HPP API

## 7.1 Get Product Costs

```http
GET /api/v1/products/{product_id}/costs
```

Response:

```json
{
  "success": true,
  "data": {
    "product_id": 1,
    "raw_material": 3500,
    "packaging": 1000,
    "direct_labor": 500,
    "allocated_overhead": 500,
    "unit_hpp": 5500
  }
}
```

## 7.2 Update Product Costs

```http
PUT /api/v1/products/{product_id}/costs
```

Request:

```json
{
  "raw_material": 3500,
  "packaging": 1000,
  "direct_labor": 500,
  "allocated_overhead": 500
}
```

Backend calculates:

```text
unit_hpp
=
raw_material
+ packaging
+ direct_labor
+ allocated_overhead
```

Fixed cost such as rent and fixed salary is not included in product HPP.

## 7.3 Get Product Profitability

```http
GET /api/v1/products/profitability
```

Optional:

```text
?period_start=2026-08-01&period_end=2026-08-31
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "product_id": 1,
      "product_name": "Es Kopi Susu",
      "unit_hpp": 5500,
      "selling_price": 12000,
      "profit_per_unit": 6500,
      "margin_percentage": 54.17
    }
  ]
}
```

---

# 8. Sales Transaction API

## 8.1 Create Transaction

```http
POST /api/v1/transactions
```

Creating a transaction also updates inventory in the same database transaction.

Request:

```json
{
  "transaction_date": "2026-08-11T10:30:00",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "selling_price": 12000
    }
  ],
  "payment_method": "cash"
}
```

Backend process:

```text
Create Transaction
      ↓
Create Transaction Items
      ↓
Snapshot HPP/unit
      ↓
Calculate Revenue / COGS
      ↓
Create Inventory Movement: sale
      ↓
Decrease Current Stock
      ↓
Commit Transaction
```

All steps succeed or all are rolled back.

Response:

```json
{
  "success": true,
  "data": {
    "id": 101,
    "transaction_date": "2026-08-11T10:30:00",
    "total_amount": 24000,
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "selling_price": 12000,
        "unit_hpp": 5500
      }
    ]
  }
}
```

## 8.2 List Transactions

```http
GET /api/v1/transactions
```

Optional:

```text
?page=1&per_page=20&date_from=2026-08-01&date_to=2026-08-31
```

## 8.3 Get Transaction

```http
GET /api/v1/transactions/{transaction_id}
```

---

# 9. Inventory API

## 9.1 Get Inventory

```http
GET /api/v1/inventory
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "product_id": 1,
      "product_name": "Es Kopi Susu",
      "current_stock": 25,
      "stock_unit": "cup"
    }
  ]
}
```

## 9.2 Create Inventory Movement

```http
POST /api/v1/inventory/movements
```

Request:

```json
{
  "product_id": 1,
  "movement_type": "received",
  "quantity": 30,
  "movement_date": "2026-08-11T11:00:00",
  "notes": "Restock supplier"
}
```

Supported movement types:

```text
sale
received
waste
adjustment
```

Backend updates current stock based on movement type.

## 9.3 Inventory History

```http
GET /api/v1/inventory/movements
```

Optional:

```text
?product_id=1&date_from=2026-08-01&date_to=2026-08-31
```

---

# 10. Finance API

## 10.1 Financial Summary

```http
GET /api/v1/finance/summary
```

Optional:

```text
?period_start=2026-08-01&period_end=2026-08-31
```

Response:

```json
{
  "success": true,
  "data": {
    "revenue": 12500000,
    "cogs": 5000000,
    "gross_profit": 7500000,
    "gross_margin": 60.0,
    "operating_expense": 3500000,
    "net_profit": 4000000
  }
}
```

## 10.2 Operating Expense

```http
GET /api/v1/finance/expenses
POST /api/v1/finance/expenses
PUT /api/v1/finance/expenses/{expense_id}
DELETE /api/v1/finance/expenses/{expense_id}
```

Request:

```json
{
  "expense_date": "2026-08-01",
  "category": "rent",
  "amount": 1500000,
  "description": "Monthly rent"
}
```

Fixed cost seperti rent dan fixed salary dicatat sebagai Operating Expense.

---

# 11. Dashboard API

## 11.1 Dashboard Summary

```http
GET /api/v1/dashboard
```

Optional:

```text
?period_start=2026-08-01&period_end=2026-08-31
```

Response:

```json
{
  "success": true,
  "data": {
    "revenue": 12500000,
    "gross_profit": 7500000,
    "net_profit": 4000000,
    "gross_margin": 60.0,
    "transaction_count": 425,
    "top_product": {
      "product_id": 1,
      "product_name": "Es Kopi Susu",
      "quantity_sold": 180
    },
    "business_health": "SEHAT"
  }
}
```

---

# 12. Forecasting API

## 12.1 Product Forecast

```http
GET /api/v1/forecasting/products/{product_id}
```

Optional:

```text
?forecast_days=7
```

Response:

```json
{
  "success": true,
  "data": {
    "product_id": 1,
    "product_name": "Es Kopi Susu",
    "forecast_days": 7,
    "forecast": [
      {
        "date": "2026-08-12",
        "predicted_quantity": 18
      },
      {
        "date": "2026-08-13",
        "predicted_quantity": 20
      }
    ]
  }
}
```

## 12.2 Forecast All Products

```http
GET /api/v1/forecasting/products
```

## 12.3 Forecast Refresh

Jika forecasting membutuhkan proses khusus:

```http
POST /api/v1/forecasting/refresh
```

Backend dapat menjalankan proses secara asynchronous/background.

---

# 13. Smart Pricing API

## 13.1 Get Pricing Recommendations

```http
GET /api/v1/pricing/recommendations
```

Optional:

```text
?product_id=1
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": 12,
      "product_id": 1,
      "product_name": "Es Kopi Susu",
      "current_price": 12000,
      "recommended_price": 14000,
      "unit_hpp": 5500,
      "margin_percentage": 60.71,
      "confidence": 0.86,
      "status": "recommended",
      "reason": "Harga saat ini masih memberikan ruang margin yang dapat ditingkatkan."
    }
  ]
}
```

## 13.2 Generate Pricing Recommendation

```http
POST /api/v1/pricing/recommendations
```

Request:

```json
{
  "product_id": 1,
  "target_margin": 60,
  "competitor_price": 14000
}
```

`competitor_price` bersifat optional.

Backend tetap membatasi rekomendasi agar realistis dan memungkinkan profit.

## 13.3 Apply Pricing Recommendation

Keputusan untuk menerapkan harga tetap berada di tangan user.

Jika user memilih menerapkan:

```http
POST /api/v1/pricing/apply
```

Request:

```json
{
  "recommendation_id": 12
}
```

Backend:

```text
Pricing Recommendation
       ↓
User chooses "Terapkan"
       ↓
Update Product Selling Price
       ↓
Record Decision
```

Response:

```json
{
  "success": true,
  "data": {
    "product_id": 1,
    "old_price": 12000,
    "new_price": 14000,
    "decision_id": 55,
    "status": "applied"
  }
}
```

Tidak ada perubahan harga hanya karena recommendation dibuat.

---

# 14. Smart Restock API

## 14.1 Get Restock Recommendations

```http
GET /api/v1/restock/recommendations
```

Optional:

```text
?product_id=1
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": 20,
      "product_id": 1,
      "product_name": "Es Kopi Susu",
      "current_stock": 25,
      "predicted_daily_demand": 18,
      "safety_days": 3,
      "recommended_quantity": 40,
      "stockout_risk": "high",
      "status": "recommended"
    }
  ]
}
```

## 14.2 Generate Restock Recommendation

```http
POST /api/v1/restock/recommendations
```

Request:

```json
{
  "product_id": 1
}
```

Decision engine menggunakan:

```text
Forecast
+
Current Stock
+
Safety Days
```

## 14.3 Apply Restock

Saat user memilih restock:

```http
POST /api/v1/restock/apply
```

Request:

```json
{
  "recommendation_id": 20
}
```

Backend:

```text
Restock Recommendation
       ↓
User chooses "Restock"
       ↓
Create Inventory Movement: received
       ↓
Increase Current Stock
       ↓
Record Decision
```

Response:

```json
{
  "success": true,
  "data": {
    "product_id": 1,
    "quantity_received": 40,
    "new_stock": 65,
    "decision_id": 56,
    "status": "applied"
  }
}
```

---

# 15. Business Health API

## 15.1 Get Business Health

```http
GET /api/v1/health
```

Optional:

```text
?period_start=2026-08-01&period_end=2026-08-31
```

Response:

```json
{
  "success": true,
  "data": {
    "status": "SEHAT",
    "score": 82,
    "metrics": {
      "revenue_trend": "positive",
      "gross_margin": 60.0,
      "net_margin": 32.0,
      "stock_risk": "low"
    }
  }
}
```

Allowed status:

```text
SEHAT
PERLU_PERHATIAN
BERISIKO
```

Health classification is generated by backend rules.

---

# 16. Decisions API

## 16.1 List Applied Decisions

```http
GET /api/v1/decisions
```

Optional:

```text
?page=1&per_page=20&type=pricing
```

Only decisions that have been applied are included in the decision monitoring history.

## 16.2 Decision Detail

```http
GET /api/v1/decisions/{decision_id}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": 55,
    "type": "pricing",
    "product_id": 1,
    "status": "applied",
    "applied_at": "2026-08-11T12:00:00",
    "metrics_before": {
      "selling_price": 12000,
      "margin_percentage": 54.17
    },
    "metrics_after": {
      "selling_price": 14000,
      "margin_percentage": 60.71
    }
  }
}
```

## 16.3 Apply Generic Decision

Untuk decision yang memang dapat diterapkan:

```http
POST /api/v1/decisions/{decision_id}/apply
```

Jika decision sudah memiliki domain-specific apply endpoint seperti pricing/restock, domain-specific endpoint lebih disarankan.

## 16.4 Dismiss Decision

```http
POST /api/v1/decisions/{decision_id}/dismiss
```

Decision yang ditolak tidak diterapkan ke data bisnis.

## 16.5 Metrics Before vs After

`/decisions` membaca Decision yang sudah diterapkan.

`metrics_before` adalah snapshot kondisi sebelum keputusan diterapkan.

`metrics_after` dihitung dari data aktual setelah keputusan diterapkan.

```text
Decision Applied
      ↓
Snapshot Before
      ↓
Business Data Changed
      ↓
Current Actual Data
      ↓
Metrics After
```

Sistem tidak menggunakan hasil prediksi sebagai `metrics_after`.

Contoh pricing:

```text
Before:
selling_price = 12.000
margin = 54.17%

Apply:
selling_price = 14.000

After:
selling_price = 14.000
margin = calculated from actual current HPP
```

---

# 17. Growth API

## 17.1 Growth Map

```http
GET /api/v1/growth
```

Response:

```json
{
  "success": true,
  "data": {
    "current_stage": "Stabil",
    "stages": [
      {
        "id": "pondasi",
        "name": "Pondasi",
        "status": "completed"
      },
      {
        "id": "stabil",
        "name": "Stabil",
        "status": "current"
      },
      {
        "id": "tumbuh",
        "name": "Tumbuh",
        "status": "locked"
      }
    ]
  }
}
```

Growth Map recommendation berasal dari business analysis/rule-based backend.

---

# 18. Business Assistant API

## 18.1 Chat

```http
POST /api/v1/ai/chat
```

Request:

```json
{
  "message": "Kenapa keuntungan saya turun bulan ini?",
  "conversation_id": 10
}
```

Response:

```json
{
  "success": true,
  "data": {
    "conversation_id": 10,
    "message": "Berdasarkan data bisnis Anda, penurunan keuntungan terutama dipengaruhi oleh..."
  }
}
```

## 18.2 AI Context

AI menerima context yang disiapkan backend.

Contoh internal context:

```json
{
  "business": {
    "name": "Kedai Contoh"
  },
  "financial": {
    "revenue": 12500000,
    "gross_profit": 7500000,
    "net_profit": 4000000
  },
  "inventory": {
    "high_risk_products": 2
  },
  "health": {
    "status": "PERLU_PERHATIAN"
  }
}
```

AI tidak melakukan direct database query.

## 18.3 AI Scope

Business Assistant dibatasi sebagai:

> Business Assistant DATARA.

AI boleh menjawab pertanyaan umum selama masih relevan dengan bisnis.

AI tidak boleh mengklaim melakukan tindakan bisnis yang belum dilakukan.

Contoh:

```text
User:
"Sudahkah kamu melakukan restock?"

AI:
"Belum. DATARA hanya memberikan rekomendasi. Restock perlu diterapkan oleh Anda."
```

---

# 19. API-to-Frontend Mapping

| Frontend Feature | API |
|---|---|
| Dashboard | `GET /dashboard` |
| Transactions | `GET/POST /transactions` |
| Products | `GET/POST/PUT/DELETE /products` |
| Product Costs | `GET/PUT /products/{id}/costs` |
| Product Profitability | `GET /products/profitability` |
| Forecasting | `GET /forecasting/products` |
| Smart Pricing | `GET/POST /pricing/recommendations` |
| Apply Pricing | `POST /pricing/apply` |
| Smart Restock | `GET/POST /restock/recommendations` |
| Apply Restock | `POST /restock/apply` |
| Decisions | `GET /decisions` |
| Apply Decision | `POST /decisions/{id}/apply` |
| Growth Map | `GET /growth` |
| Business Assistant | `POST /ai/chat` |
| Login | `POST /auth/login` |

---

# 20. Transaction Integrity

## 20.1 Sale Transaction

Creating a sale must be atomic.

```text
BEGIN
  ↓
Validate Products
  ↓
Validate Stock
  ↓
Create Transaction
  ↓
Create Transaction Items
  ↓
Snapshot HPP
  ↓
Create Sale Inventory Movement
  ↓
Update Current Stock
  ↓
COMMIT
```

Jika salah satu proses gagal:

```text
ROLLBACK
```

## 20.2 Restock Apply

```text
BEGIN
  ↓
Validate Recommendation
  ↓
Create Inventory Movement
  ↓
Increase Current Stock
  ↓
Record Applied Decision
  ↓
COMMIT
```

## 20.3 Pricing Apply

```text
BEGIN
  ↓
Validate Recommendation
  ↓
Update Product Price
  ↓
Record Applied Decision
  ↓
COMMIT
```

---

# 21. Idempotency & Duplicate Protection

Action endpoints harus mencegah penerapan recommendation yang sama berkali-kali.

Contoh:

```text
POST /pricing/apply
```

Jika recommendation sudah `applied`:

```http
409 Conflict
```

Response:

```json
{
  "success": false,
  "message": "Recommendation has already been applied."
}
```

Hal yang sama berlaku untuk restock dan decision.

---

# 22. Validation Rules

## Product

```text
selling_price >= 0
current_stock >= 0
```

## HPP

```text
raw_material >= 0
packaging >= 0
direct_labor >= 0
allocated_overhead >= 0
```

## Transaction

```text
quantity > 0
selling_price >= 0
stock must be sufficient
```

## Expense

```text
amount > 0
```

## Safety Days

```text
safety_days >= 0
```

## Pricing

Recommended price harus:

```text
>= unit_hpp
```

kecuali terdapat business rule khusus yang secara eksplisit mengizinkan strategi loss leader. Untuk MVP DATARA, rekomendasi normal tidak diarahkan pada harga yang menghasilkan kerugian.

---

# 23. Pagination

List endpoint mendukung:

```text
?page=1&per_page=20
```

Default:

```text
page = 1
per_page = 20
```

Maximum:

```text
per_page = 100
```

---

# 24. Filtering & Sorting

Endpoint list dapat mendukung:

```text
?search=
?date_from=
?date_to=
?product_id=
?status=
?type=
?sort_by=
?sort_order=
```

Contoh:

```text
GET /api/v1/transactions?date_from=2026-08-01&date_to=2026-08-31
```

---

# 25. API Security

## 25.1 Protected Routes

Semua business data endpoint protected.

```text
Authorization
        ↓
Authenticated User
        ↓
Business Ownership
```

## 25.2 Input Validation

Semua request divalidasi backend menggunakan Pydantic.

## 25.3 SQL Injection

Database access harus menggunakan parameterized query / ORM.

## 25.4 Secret Management

API key AI dan credential database hanya disimpan pada environment variable/secret manager.

## 25.5 AI Security

User input tidak boleh menyebabkan AI:

- Mengakses database langsung.
- Menjalankan SQL.
- Mengubah business data tanpa domain API.
- Mengklaim tindakan yang belum terjadi.

---

# 26. API Implementation Priority

## Phase 1 — Foundation

```text
Auth
Business
Products
Costs / HPP
```

## Phase 2 — Core Operations

```text
Transactions
Inventory
Expenses
Dashboard
```

## Phase 3 — Intelligence

```text
Forecasting
Smart Pricing
Smart Restock
Business Health
```

## Phase 4 — Decision & Growth

```text
Decisions
Growth Map
```

## Phase 5 — AI

```text
Business Assistant
```

---

# 27. Final API Contract Rules

1. Base path menggunakan `/api/v1`.
2. REST API menggunakan JSON.
3. Field menggunakan `snake_case`.
4. Backend adalah source of truth.
5. Frontend tidak mengakses database langsung.
6. Authentication dan authorization dilakukan backend.
7. Business ownership wajib diverifikasi.
8. Financial amount menggunakan decimal precision.
9. HPP/unit dihitung backend.
10. Fixed cost dicatat sebagai Operating Expense.
11. Transaction dan stock movement sale dilakukan secara atomic.
12. HPP/unit disimpan sebagai snapshot pada transaction item.
13. Smart Pricing menghasilkan recommendation, bukan perubahan otomatis.
14. User memutuskan apakah recommendation pricing diterapkan.
15. Apply Pricing mengubah harga produk dan mencatat decision.
16. Apply Restock membuat inventory movement `received` dan menambah stock.
17. Recommendation yang sudah diterapkan tidak boleh diterapkan ulang.
18. `/decisions` hanya memonitor decision yang sudah diterapkan.
19. `metrics_before` menggunakan snapshot sebelum penerapan.
20. `metrics_after` dihitung dari data aktual.
21. Forecasting menjadi input Smart Restock.
22. Safety Days dapat dikonfigurasi user.
23. Business Health menggunakan tiga status: `SEHAT`, `PERLU_PERHATIAN`, `BERISIKO`.
24. AI tidak menjadi source of truth untuk angka bisnis.
25. AI menerima structured context dari backend.
26. Business Assistant boleh menjawab pertanyaan umum yang masih relevan dengan bisnis.
27. AI tidak boleh mengklaim tindakan yang belum dilakukan.
28. MVP menggunakan modular monolith dan API versioning.
29. Action endpoints harus memiliki duplicate protection.
30. Error response menggunakan struktur JSON yang konsisten.

---

# 28. Document Status

**API CONTRACT / API SPECIFICATION: FINAL**

Dokumen ini menjadi acuan implementasi antara:

```text
DATARA Frontend
        ↕
    REST API
        ↕
DATARA Backend
```

Contract ini harus menjadi referensi utama saat frontend mengganti mock/demo data dengan API backend.
