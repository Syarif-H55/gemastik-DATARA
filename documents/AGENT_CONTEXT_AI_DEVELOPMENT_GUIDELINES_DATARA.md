# AGENT CONTEXT / AI DEVELOPMENT GUIDELINES
## DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM

**Status:** FINAL  
**Purpose:** Single development context for AI coding agents, developers, and contributors  
**Primary Product Actor:** Pemilik UMKM  
**Architecture:** Decoupled Web Application  
**Frontend:** Next.js 16 + React + TypeScript  
**Backend:** FastAPI + Python + MySQL  
**API:** REST

---

# 1. PROJECT IDENTITY

Project:

**DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM**

Core concept:

> Decision Support System yang mengolah data penjualan, HPP, biaya, stok, dan profitabilitas menjadi indikator bisnis serta rekomendasi keputusan yang explainable.

Core flow:

```text
Transaction
    ↓
Business Data
    ↓
Analytics
    ↓
Decision Engine / Forecasting
    ↓
Recommendation
    ↓
Explanation
    ↓
User Decision
    ↓
Monitoring
```

The system is not an autonomous business agent.

---

# 2. PRIMARY DEVELOPMENT RULE

## Backend is the source of truth.

Business calculations must not be independently reimplemented in the frontend.

Authoritative calculations include:

- HPP.
- Revenue.
- COGS.
- Gross Profit.
- Margin.
- Net Profit.
- Product profitability.
- Pricing recommendation.
- Restock recommendation.
- Forecast result.
- Business Health.
- Growth stage.
- Decision monitoring.

Frontend is responsible for:

- Presentation.
- Interaction.
- Local UI state.
- Formatting.
- API communication.

---

# 3. CURRENT PROJECT STATE

The frontend demo already exists.

Current frontend:

```text
frontend/
└── Next.js 16 App Router
```

The frontend currently uses:

```text
src/lib/demo-data.ts
```

as mock data and contains client-side demo calculations.

Backend:

```text
FastAPI + MySQL
```

is the intended production backend.

The current mock/demo implementation is not the final source of truth. It must eventually be replaced by API-backed data.

---

# 4. ARCHITECTURE

Production architecture:

```text
┌──────────────────────┐
│ Next.js Frontend     │
│ React / TypeScript   │
└──────────┬───────────┘
           │ REST API
           ▼
┌──────────────────────┐
│ FastAPI Backend      │
│ Domain / Services    │
│ Decision Engine      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ MySQL Database       │
└──────────────────────┘
```

AI:

```text
Backend Business Context
          ↓
     AI Service
          ↓
     LLM Provider
```

LLM must not have direct database access.

---

# 5. ACTOR MODEL

Primary actor:

```text
Pemilik UMKM
```

The product should not depend on separate Owner/Staff workflows.

Legacy frontend types may still contain:

```text
owner | staff
```

but this must not drive product behavior.

Do not introduce a new Staff UI unless explicitly approved.

---

# 6. TECH STACK

## Frontend

- Next.js 16.3.0.
- React 19.
- TypeScript strict mode.
- Tailwind CSS v4.
- shadcn/ui.
- Recharts.
- Phosphor Icons.
- next-themes.
- Sonner.

## Backend

- FastAPI.
- Python.
- MySQL.
- REST API.

## Frontend scripts

```bash
npm run dev
npm run build
npm run start
npm run lint
```

There is currently no dedicated test suite in the frontend.

---

# 7. FRONTEND DIRECTORY STRUCTURE

```text
frontend/
├── AGENTS.md
├── CLAUDE.md
├── package.json
├── components.json
├── tsconfig.json
├── next.config.ts
└── src/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   ├── globals.css
    │   ├── login/
    │   │   └── page.tsx
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
    ├── components/
    │   ├── layout/
    │   ├── ui/
    │   ├── page-header.tsx
    │   ├── kira-icons.tsx
    │   ├── theme-provider.tsx
    │   └── theme-toggle.tsx
    ├── hooks/
    │   └── use-mobile.ts
    └── lib/
        ├── types.ts
        ├── api.ts
        ├── format.ts
        ├── utils.ts
        └── demo-data.ts
```

