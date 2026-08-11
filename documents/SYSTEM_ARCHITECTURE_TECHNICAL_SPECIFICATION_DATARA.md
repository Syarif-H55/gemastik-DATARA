# SYSTEM ARCHITECTURE & TECHNICAL SPECIFICATION
## DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM

**Status:** FINAL  
**Scope:** MVP  
**Architecture:** Modular Monolith + REST API  
**Backend:** FastAPI + Python  
**Database:** MySQL  
**Frontend:** Next.js + React + TypeScript

---

# 1. System Overview

DATARA adalah sistem pendukung keputusan untuk membantu pemilik UMKM makanan dan minuman skala mikro memahami kondisi bisnis dan mengambil keputusan berdasarkan data.

Alur utama:

```text
Business Data
      ↓
Data Processing
      ↓
Analysis / Decision Engine
      ↓
Recommendation
      ↓
AI Explanation
      ↓
Business Decision
```

AI bukan pengambil keputusan utama. Perhitungan dan rekomendasi angka berasal dari backend dan decision engine.

## Core Capabilities

- Product & Cost Management
- HPP/unit
- Transaction Management
- Inventory Management
- Financial Analysis
- Sales Forecasting
- Smart Pricing
- Smart Restock
- Business Health
- Growth Map
- Business Assistant

Financial metrics:

```text
Revenue
COGS
Gross Profit
Gross Margin
Operating Expense
Net Profit
```

Business Health:

```text
SEHAT
PERLU_PERHATIAN
BERISIKO
```

---

# 2. Architecture Principles

## 2.1 Backend as Source of Truth

Backend menjadi sumber kebenaran untuk business data, financial calculation, HPP, profit, inventory, forecast result, recommendation, dan Business Health.

Frontend tidak melakukan perhitungan bisnis authoritative.

## 2.2 Separation of Concerns

```text
Presentation
     ↓
API / Application
     ↓
Domain / Business Logic
     ↓
Data Access
     ↓
Database
```

AI menjadi integration layer yang menggunakan structured business context.

## 2.3 Rule-Based Decision, AI-Assisted Explanation

```text
Data
 ↓
Rule / Algorithm / Model
 ↓
Decision
 ↓
LLM
 ↓
Explanation
```

LLM tidak menentukan keputusan bisnis secara bebas.

## 2.4 User Input as Primary Business Signal

Untuk fitur seperti Smart Pricing:

```text
User Input
    ↓
Primary Signal
    +
Supporting Data
    ↓
Decision Engine
```

## 2.5 Simple but Useful

MVP menghindari:

- Accounting ledger kompleks.
- Multi-business management.
- Enterprise multi-role.
- AI orchestration berlebihan.
- Microservices tanpa kebutuhan nyata.

## 2.6 Historical Data Preservation

Historical data dipertahankan untuk analisis tren, forecasting, profitability, Business Health, dan Growth Map.

`unit_hpp` disimpan sebagai snapshot pada transaction item agar historical profitability tidak berubah ketika HPP master diperbarui.

## 2.7 Secure by Backend

```text
Request
   ↓
Authentication
   ↓
Authorization
   ↓
Validation
   ↓
Business Logic
   ↓
Database
```

## 2.8 API-First Communication

```text
Frontend
   ↕
REST API
   ↕
Backend
   ↕
Database / Decision Engine / AI
```

## 2.9 Modular Backend

```text
Auth
Business
Product
Cost
Sales
Inventory
Finance
Forecast
Pricing
Restock
Health
Growth
AI
```

## 2.10 Monolith First

MVP menggunakan modular monolith.

---

# 3. Technology Stack & Technical Constraints

| Layer | Technology |
|---|---|
| Frontend | Next.js + React + TypeScript |
| Styling | Tailwind CSS + shadcn/ui |
| Backend | FastAPI + Python |
| API | REST API |
| Database | MySQL |
| Validation | Pydantic |
| AI/LLM | Backend-mediated integration |
| Forecasting | Python-based processing |
| Version Control | Git |

Frontend menggunakan Next.js 16.3.0, React 19.2.8, TypeScript, Tailwind CSS v4, shadcn/ui, Recharts, Phosphor Icons, next-themes, dan Sonner.