---

# 8. NEXT.JS 16 RULES

The project uses Next.js 16.

Important:

```text
params
searchParams
```

are Promise-based in the relevant App Router APIs.

Use:

```typescript
const resolvedParams = await params;
```

rather than treating them as synchronous objects.

Use the available Next.js type helpers where appropriate.

Do not copy patterns intended for older Next.js versions without checking compatibility.

---

# 9. SERVER VS CLIENT COMPONENTS

## Server Components

Default to Server Components.

Server Components must not directly import browser-only functionality.

For Phosphor icons:

```text
Server Component
      ↓
src/components/kira-icons.tsx
```

Do not directly import:

```text
@phosphor-icons/react
```

from a Server Component.

## Client Components

Files using:

```text
"use client"
```

may import Phosphor icons directly.

Use Client Components only when necessary:

- Browser interaction.
- React state.
- Event handlers.
- Client-only hooks.
- Interactive charts.
- Theme interaction.

---

# 10. ICON CONVENTION

Existing wrapper:

```text
src/components/kira-icons.tsx
```

is the icon wrapper for Server Components.

Important:

Phosphor export names must be verified before use.

Examples documented in the current frontend:

```text
TrendUp
SignOut
ArrowsDownUp
WarningCircle
```

Do not invent icon names.

If an icon import fails, check the actual package export.

---

# 11. UI COMPONENT CONVENTION

Use existing shared components before creating new equivalents.

Important shared components:

```text
PageHeader
EmptyState
ModuleBadge
AppShell
AppSidebar
ThemeProvider
ThemeToggle
```

shadcn/ui components are available under:

```text
src/components/ui/
```

Do not create a duplicate `Button`, `Card`, `Badge`, `Dialog`, etc. if the existing component already satisfies the requirement.

---

# 12. STYLING RULES

Use:

```text
Tailwind CSS v4
```

Do not introduce a second styling system without explicit approval.

Prefer:

```text
className
```

with existing Tailwind conventions.

Use existing CSS variables/theme tokens where appropriate.

Maintain light/dark theme compatibility.

---

# 13. DATA FORMATTING

Use:

```text
src/lib/format.ts
```

for business formatting.

Locale:

```text
id-ID
```

Required conventions:

```text
Currency:
Rp12.500

Percentage:
30.0%

Number:
12.500

Date:
dd MMM yyyy

DateTime:
dd MMM yyyy, HH:mm
```

Do not duplicate currency/date formatting logic throughout pages.

---

# 14. API CLIENT

Frontend API communication goes through:

```text
src/lib/api.ts
```

Base URL:

```text
NEXT_PUBLIC_API_URL
```

Do not create ad-hoc `fetch()` calls throughout page components when the API client can own the request.

Target flow:

```text
Page
 ↓
API client
 ↓
REST API
```

Not:

```text
Page
 ↓
Database
```

---

# 15. API DATA CONVENTION

API JSON fields use:

```text
snake_case
```

Examples:

```text
selling_price
low_stock_threshold
predicted_units
target_margin_percent
actual_margin_percent
suggested_quantity
days_of_supply
```

Do not silently rename API fields to camelCase unless an explicit frontend adapter is being used.

Keep frontend domain types aligned with API contracts.

---

# 16. DOMAIN TYPES

Important entities:

```text
User
Product
ProductProfitability
InventoryLog
Transaction
TransactionItem
Cost
Decision
PricingRecommendation
RestockRecommendation
BusinessHealth
DashboardMetrics
ForecastPoint
ProductForecast
DecisionRecord
GrowthStage
```

The current frontend domain contract should be treated as the baseline when implementing backend integration.