## API Versioning

```text
/api/v1/
```

## Naming Convention

JSON dan database menggunakan `snake_case`.

```json
{
  "product_id": 12,
  "current_stock": 25,
  "recommended_quantity": 40
}
```

## Financial Precision

Nilai uang menggunakan:

```text
DECIMAL(15,2)
```

## Time & Date

```text
transaction_date → DATETIME
expense_date     → DATE
period_start     → DATE
period_end       → DATE
forecast_date    → DATE
```

Timezone mengikuti konfigurasi sistem, dengan `Asia/Jakarta` sebagai default deployment Indonesia.

## Validation

Frontend validation untuk UX, backend validation untuk security dan data integrity.

## HTTP Status

| Status | Use |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 400 | Invalid request |
| 401 | Unauthenticated |
| 403 | Unauthorized |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation error |
| 500 | Internal server error |

## Authentication

Authentication dikontrol backend.

## Authorization

Authorization menggunakan business ownership.

## AI Constraint

AI/LLM tidak mengakses database secara langsung.

```text
User
 ↓
Backend
 ↓
Context Builder
 ↓
Structured Business Context
 ↓
LLM
 ↓
Response
```

## Forecasting

Forecasting dipisahkan dari request-response normal jika prosesnya berat.

```text
Historical Sales
       ↓
Forecasting Process
       ↓
forecast_results
       ↓
Smart Restock
```

## Background Processing

Dapat digunakan untuk:

- Forecasting.
- Batch analytical calculation.
- Periodic Business Health assessment.
- Periodic recommendation generation.

## Environment

Minimal:

```text
Development
Production
```

Secret production tidak boleh digunakan pada development.

---

# 4. System Architecture

## 4.1 High-Level Architecture

```text
┌──────────────────────────────────────────────┐
│                 DATARA USER                  │
│              UMKM Business Owner             │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                  FRONTEND                    │
│              Web Application                 │
│                                              │
│ Dashboard │ Products │ Sales │ Inventory     │
│ Finance   │ Pricing  │ Restock │ Growth Map  │
│ Business Assistant                           │
└──────────────────────┬───────────────────────┘
                       │
                    REST API
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              DATARA BACKEND                  │
│              Modular Monolith                │
│                                              │
│ Auth │ Business │ Product │ Sales            │
│ Inventory │ Finance │ Forecast │ Pricing     │
│ Restock │ Health │ Growth │ AI Assistant     │
└──────────────┬────────────────┬───────────────┘
               │                │
               ▼                ▼
        ┌─────────────┐  ┌─────────────┐
        │    MySQL    │  │  AI / LLM   │
        │  Database   │  │ Integration │
        └─────────────┘  └─────────────┘
```

## 4.2 Architecture Layers

### Presentation
Menampilkan data, form input, dashboard, visualisasi, recommendation, dan Business Assistant.

### API / Application
Menangani HTTP request, authentication, authorization, validation, response formatting, dan orchestration.

### Domain / Business Logic
Menangani HPP, financial calculation, pricing, restock, Business Health, dan Growth Recommendation.

### Data Access
Menangani komunikasi dengan database.

### Intelligence
Menangani forecasting, decision engine, AI context building, dan LLM integration.

## 4.3 Module Architecture

```text
backend/
├── auth/
├── business/
├── products/
├── sales/
├── inventory/
├── finance/
├── forecasting/
├── pricing/
├── restock/
├── health/
├── growth/
└── ai/
```

## 4.4 Core Data Flow

```text
User Input
    ↓
Frontend
    ↓
REST API
    ↓
Validation
    ↓
Business Service
    ↓
Database
    ↓
Analytical / Decision Engine
    ↓
Recommendation
    ↓
API Response
    ↓
Frontend
```

## 4.5 Smart Pricing

```text
Product
  ↓
HPP
  ↓
Current Price
  ↓
User Input / Supporting Factors
  ↓
Pricing Decision Engine
  ↓
Recommended Price
  ↓
Pricing Recommendation
  ↓
Frontend
```

## 4.6 Smart Restock

```text
Historical Sales
       ↓
Forecasting
       ↓
Forecast Result
       +
Current Stock
       +
Safety Days
       ↓
Restock Decision Engine
       ↓
Recommended Quantity
       ↓
Restock Recommendation
```

Actual restock tetap dilakukan user dan dicatat sebagai inventory movement.

## 4.7 Financial Analysis

```text
Sales Transactions
        +
Product HPP
        +
Operating Expenses
        ↓
Financial Calculation
        ↓
Revenue
COGS
Gross Profit
Gross Margin
Net Profit
        ↓
Business Health
        ↓
Growth Recommendation
```

## 4.8 AI Architecture

```text
             USER
               │
               ▼
        Business Assistant
               │
               ▼
            Backend
               │
               ▼
        Context Builder
               │
       ┌───────┴────────┐
       ▼                ▼
Business Data     Conversation
       │             History
       └───────┬────────┘
               ▼
             LLM
               │
               ▼
        Natural Language
           Response
```

## 4.9 Request Flow

```text
HTTP Request
     ↓
Authentication
     ↓
Authorization
     ↓
Request Validation
     ↓
Controller
     ↓
Application Service
     ↓
Domain Logic
     ↓
Repository / Data Access
     ↓
Database
     ↓
Response
```

## 4.10 Architectural Boundaries

- Frontend ↔ Backend: REST API.
- Backend ↔ Database: database hanya diakses backend.
- Backend ↔ AI: AI menerima structured context.
- Decision Engine ↔ AI: decision engine menghasilkan angka/keputusan, AI menjelaskan.

Contoh:

```text
Decision Engine
     ↓
"Recommended Price = Rp14.000"
     ↓
AI
     ↓
"DATARA menyarankan harga Rp14.000 karena..."
```

## 4.11 Quality Goals

- Correctness.
- Security.
- Maintainability.
- Simplicity.
- Scalability.
- Traceability.
- Explainability.

---

# 5. Frontend Architecture

## 5.1 Frontend Stack

- Next.js 16.3.0.
- React 19.2.8.
- TypeScript.
- Tailwind CSS v4.
- shadcn/ui.
- Recharts.
- Phosphor Icons.
- next-themes.
- Sonner.

## 5.2 Frontend Structure

```text
frontend/
└── src/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   ├── login/
    │   └── (app)/
    │       ├── layout.tsx
    │       ├── dashboard/
    │       ├── transactions/
    │       ├── forecasting/
    │       ├── products/
    │       ├── pricing/
    │       ├── restock/
    │       ├── decisions/
    │       └── growth/
    │
    ├── components/
    ├── hooks/
    └── lib/
        ├── types.ts
        ├── api.ts
        ├── format.ts
        ├── utils.ts
        └── demo-data.ts
```

## 5.3 Routes

| Route | Function |
|---|---|
| `/` | Landing |
| `/login` | Login |
| `/dashboard` | Business Dashboard |
| `/transactions` | Catat Transaksi |
| `/forecasting` | Sales Forecasting |
| `/products` | Product Profitability |
| `/pricing` | Smart Pricing |
| `/restock` | Smart Restock |
| `/decisions` | Keputusan & Monitoring |
| `/growth` | Roadmap Pertumbuhan |

## 5.4 Frontend Responsibilities

- Presentation.
- User interaction.
- Form input.
- Client-side UX validation.
- Visualisasi data.
- Loading/error/empty states.
- Pemanggilan REST API.
- Menampilkan hasil analytical engine.

Frontend bukan source of truth business calculation.

## 5.5 API Integration

API client:

```text
src/lib/api.ts
```

Base URL:

```text
NEXT_PUBLIC_API_URL
```

Default development:

```text
http://localhost:8000/api
```

Supported methods:

```text
GET
POST
PUT
PATCH
DELETE
```

Target:

```text
Frontend Page
      ↓
src/lib/api.ts
      ↓
REST API
      ↓
FastAPI Backend
```

## 5.6 Domain Type Contract

`src/lib/types.ts` menjadi referensi kontrak data frontend-backend.

Entity:

- User.
- Product.
- ProductProfitability.
- InventoryLog.
- Transaction.
- TransactionItem.
- Cost.
- PricingRecommendation.
- RestockRecommendation.
- ProductForecast.
- DashboardMetrics.
- BusinessHealth.
- Decision.
- DecisionRecord.
- GrowthStage.