---

# 17. BUSINESS LOGIC LOCATION

Do not place authoritative business logic in:

```text
React component
```

or:

```text
demo-data.ts
```

Production target:

```text
FastAPI
 ↓
Domain / Service Layer
 ↓
Database
```

Examples:

### HPP

```text
Backend calculates HPP.
Frontend displays HPP.
```

### Pricing

```text
Backend generates recommendation.
Frontend displays recommendation.
```

### Forecasting

```text
Backend generates forecast.
Frontend renders chart.
```

### Business Health

```text
Backend determines status.
Frontend displays status.
```

---

# 18. HPP RULES

HPP focuses on costs directly related to producing a product.

Primary components:

```text
Raw Material
+
Packaging
+
Direct Labor
+
Allocated Production Overhead
```

Fixed operating expenses such as:

```text
Rent
Fixed Salary
Administration
```

remain separate as Operating Expense.

Variable cost directly attributable to the product enters HPP.

Difficult-to-allocate production costs such as electricity/gas may be treated as allocated production overhead or operational overhead according to the finalized business rule.

HPP is calculated per unit.

---

# 19. FINANCIAL STRUCTURE

Conceptual:

```text
HPP / Unit
   ↓
Smart Pricing
   ↓
Margin
   ↓
Profit
   ↓
Decision Support
   ↓
Growth Map
```

Operating Expense remains separate from product HPP.

Do not casually merge fixed operating expenses into HPP.

---

# 20. SMART PRICING RULES

Smart Pricing is rule-based.

Primary inputs:

```text
User Input
+
HPP
+
Current Price
```

Supporting inputs may include:

```text
Target Margin
Competitor Price
Historical Performance
```

User input has greater weight than optional external signals.

Recommendation must remain:

- Realistic.
- Profitable under normal conditions.
- Consistent with HPP.
- Consistent with target margin.
- Not excessively extreme versus current price.

Pricing recommendation does not automatically change the product price.

Flow:

```text
Recommendation
 ↓
User Review
 ↓
Apply / Ignore
```

---

# 21. SMART RESTOCK RULES

Smart Restock uses:

```text
Forecast Demand
+
Current Stock
+
Safety Days
```

Safety Days:

- User configurable.
- Has a default value.
- Must remain realistic.

Conceptual:

```text
Forecast Daily Demand
      ↓
Planning Horizon
      +
Safety Stock
      ↓
Required Stock
      -
Current Stock
      ↓
Suggested Quantity
```

Do not allow an LLM to independently determine stock quantity.

---

# 22. FORECASTING RULES

Forecasting uses a combination of:

```text
Simple Average
+
Moving Average
+
Exponential Smoothing
```

Method selection depends on data sufficiency.

Conceptual:

```text
Very Limited Data
→ Simple Average

Limited Data
→ Moving Average

Sufficient Data
→ Exponential Smoothing
```

If data is limited, the system still provides a simple estimate with low confidence.

Do not fabricate historical data.

Forecast is an estimate, not a guarantee.

---

# 23. FORECAST CONFIDENCE

Confidence levels:

```text
HIGH
MEDIUM
LOW
```

Confidence reflects:

- Data volume.
- Data consistency.
- Historical stability.
- Method reliability.

Low confidence must be communicated clearly.

Example:

```text
Estimasi masih bersifat awal karena
data penjualan produk belum banyak.
```

---

# 24. BUSINESS HEALTH

Business Health is rule-based.

Allowed statuses:

```text
SEHAT
PERLU_PERHATIAN
BERISIKO
```

The backend is authoritative.

Frontend must not independently reinterpret the health classification.

LLM may explain why the status exists.

---

# 25. PRODUCT PROFITABILITY

Backend calculates:

```text
Unit Profit
Margin
Qty Sold
Total Revenue
Total Cost
Total Profit
```

Conceptual:

```text
unit_profit =
selling_price - hpp

margin_percent =
unit_profit / selling_price × 100

total_profit =
total_revenue - total_cost
```

Use backend result for authoritative UI.

---

# 26. PRODUCT CLASSIFICATION

The frontend demo uses simple classification based on:

- Margin.
- Quantity sold.

Current conceptual classes:

```text
profitable
potential
evaluate
```

Display labels may be:

```text
Menguntungkan
Berpotensi
Perlu Evaluasi
```

The backend should own the production classification rules.

Do not silently change thresholds without updating the relevant business rule documentation.

---

# 27. DECISION MODEL

A recommendation is not automatically a decision.

Distinction:

```text
Recommendation
→ Suggested action

Decision
→ Recommendation chosen/applied by user

Decision Record
→ Applied decision + subsequent monitoring
```

User remains the decision authority.

---

# 28. DECISION MONITORING

`/decisions` reads decisions that were actually applied.

Backend calculates:

```text
metrics_before
vs
metrics_after
```

using actual business data.

Primary monitoring metrics:

```text
Revenue
Margin
Stock
```

Possible outcome:

```text
Improved
Flat
Regressed
```

Do not generate fake post-decision outcomes.

If insufficient data exists:

```text
Monitoring unavailable / limited
```

must be represented honestly.

---

# 29. GROWTH MAP

Growth Map is rule-based.

The backend determines:

```text
Current Stage
+
Next Stage
+
Required Indicator
+
Next Step
```

Frontend presents the result.

LLM may explain the stage.

LLM must not override the Growth Map classification.

---

# 30. AI ROLE

AI is:

```text
Business Assistant
+
Explanation Layer
```

AI is not:

```text
Source of Truth
```

Core flow:

```text
Business Data
 ↓
Rule / ML Engine
 ↓
Business Result
 ↓
AI Context
 ↓
LLM
 ↓
Explanation / Advice
```

---

# 31. AI SCOPE

Business Assistant may answer:

- Questions about the user's business data.
- Explanations of recommendations.
- Explanations of Business Health.
- Explanations of profitability.
- General business questions relevant to the user's context.

AI should remain within the business domain.

For unrelated questions:

```text
Maaf, saya fokus membantu Anda memahami
dan mengelola bisnis melalui DATARA.
```

---

# 32. AI MUST NOT

LLM must not:

- Invent business numbers.
- Replace backend calculations.
- Change database directly.
- Apply prices directly.
- Execute restocking directly.
- Claim an action happened when it did not.
- Override business rules.
- Access another user's business data.
- Treat generated text as authoritative financial data.

---

# 33. AI CONTEXT

LLM receives structured context.

Example:

```text
User Question
+
Business Summary
+
Relevant Metrics
+
Decision Result
+
Relevant History
```

Do not send the entire database to the LLM.

Context should be selected based on the question.

Example:

```text
Question:
"Kenapa keuntungan saya turun?"

Context:
Financial Summary
+
Previous Period
+
COGS
+
Operating Expense
```

No need to send unrelated inventory logs.

---

# 34. AI GROUNDING

AI response must be grounded in backend output.

Separate:

```text
FACT
RECOMMENDATION
GENERAL ADVICE
```

If data is unavailable:

```text
Data tersebut belum tersedia di DATARA.
```

Do not guess.

---

# 35. AI ACTION BOUNDARY

Correct:

```text
LLM
 ↓
Explanation
 ↓
User
 ↓
Frontend Action
 ↓
Backend API
 ↓
Database
```

Incorrect:

```text
LLM
 ↓
Database
```

If function calling is introduced later, every action must still pass through authorized backend domain APIs.

---

# 36. PROVIDER-AGNOSTIC LLM

Do not hard-code the product architecture to a single LLM provider.

Use:

```text
AI Service
 ↓
LLM Adapter
 ↓
Provider
 ↓
Model
```

Configuration:

```text
LLM_PROVIDER
LLM_MODEL
LLM_API_KEY
```