Field API menggunakan `snake_case`.

## 5.7 Analytical Migration

Current demo:

```text
demo-data.ts
      ↓
Client-side calculation
      ↓
UI
```

Target:

```text
Database
    ↓
FastAPI
    ↓
Business / Decision Engine
    ↓
REST API
    ↓
Frontend
```

## 5.8 Responsive Architecture

Frontend menggunakan:

- AppShell.
- Collapsible sidebar.
- Mobile detection.
- Responsive layout.
- Light/dark theme.
- shadcn/ui components.

## 5.9 Integration Constraints

1. Response API kompatibel dengan frontend types.
2. Field menggunakan `snake_case`.
3. Business calculation dilakukan backend.
4. Mock data digantikan API setelah endpoint tersedia.
5. Authentication demo digantikan authentication nyata.
6. `NEXT_PUBLIC_API_URL` menjadi konfigurasi base API.

---

# 6. Backend Architecture

## 6.1 Backend Stack

| Component | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python |
| API | REST API |
| Database | MySQL |
| Architecture | Modular Monolith |
| Validation | Pydantic |
| Data Access | Repository / ORM implementation |
| Authentication | Backend-controlled |
| AI Integration | Backend-mediated |
| Forecasting | Python-based processing |

## 6.2 Backend Layers

```text
FastAPI Backend
│
├── API Layer
│   ├── Routes
│   ├── Request Schema
│   └── Response Schema
│
├── Application Layer
│   ├── Services
│   └── Use Cases
│
├── Domain Layer
│   ├── Business Rules
│   ├── Financial Logic
│   ├── Pricing Logic
│   ├── Restock Logic
│   └── Health Logic
│
├── Intelligence Layer
│   ├── Forecasting
│   ├── Decision Engine
│   └── AI Context Builder
│
└── Data Layer
    ├── Models
    ├── Repository / Data Access
    └── MySQL
```

## 6.3 Suggested Backend Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── business.py
│   │       ├── products.py
│   │       ├── sales.py
│   │       ├── inventory.py
│   │       ├── finance.py
│   │       ├── forecasting.py
│   │       ├── pricing.py
│   │       ├── restock.py
│   │       ├── health.py
│   │       ├── growth.py
│   │       └── ai.py
│   │
│   ├── schemas/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── domain/
│   ├── forecasting/
│   ├── decision_engine/
│   ├── ai/
│   ├── core/
│   └── db/
│
├── tests/
├── requirements.txt
└── .env
```

## 6.4 API Layer

Menangani:

- Routing.
- HTTP method.
- Authentication dependency.
- Request validation.
- Response schema.
- HTTP status code.

Router tidak berisi business logic kompleks.

## 6.5 Service Layer

Contoh:

```text
PricingService
RestockService
FinanceService
ForecastService
HealthService
GrowthService
AIService
```

Flow:

```text
Pricing Router
      ↓
Pricing Service
      ↓
HPP Service
      ↓
Pricing Decision Engine
      ↓
Pricing Recommendation
```

## 6.6 Domain / Decision Layer

```text
decision_engine/
├── pricing/
├── restock/
├── health/
└── growth/
```

Business rules ditempatkan di domain layer agar mudah diuji, diubah, dan digunakan oleh API maupun background job.

## 6.7 Repository / Data Access

Contoh:

```text
ProductRepository
SalesRepository
InventoryRepository
ExpenseRepository
ForecastRepository
RecommendationRepository
```

Flow:

```text
Service
   ↓
Repository
   ↓
Database
```

## 6.8 Pydantic Schemas

Pydantic digunakan untuk request/response validation:

- Required field.
- Data type.
- Numeric range.
- Business-specific validation.

## 6.9 Financial Service

```text
FinancialService
    │
    ├── calculate_revenue()
    ├── calculate_cogs()
    ├── calculate_gross_profit()
    ├── calculate_gross_margin()
    └── calculate_net_profit()
```

Sumber:

```text
Sales Transactions
+
HPP
+
Operating Expenses
```

## 6.10 HPP Service

```text
Product Costs
      ↓
HPP Service
      ↓