Provider can be changed without redesigning Business Assistant.

---

# 37. SECURITY

## Authentication

Production requires real authentication.

The current login page is only a demo and is not an authentication implementation.

## Authorization

Every business-related request must verify:

```text
Authenticated User
+
Business Ownership
```

Never trust:

```text
business_id
```

from the client without authorization validation.

## AI Data Isolation

LLM context must only contain data belonging to the authenticated business.

---

# 38. VALIDATION

Validate at both:

```text
Frontend
+
Backend
```

Backend validation is authoritative.

Examples:

```text
quantity > 0
price >= 0
margin within allowed range
valid product
valid transaction
```

Do not rely only on frontend validation.

---

# 39. TRANSACTION + INVENTORY ATOMICITY

A successful sale must maintain consistency.

Conceptual:

```text
Create Transaction
+
Create Transaction Items
+
Decrease Inventory
+
Create Inventory Log
```

These operations should be atomic.

If one required operation fails:

```text
Rollback
```

Do not create a transaction while leaving inventory inconsistent.

---

# 40. REST API INTEGRATION

Production frontend should consume:

```text
/api/...
```

through the centralized API client.

Do not duplicate endpoint URLs across pages.

Expected domains:

```text
auth
business
products
transactions
inventory
costs
dashboard
forecasting
pricing
restock
decisions
growth
assistant
```

---

# 41. UI STATE REQUIREMENTS

Every API-driven page should handle:

```text
idle
loading
success
empty
error
```

Mutation:

```text
idle
submitting
success
error
```

Do not leave blank screens during loading or API failure.

---

# 42. ERROR HANDLING

Errors shown to users must be understandable.

Prefer:

```text
Data belum dapat dimuat.
Coba lagi.
```

over exposing:

```text
SQLAlchemy IntegrityError...
```

Technical details may be logged internally.

---

# 43. DEMO DATA MIGRATION

Current:

```text
demo-data.ts
 ↓
Client-side calculations
 ↓
UI
```

Target:

```text
FastAPI
 ↓
Database / Services
 ↓
API
 ↓
api.ts
 ↓
UI
```

When replacing demo data:

1. Preserve the existing UI contract where possible.
2. Align API response fields with `types.ts`.
3. Move authoritative calculations to backend.
4. Remove duplicated client calculations.
5. Keep mock data only where useful for isolated UI development.

---

# 44. REBRANDING

The frontend still contains legacy KIRA references.

Production product name:

```text
DATARA
```

Full name:

```text
DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM
```

Legacy KIRA references must be removed from:

```text
Metadata
Landing Page
Login
AppBrand
Developer documentation
```

Do not introduce new KIRA branding.

The existing icon wrapper may retain its filename temporarily for compatibility, but new naming should prefer DATARA when refactoring is practical.

---

# 45. ROUTES

Primary application routes:

```text
/dashboard
/transactions
/forecasting
/products
/pricing
/restock
/decisions
/growth
```

Authentication:

```text
/login
```

Landing:

```text
/
```

Do not create additional primary modules without checking scope.

---

# 46. FEATURE SCOPE

Core MVP:

1. Business Dashboard.
2. HPP / Product Profitability.
3. Transaction Recording.
4. Sales Forecasting.
5. Smart Pricing.
6. Smart Restock.
7. Explainable Recommendations.
8. Decision Recording.
9. Decision Monitoring.
10. Business Growth Roadmap.
11. Business Assistant.

Out of scope unless explicitly re-approved:

- What-If Simulator.
- Smart Alert.
- Action Center.
- External marketplace integration.
- Payment gateway integration.
- Third-party POS integration.
- Autonomous price changes.
- Autonomous purchasing.

---

# 47. NO FEATURE CREEP

Do not introduce a feature merely because it sounds useful.

Before implementing a new feature, verify:

```text
PRD
+
Business Rules
+
API Contract
+
UI/UX Specification
+
Scope
```