HPP / Unit
```

Formula:

```text
HPP/unit
=
Raw Material
+ Packaging
+ Direct Labor
+ Allocated Production Overhead
```

Fixed cost seperti sewa dan gaji tetap tidak masuk HPP.

## 6.11 Forecasting Module

```text
Historical Sales
       ↓
Data Preparation
       ↓
Forecast Model
       ↓
Forecast Result
       ↓
forecast_results
```

Forecast result digunakan oleh:

```text
forecast_results
       ↓
Restock Decision Engine
```

Model forecasting tidak langsung mengubah inventory.

## 6.12 Decision Engine

```text
Data
 ↓
Rules / Model
 ↓
Decision
 ↓
Recommendation
```

Decision engine tidak berinteraksi langsung dengan frontend.

## 6.13 AI Service

Menangani:

- Context preparation.
- Prompt construction.
- LLM request.
- Response processing.
- Conversation management.

Flow:

```text
AI Router
   ↓
AI Service
   ↓
Context Builder
   ↓
LLM Provider
   ↓
Response
```

AI tidak menghitung financial metrics secara independen.

## 6.14 Dependency Direction

```text
API
 ↓
Service
 ↓
Domain
 ↓
Repository
 ↓
Database
```

AI:

```text
API
 ↓
AI Service
 ↓
Context Builder
 ↓
Business Services / Read Models
 ↓
LLM
```

Domain logic tidak bergantung pada HTTP framework.

## 6.15 Backend Security Boundary

```text
Authentication
      ↓
Authorization
      ↓
Business Ownership Check
      ↓
Validation
      ↓
Service
```

## 6.16 Backend Error Boundary

Internal exception tidak langsung diekspos ke user.

```text
Database Exception
        ↓
Internal Logging
        ↓
Generic API Error
```

## 6.17 Backend Responsibility

```text
┌───────────────────────────────────┐
│             FastAPI               │
├───────────────────────────────────┤
│ Authentication / Authorization    │
│ Validation                        │
│ CRUD                              │
│ HPP Calculation                   │
│ Financial Analysis                │
│ Forecast Integration              │
│ Smart Pricing                     │
│ Smart Restock                     │
│ Business Health                   │
│ Growth Map                        │
│ AI Context                        │
│ API Response                      │
└───────────────────────────────────┘
```

---

# 7. Final Architecture Summary

```text
                         USER
                           │
                           ▼
                ┌───────────────────┐
                │     FRONTEND      │
                │ Next.js + React   │
                │    TypeScript     │
                └─────────┬─────────┘
                          │
                       REST API
                          │
                          ▼
                ┌───────────────────┐
                │   FASTAPI BACKEND │
                │ Modular Monolith  │
                └─────────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   Business Logic    Decision Engine    AI Service
        │                 │                 │
        │                 ▼                 ▼
        │            Forecasting          Context
        │                 │                 │
        └──────────┬──────┘                 ▼
                   │                       LLM
                   ▼
                ┌───────┐
                │ MySQL │
                └───────┘
```

## Architectural Rules

1. Backend adalah source of truth.
2. Frontend tidak menghitung business metric authoritative.
3. Database hanya diakses backend.
4. Semua business API menggunakan REST API.
5. API menggunakan `/api/v1`.
6. Business logic berada di service/domain layer.
7. Decision engine menghasilkan recommendation.
8. Forecasting menghasilkan forecast result.
9. AI menjelaskan dan memberikan saran berdasarkan structured context.
10. LLM tidak memiliki direct database access.
11. Historical data harus dipertahankan.
12. Authentication dan authorization dilakukan backend.
13. Business ownership wajib diverifikasi pada protected resource.
14. Financial amount menggunakan decimal precision.
15. MVP menggunakan modular monolith, bukan microservices.

---

# 8. Document Status

**SYSTEM ARCHITECTURE & TECHNICAL SPECIFICATION: FINAL**

Dokumen ini menjadi acuan untuk:

- Implementasi FastAPI backend.
- Integrasi frontend.
- Database integration.
- API Contract.
- Decision Engine.
- Forecasting.
- Smart Pricing.
- Smart Restock.
- Business Health.
- Growth Map.
- AI Business Assistant.
- Deployment dan development workflow.