If it changes product behavior materially, it must be explicitly approved.

---

# 48. CODE QUALITY

Priorities:

```text
Correctness
>
Consistency
>
Maintainability
>
Complexity
```

Avoid unnecessary abstraction.

Avoid:

- Premature optimization.
- Duplicate logic.
- Giant components.
- Giant utility files.
- Unused dependencies.
- Unused state.
- Hidden business rules.

Prefer small domain-focused modules.

---

# 49. TYPESCRIPT RULES

Use strict TypeScript.

Avoid:

```typescript
any
```

unless there is a documented reason.

Prefer explicit types.

API response types should correspond to domain types.

Do not silently cast invalid API data to satisfy TypeScript.

---

# 50. DATABASE RULE

Database schema follows the finalized Data Dictionary and Data Model.

Do not invent columns casually.

If a required field is missing:

```text
Check Data Model
→ Check API Contract
→ Check Business Rules
```

Only then modify the schema.

---

# 51. BUSINESS RULE CHANGE PROCESS

When changing business logic:

```text
1. Identify affected rule.
2. Update Business Rules / Decision Logic.
3. Update API Contract if response/input changes.
4. Update Data Model if schema changes.
5. Update AI/ML Specification if intelligence changes.
6. Update UI/UX if user behavior changes.
7. Implement.
8. Verify.
```

Do not change backend calculations silently.

---

# 52. TESTING / VERIFICATION

Current frontend has no dedicated test suite.

After frontend changes:

```bash
npm run lint
npm run build
```

At minimum.

For backend changes, add/execute relevant automated tests when backend implementation exists.

Critical business logic should eventually have deterministic tests.

Priority test areas:

- HPP.
- Pricing.
- Forecast fallback.
- Restock.
- Profitability.
- Business Health.
- Decision monitoring.
- Authorization.
- Transaction/inventory atomicity.

---

# 53. ACCEPTANCE MINDSET

For every implementation, ask:

```text
What happens on the happy path?
What happens when data is missing?
What happens when input is invalid?
What happens when the API fails?
What happens when the user rejects a recommendation?
What happens when data is insufficient?
```

Do not implement only the happy path.

---

# 54. DATA SUFFICIENCY

The system must distinguish:

```text
No Data
Limited Data
Sufficient Data
```

Do not treat these states as equivalent.

Example:

```text
No sales
→ No reliable forecast.

Limited sales
→ Simple estimate + Low Confidence.

Sufficient sales
→ Appropriate forecasting method.
```

---

# 55. EXPLAINABILITY

Every recommendation should expose:

```text
Recommendation
+
Reason
+
Supporting Data
```

Example:

```text
Harga rekomendasi: Rp14.000

Alasan:
HPP: Rp5.500
Margin saat ini: 54.2%
Target margin: 60%
```

The explanation must be traceable to backend values.

---

# 56. USER CONTROL

Never convert a recommendation into an automatic action unless explicitly approved as a future product change.

Examples:

```text
Smart Pricing
→ recommends price
→ user decides

Smart Restock
→ recommends quantity
→ user decides

Growth Map
→ recommends next step
→ user decides
```

---

# 57. FRONTEND PERFORMANCE

Avoid unnecessary:

- Client Components.
- API requests.
- Re-renders.
- Large context payloads.
- Recalculation of backend metrics.

Use server-side/backend aggregation for expensive business analysis.

---

# 58. ACCESSIBILITY

Interactive UI must:

- Be keyboard accessible.
- Have visible focus state.
- Use semantic labels.
- Not rely only on color.
- Provide readable empty/error states.
- Provide supporting text for charts where necessary.

---

# 59. MOBILE

The product is responsive.

Priority on mobile:

```text
Status
→ Key Metric
→ Recommendation
→ Action
→ Detail
```

Do not force complex desktop tables into narrow screens without adaptation.

---

# 60. AI AGENT WORKFLOW

When an AI coding agent receives a task:

```text
1. Understand requested change.
2. Read relevant existing code.
3. Check this AGENT CONTEXT.
4. Check relevant specification document.
5. Identify affected domain.
6. Implement smallest correct change.
7. Run lint/build/tests where available.
8. Report changes and verification.
```

Do not rewrite unrelated files.

---

# 61. SPECIFICATION PRIORITY

When documents conflict, use this priority:

```text
1. Explicit latest user/team decision
2. Business Rules & Decision Logic
3. Data Dictionary & Data Model
4. API Contract
5. AI / ML Specification
6. UI / UX Specification
7. Existing demo implementation
```

Existing demo code is evidence of current implementation, not automatically the final business rule.

---

# 62. SOURCE-OF-TRUTH PRINCIPLE

Different concerns have different sources of truth:

```text
Business behavior
→ Business Rules

Data structure
→ Data Model

API behavior
→ API Contract

AI/ML behavior
→ AI/ML Specification

UI behavior
→ UI/UX Specification

Current implementation
→ Source code
```

Do not use source code alone to infer a new business requirement.

---

# 63. IMPORTANT CURRENT FRONTEND NOTES

The current frontend report identifies these known gaps:

- Backend FastAPI + MySQL has not yet been implemented.
- Authentication is not real yet.
- CRUD persistence is not implemented.
- Inventory update is currently simulated.
- Data resets on reload.
- Rebranding KIRA → DATARA is incomplete.
- Legacy `owner | staff` type remains.
- Mock data currently drives analytics.
- There is no frontend test suite.

These are implementation gaps, not reasons to expand scope.

---

# 64. LEGACY DEMO ALGORITHM NOTE

The current demo implementation includes simplified formulas for:

- Product profitability.
- Smart Pricing.
- Forecasting.
- Smart Restock.
- Product classification.
- Dashboard metrics.
- Growth stages.

These demo algorithms may be used as implementation references, but production behavior must follow the finalized specification documents.

Do not copy demo-specific hardcoded dates, scores, or fake confidence values into production.

---

# 65. FINAL DEVELOPMENT RULES

1. DATARA is a decision-support system.
2. Backend is authoritative for business calculations.
3. Frontend is primarily presentation and interaction.
4. User remains the final decision maker.
5. Recommendations are not automatic actions.
6. Rule-based logic determines core business recommendations.
7. Statistical/ML methods support forecasting.
8. LLM explains and assists; it does not invent decisions.
9. LLM has no direct database authority.
10. Business data must be isolated per authenticated business.
11. HPP separates product cost from operating expenses.
12. HPP is calculated per unit.
13. Smart Pricing must remain realistic and profitable.
14. Smart Restock uses forecast, stock, and configurable Safety Days.
15. Forecasting supports limited data through fallback estimates with low confidence.
16. Business Health uses `SEHAT`, `PERLU_PERHATIAN`, `BERISIKO`.
17. Decision monitoring uses actual data before vs after application.
18. Growth Map is rule-based.
19. API fields use snake_case.
20. Next.js 16 Promise-based route params/searchParams must be respected.
21. Shared UI components should be reused.
22. Server Components use the icon wrapper.
23. `npm run lint` and `npm run build` are required verification steps for frontend changes.
24. Do not add features outside approved scope.
25. Do not silently alter finalized business logic.
26. Keep implementation simple, explainable, and maintainable.
27. Prefer deterministic calculations over LLM-generated calculations.
28. Treat user input and AI prompts as untrusted.
29. Validate on the backend.
30. Keep documentation and implementation aligned.

---

# 66. DOCUMENT STATUS

**AGENT CONTEXT / AI DEVELOPMENT GUIDELINES: FINAL**

This document is the operational context for developers and AI coding agents working on DATARA.

Before implementing a significant change, consult the relevant specification rather than relying solely on existing demo code.
