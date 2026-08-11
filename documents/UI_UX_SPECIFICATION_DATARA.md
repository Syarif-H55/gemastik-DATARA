# UI/UX SPECIFICATION
## DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM

**Status:** FINAL  
**Platform:** Responsive Web Application  
**Primary User:** Pemilik UMKM makanan dan minuman skala mikro  
**Frontend:** Next.js + React + TypeScript  
**UI Library:** shadcn/ui  
**Styling:** Tailwind CSS  
**Visualization:** Recharts  
**Icon:** Phosphor Icons

---

# 1. UI/UX Overview

DATARA dirancang untuk membantu pemilik UMKM memahami kondisi bisnis tanpa harus melakukan analisis data secara manual.

Prinsip utama:

```text
Data
 ↓
Insight
 ↓
Recommendation
 ↓
Decision
 ↓
Monitoring
```

UI harus memprioritaskan:

- Kejelasan.
- Kesederhanaan.
- Actionability.
- Explainability.
- Konsistensi.
- Responsive design.

Pengguna tidak seharusnya dipaksa memahami istilah akuntansi atau machine learning untuk menggunakan fitur utama.

---

# 2. UX Principles

## 2.1 Simple First

Informasi utama ditampilkan terlebih dahulu.

Contoh:

```text
Business Health
SEHAT

Omzet
Rp12,5 jt

Laba
Rp4 jt
```

Detail dapat dibuka setelahnya.

## 2.2 Decision-Oriented

Setiap analytical output harus membantu user menjawab:

```text
Apa yang terjadi?
Mengapa?
Apa yang sebaiknya dilakukan?
```

## 2.3 Explainable

Recommendation harus memiliki alasan.

Contoh:

```text
Harga direkomendasikan Rp14.000

Karena:
HPP Rp5.500
Margin saat ini 54,2%
Target margin 60%
```

## 2.4 User Remains in Control

DATARA memberikan recommendation, bukan tindakan otomatis.

```text
Recommendation
      ↓
User Review
      ↓
Apply / Ignore
```

## 2.5 Progressive Disclosure

Informasi kompleks ditampilkan bertahap.

```text
Summary
  ↓
Key Insight
  ↓
Detail
```

## 2.6 Consistency

Komponen yang memiliki fungsi sama harus menggunakan pola UI yang sama.

---

# 3. Visual Design System

## 3.1 General Style

Karakter visual:

- Modern.
- Clean.
- Professional.
- Data-oriented.
- Tidak terlalu ramai.
- Cocok untuk penggunaan harian.

## 3.2 Typography

Frontend menggunakan:

- Geist untuk primary sans.
- Geist Mono / JetBrains Mono untuk data tertentu.

Hierarchy:

```text
Page Title
  ↓
Section Heading
  ↓
Card Title
  ↓
Body
  ↓
Supporting Text
```

## 3.3 Color Semantics

Warna digunakan berdasarkan makna, bukan dekorasi.

```text
Primary
→ Action utama

Success / Emerald
→ Positif / Sehat / Profit

Warning / Amber
→ Perlu perhatian

Destructive / Red
→ Risiko / Masalah

Neutral / Slate
→ Informasi umum
```

Business Health:

```text
SEHAT
→ Success

PERLU_PERHATIAN
→ Warning

BERISIKO
→ Destructive
```

## 3.4 Spacing

Mengikuti spacing system Tailwind.

Prioritas:

```text
Small
→ Related elements

Medium
→ Components

Large
→ Sections
```

## 3.5 Border & Radius

Card dan container menggunakan border ringan dan radius konsisten.

## 3.6 Dark Mode

UI mendukung:

```text
Light
Dark
System
```

Theme toggle tersedia pada application shell.

---

# 4. Application Layout

## 4.1 Global Structure

```text
┌─────────────────────────────────────────────┐
│ Sidebar │ Header                            │
│         ├───────────────────────────────────┤
│         │                                   │
│         │       Main Content                 │
│         │                                   │
│         │                                   │
└─────────┴───────────────────────────────────┘
```

## 4.2 Sidebar

Navigasi utama:

1. Business Dashboard
2. Catat Transaksi
3. Sales Forecasting
4. Product Profitability
5. Smart Pricing
6. Smart Restock
7. Keputusan & Monitoring
8. Roadmap Pertumbuhan

Business Assistant dapat tersedia sebagai entry point global atau bagian aplikasi tanpa menambah menu utama yang berlebihan.

## 4.3 Header

Header:

- Sidebar trigger.
- Separator.
- Theme toggle.

## 4.4 Main Content

Padding responsive:

```text
Mobile:  p-4
Tablet:  p-6
Desktop: p-8
```

---

# 5. Responsive Design

DATARA menggunakan responsive web design.

## 5.1 Desktop

Sidebar tampil penuh.

Content menggunakan grid/card layout.

## 5.2 Tablet

Sidebar dapat diperkecil.

Grid menyesuaikan jumlah kolom.

## 5.3 Mobile

Sidebar menjadi collapsible/drawer.

Contoh:

```text
Desktop:
[Sidebar] [Content]

Mobile:
[Header]
[Content]
```

Table kompleks dapat menggunakan:

- Horizontal scroll.
- Stacked cards jika lebih sesuai.

## 5.4 Responsive Rule

Tidak boleh ada horizontal overflow pada layout utama.

Interactive controls harus tetap usable pada layar kecil.

---

# 6. Common Components

## 6.1 PageHeader

Digunakan pada setiap halaman utama.

Structure:

```text
Page Title
Description
Optional Actions
```

Contoh:

```text
Smart Pricing
Rekomendasi harga berdasarkan HPP dan target margin

[Target Margin]
```

## 6.2 ModuleBadge

Menandai status atau jenis modul.

## 6.3 EmptyState

Digunakan ketika data belum tersedia.

Format:

```text
Icon
Title
Description
Optional Action
```

## 6.4 Card

Untuk:

- Metric.
- Recommendation.
- Summary.
- Status.

## 6.5 Table

Untuk data dengan jumlah record lebih besar.

Fitur:

- Search.
- Filter.
- Sort.
- Pagination bila diperlukan.

## 6.6 Badge

Digunakan untuk:

- Status.
- Classification.
- Trend.
- Urgency.

## 6.7 Progress

Digunakan untuk:

- Business Health Score.
- Progress pertumbuhan.
- Confidence jika relevan.

## 6.8 Toast

Digunakan untuk feedback singkat:

```text
Success
Error
Warning
```

Contoh:

```text
Transaksi berhasil disimpan.
```

---

# 7. Navigation & Information Architecture

```text
DATARA
│
├── Business Dashboard
│
├── Operasional
│   └── Catat Transaksi
│
├── Analitik
│   ├── Sales Forecasting
│   └── Product Profitability
│
├── Rekomendasi
│   ├── Smart Pricing
│   └── Smart Restock
│
├── Keputusan
│   └── Keputusan & Monitoring
│
└── Pertumbuhan
    └── Roadmap Pertumbuhan
```

Business Assistant bersifat cross-feature.

---

# 8. Landing Page

Route:

```text
/
```

Tujuan:

Memperkenalkan DATARA dan mengarahkan user ke aplikasi.

Struktur:

```text
Hero
  ↓
Value Proposition
  ↓
Feature Summary
  ↓
CTA
```

Primary CTA:

```text
Masuk Aplikasi
```

Secondary CTA:

```text
Lihat Demo
```

Brand harus menggunakan:

```text
DATARA
```

bukan KIRA.

---

# 9. Login

Route:

```text
/login
```

Elements:

```text
DATARA Logo / Brand
Email
Password
Masuk
```

UX:

- Field validation.
- Loading state.
- Error state.
- Password visibility toggle jika diperlukan.

Setelah berhasil:

```text
/login
 ↓
/dashboard
```

---

# 10. Business Dashboard

Route:

```text
/dashboard
```

## 10.1 Objective

Memberikan ringkasan kondisi bisnis secara cepat.

## 10.2 Layout

```text
PageHeader
   ↓
Business Health
   ↓
Main Metrics
   ↓
Activity Metrics
   ↓
Revenue Trend
   ↓
Category Breakdown
```

## 10.3 Business Health Card

Menampilkan:

```text
Business Health
82 / 100
SEHAT
```

Disertai progress bar.

Status:

```text
SEHAT
PERLU_PERHATIAN
BERISIKO
```

## 10.4 Main Metrics

Minimal:

- Omzet.
- Laba.
- HPP/COGS.
- Margin rata-rata.

## 10.5 Activity Metrics

- Jumlah transaksi.
- Produk terjual.

## 10.6 Revenue Trend

Area/line chart.

Menampilkan:

```text
Omzet
Laba
```

## 10.7 Category Breakdown

Bar chart:

```text
Makanan
Minuman
Camilan
```

## 10.8 UX Rule

Dashboard tidak hanya menampilkan angka.

Jika terdapat kondisi penting, user harus dapat diarahkan ke modul terkait.

---

# 11. Catat Transaksi

Route:

```text
/transactions
```

## 11.1 Objective

Mencatat transaksi penjualan harian.

## 11.2 Layout

Desktop:

```text
┌─────────────────────┬──────────────────┐
│ Daftar Produk       │ Keranjang        │
│                     │                  │
│ Product cards       │ Items            │
│                     │ Total            │
│                     │ Payment          │
│                     │ [Simpan]         │
└─────────────────────┴──────────────────┘
```

## 11.3 Product Selection

Product ditampilkan sebagai clickable card/button.

Menampilkan:

```text
Nama
Harga
Stok
```

Jika sudah dipilih:

```text
Qty
```

ditampilkan.

## 11.4 Cart

Fitur:

- Increase quantity.
- Decrease quantity.
- Remove item.
- Stock validation.

Tidak boleh memilih quantity melebihi stok.

## 11.5 Optional Customer Name

Field:

```text
Nama Pelanggan
```

optional.

## 11.6 Payment

Field:

```text
Uang Diterima
```

Jika relevan, tampilkan:

```text
Total
Bayar
Kembalian
```

## 11.7 Submit

Button:

```text
Simpan Transaksi
```

Success:

```text
Transaksi berhasil disimpan.
```

Backend juga memperbarui inventory secara atomic.

---

# 12. Sales Forecasting

Route:

```text
/forecasting
```

## 12.1 Objective

Menampilkan prediksi penjualan produk dan membantu user memahami demand.

## 12.2 Layout

```text
PageHeader
   ↓
Product Selector
   ↓
Forecast Summary Cards
   ↓
Forecast Chart
   ↓
Trend Badge
   ↓
Reasoning
```

## 12.3 Product Selector

Dropdown:

```text
Pilih Produk
```

Perubahan produk memperbarui seluruh analytical content.

## 12.4 Summary Cards

Minimal:

- Prediksi periode.
- Estimasi penjualan unit.
- Confidence.

## 12.5 Forecast Chart

Line chart:

```text
Actual ─────
Forecast - - - -
```

Reference line digunakan untuk membedakan historical dan forecast.

## 12.6 Trend

Allowed:

```text
Tren Naik
Tren Menurun
Stabil
```

## 12.7 Reasoning

Contoh:

```text
Penjualan menunjukkan tren meningkat
dalam beberapa periode terakhir.
```

Confidence rendah harus diberi konteks bahwa data historis masih terbatas.

---

# 13. Product Profitability

Route:

```text
/products
```

## 13.1 Objective

Membantu user mengidentifikasi produk yang menguntungkan, potensial, dan perlu dievaluasi.

## 13.2 Summary

Tiga card:

```text
Menguntungkan
Berpotensi
Perlu Evaluasi
```

## 13.3 Product Table

Columns:

```text
Produk
Harga Jual
HPP
Laba/Unit
Margin
Terjual
Total Laba
Klasifikasi
```

## 13.4 Search

Search berdasarkan:

```text
Nama
SKU
```

## 13.5 Filter

Category:

```text
Semua
Minuman
Makanan
Camilan
```

Classification:

```text
Semua
Menguntungkan
Berpotensi
Perlu Evaluasi
```

## 13.6 Sort

Click column header untuk:

```text
Ascending
Descending
```

## 13.7 Margin Semantics

```text
≥40%
→ Positive

≥25%
→ Warning / Moderate

<25%
→ Risk
```

Classification menggunakan backend result sebagai source of truth.

Frontend tidak menghitung ulang authoritative classification.

---

# 14. Smart Pricing

Route:

```text
/pricing
```

## 14.1 Objective

Membantu user menentukan harga jual berdasarkan HPP dan target margin.

## 14.2 Layout

```text
PageHeader
   ↓
Target Margin Control
   ↓
Recommendation Table
```

## 14.3 Target Margin

Slider:

```text
10% ───────── 60%
```

Default dapat:

```text
30%
```

Nilai yang ditampilkan secara jelas.

## 14.4 Recommendation Table

Columns:

```text
Produk
Harga Saat Ini
HPP
Margin Aktual
Harga Rekomendasi
Alasan
Action
```

## 14.5 Recommendation Highlight

Jika harga berubah:

```text
Recommended Price
```

diberi visual emphasis.

## 14.6 Reasoning

Contoh:

```text
Margin saat ini berada di bawah target.
Harga direkomendasikan untuk dinaikkan agar
profitabilitas lebih sehat.
```

## 14.7 Apply

Button:

```text
Terapkan
```

atau:

```text
Terapkan Semua
```

Tindakan ini memerlukan user confirmation jika menerapkan banyak recommendation.

Setelah apply:

```text
Recommendation
 ↓
User confirms
 ↓
Backend updates product price
 ↓
Decision recorded
```

Recommendation yang hanya ditampilkan tidak mengubah harga.

---

# 15. Smart Restock

Route:

```text
/restock
```

## 15.1 Objective

Membantu user menentukan produk yang perlu direstock dan jumlah yang disarankan.

## 15.2 Layout

```text
PageHeader
   ↓
Restock Summary
   ↓
Recommendation List/Table
```

## 15.3 Recommendation Data

Minimal:

```text
Produk
Stok Saat Ini
Days of Supply
Suggested Quantity
Urgency
Reasoning
Action
```

## 15.4 Urgency

```text
critical
low
healthy
```

Visual semantics:

```text
critical → Destructive
low      → Warning
healthy  → Success
```

## 15.5 Action

Button:

```text
Restock
```

Flow:

```text
Recommendation
 ↓
User clicks Restock
 ↓
Backend creates received movement
 ↓
Stock increases
 ↓
Decision recorded
```

---

# 16. Keputusan & Monitoring

Route:

```text
/decisions
```

## 16.1 Objective

Menampilkan keputusan yang telah diterapkan dan memantau hasilnya.

## 16.2 Decision Card / Table

Menampilkan:

```text
Decision
Type
Applied At
Before
After
Outcome
Notes
```

## 16.3 Metrics

Minimal:

```text
Revenue
Margin
Stock
```

## 16.4 Before vs After

Gunakan visual comparison:

```text
Before → After
```

Contoh:

```text
Margin
54.2% → 60.7%
```

## 16.5 Outcome

Allowed:

```text
Improved
Flat
Regressed
```

Outcome dihitung berdasarkan data aktual.

Frontend menampilkan hasil dari backend.

---

# 17. Roadmap Pertumbuhan

Route:

```text
/growth
```

## 17.1 Objective

Menunjukkan posisi bisnis dan langkah berikutnya.

## 17.2 Growth Stages

UI dapat menggunakan timeline/stepper:

```text
● Catat & Konsisten
│
● Pahami Profitabilitas
│
◉ Keputusan Berbasis Data
│
○ Perluas Menuju Pertumbuhan
```

Status:

```text
done
current
next
upcoming
```

## 17.3 Stage Detail

Menampilkan:

```text
Stage
Description
Metric
Current Value
Target
Next Step
```

## 17.4 UX Principle

Roadmap tidak hanya memberi label.

User harus mengetahui:

```text
Posisi saya sekarang
       ↓
Apa yang belum tercapai
       ↓
Apa langkah berikutnya
```

---

# 18. Business Assistant

## 18.1 Purpose

Business Assistant membantu user memahami data, recommendation, dan kondisi bisnis menggunakan bahasa natural.

## 18.2 Access

Business Assistant dapat tersedia sebagai:

- Floating assistant.
- Panel/chat drawer.
- Dedicated assistant surface.

Untuk MVP, pola **chat drawer/panel** lebih sederhana daripada menambah menu utama.

## 18.3 Chat UI

```text
┌─────────────────────────────┐
│ DATARA Business Assistant   │
├─────────────────────────────┤
│ Assistant message           │
│                             │
│              User message   │
│                             │
├─────────────────────────────┤
│ Tulis pertanyaan...   [→]   │
└─────────────────────────────┘
```

## 18.4 Suggested Questions

Contoh:

```text
Kenapa keuntungan saya turun?
Produk mana yang paling menguntungkan?
Kenapa harga ini direkomendasikan?
Kapan saya perlu restock?
```

## 18.5 Response

AI response harus:

- Singkat terlebih dahulu.
- Berdasarkan business context.
- Menyertakan alasan jika diperlukan.
- Tidak mengarang angka.

## 18.6 Scope Message

Jika pertanyaan tidak relevan:

```text
Maaf, saya fokus membantu Anda memahami
dan mengelola bisnis melalui DATARA.
```

## 18.7 Action Boundary

AI tidak boleh menampilkan seolah-olah sudah melakukan action jika user belum menerapkannya.

---

# 19. Recommendation UX Pattern

Semua recommendation menggunakan pola yang konsisten.

```text
┌────────────────────────────────────────┐
│ Recommendation                         │
│                                        │
│ What should I do?                      │
│                                        │
│ Recommended value                      │
│                                        │
│ Why?                                   │
│ Supporting data                        │
│                                        │
│ [Apply] [Ignore]                       │
└────────────────────────────────────────┘
```

Elemen:

1. Recommendation.
2. Reason.
3. Supporting data.
4. Action.
5. Optional status.

---

# 20. Status & Feedback

## 20.1 Loading

Gunakan:

- Skeleton.
- Spinner pada action.
- Disabled button saat request berlangsung.

## 20.2 Empty

Contoh:

```text
Belum ada data transaksi
Mulai catat transaksi untuk melihat analisis bisnis.
```

## 20.3 Error

Error harus:

- Jelas.
- Tidak teknis berlebihan.
- Menyediakan action jika memungkinkan.

Contoh:

```text
Data belum dapat dimuat.
Coba lagi.
```

## 20.4 Success

Toast:

```text
Transaksi berhasil disimpan.
Harga berhasil diterapkan.
Restock berhasil dicatat.
```

---

# 21. Form UX

Form mengikuti:

```text
Label
Input
Helper Text
Validation
```

Error ditampilkan dekat field.

Contoh:

```text
Target Margin
[ 30 ]

Target margin harus berada antara 10% dan 60%.
```

---

# 22. Data Formatting

Frontend menggunakan locale:

```text
id-ID
```

## Currency

```text
Rp12.500
```

## Percentage

```text
30.0%
```

## Number

```text
12.500
```

## Date

```text
11 Agu 2026
```

## Date Time

```text
11 Agu 2026, 10:30
```

---

# 23. Accessibility

Minimum requirements:

- Semantic HTML.
- Keyboard-accessible controls.
- Visible focus state.
- Label pada form input.
- Tooltip tidak menjadi satu-satunya sumber informasi penting.
- Warna tidak menjadi satu-satunya indikator status.
- Chart memiliki supporting text/summary.
- Button memiliki label yang jelas.

Contoh:

Jangan hanya:

```text
[✓]
```

Gunakan:

```text
[✓ Terapkan]
```

---

# 24. Interaction Rules

## 24.1 Destructive Action

Action yang dapat menyebabkan perubahan penting harus memiliki confirmation jika risikonya tinggi.

## 24.2 Apply Recommendation

User harus mengetahui:

```text
Apa yang berubah?
```

sebelum apply.

Contoh:

```text
Harga:
Rp12.000 → Rp14.000
```

## 24.3 Restock

User harus mengetahui:

```text
Jumlah yang akan ditambahkan.
```

## 24.4 Disabled State

Button disabled ketika:

- Request sedang berjalan.
- Input invalid.
- Action tidak tersedia.

---

# 25. Frontend State Model

Setiap page minimal menangani:

```text
idle
loading
success
empty
error
```

Untuk mutation:

```text
idle
submitting
success
error
```

---

# 26. API Integration UX

Target architecture:

```text
Page
 ↓
API Client
 ↓
REST API
 ↓
Backend
```

Frontend tidak boleh:

```text
Page
 ↓
Direct Database
```

Mock/demo data harus digantikan dengan API backend.

---

# 27. Frontend Domain Types

Frontend types harus konsisten dengan API.

Key entities:

```text
User
Product
ProductProfitability
InventoryLog
Transaction
TransactionItem
Cost
PricingRecommendation
RestockRecommendation
ProductForecast
DashboardMetrics
BusinessHealth
Decision
DecisionRecord
GrowthStage
```

JSON field:

```text
snake_case
```

---

# 28. Chart UX

Chart digunakan untuk membantu pemahaman, bukan sekadar dekorasi.

Setiap chart harus memiliki:

- Title.
- Supporting context.
- Legend jika diperlukan.
- Tooltip.
- Axis labels bila relevan.
- Summary text untuk accessibility.

Chart tidak boleh menjadi satu-satunya cara memahami informasi penting.

---

# 29. Mobile UX Priority

Pada mobile, prioritas informasi:

```text
1. Health / Status
2. Key Metric
3. Recommendation
4. Action
5. Detail
```

Contoh Smart Pricing:

```text
Product
 ↓
Current Price
 ↓
Recommended Price
 ↓
Reason
 ↓
Apply
```

Bukan memaksakan seluruh tabel desktop ke layar kecil.

---

# 30. UX Consistency Matrix

| Pattern | Dashboard | Forecast | Products | Pricing | Restock | Decisions | Growth |
|---|---:|---:|---:|---:|---:|---:|---:|
| PageHeader | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cards | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Badge | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Table | - | - | ✓ | ✓ | ✓ | ✓ | - |
| Chart | ✓ | ✓ | - | - | - | ✓ | - |
| Action Button | ✓ | - | - | ✓ | ✓ | ✓ | ✓ |
| Empty State | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

# 31. Frontend Implementation Constraints

1. Gunakan Next.js App Router.
2. Gunakan TypeScript strict mode.
3. Gunakan Tailwind CSS.
4. Gunakan shadcn/ui untuk komponen UI standar.
5. Gunakan Phosphor Icons.
6. Gunakan Recharts untuk data visualization.
7. Gunakan `PageHeader`, `EmptyState`, dan `ModuleBadge` sebagai shared component jika sesuai.
8. Server Component menggunakan icon wrapper `kira-icons.tsx`.
9. Client Component dapat mengimpor Phosphor Icons secara langsung.
10. Jangan membuat duplicate component jika shared component sudah tersedia.
11. Gunakan `src/lib/format.ts` untuk formatting.
12. Gunakan `src/lib/api.ts` untuk komunikasi API.
13. Gunakan `snake_case` pada API data.
14. Backend menjadi source of truth.
15. Jangan mempertahankan business calculation authoritative di frontend.
16. Mock data hanya untuk development/demo sampai API terhubung.
17. Setelah integrasi backend, UI harus menangani loading, empty, error, dan success state.
18. Rebranding KIRA → DATARA harus konsisten pada seluruh UI.
19. Produk menggunakan satu actor utama: Pemilik UMKM.
20. UI tidak boleh bergantung pada role `staff` sebagai actor produk.

---

# 32. Current Frontend-to-Production Migration

Current:

```text
demo-data.ts
      ↓
Client Components
      ↓
UI
```

Target:

```text
FastAPI
      ↓
REST API
      ↓
api.ts
      ↓
React Components
      ↓
UI
```

Analytical calculation harus dipindahkan dari client ke backend.

---

# 33. Existing Frontend Alignment

Frontend saat ini telah menyediakan:

- Business Dashboard.
- Catat Transaksi.
- Sales Forecasting.
- Product Profitability.
- Smart Pricing.
- Smart Restock.
- Keputusan & Monitoring.
- Roadmap Pertumbuhan.

Komponen yang telah tersedia meliputi:

- AppShell.
- AppSidebar.
- PageHeader.
- EmptyState.
- ModuleBadge.
- ThemeProvider.
- ThemeToggle.
- shadcn/ui components.
- Mobile hook.
- Formatting helpers.

Dokumen frontend juga mencatat bahwa sebagian besar halaman saat ini menggunakan mock data dan belum terhubung ke backend. Hal tersebut diperlakukan sebagai tahap development, bukan arsitektur final. fileciteturn8file0L1-L18

---

# 34. Known UI Migration Items

## 34.1 Rebranding

Semua penggunaan:

```text
KIRA
```

harus diganti menjadi:

```text
DATARA
```

termasuk metadata, landing page, login, AppBrand, dan konfigurasi terkait. fileciteturn8file5L1-L12

## 34.2 Role

UI menggunakan:

```text
Pemilik UMKM
```

sebagai actor utama.

Tidak menampilkan workflow staff sebagai role terpisah.

## 34.3 Mock Data

`demo-data.ts` tidak menjadi source of truth production.

## 34.4 Client-side Analytics

Calculation seperti profitability, pricing, forecasting, dan dashboard metrics harus berasal dari backend setelah API tersedia.

Dokumen frontend saat ini memang mencatat bahwa seluruh algoritma demo masih berjalan di browser. fileciteturn8file8L1-L15

---

# 35. UX Quality Targets

UI/UX harus mendukung:

- User memahami Business Health dengan cepat.
- User dapat mencatat transaksi tanpa langkah berlebihan.
- User dapat memahami alasan recommendation.
- User mengetahui perubahan sebelum menerapkan recommendation.
- User dapat melihat hasil keputusan.
- User dapat memahami langkah pertumbuhan berikutnya.

Target usability yang tercantum pada PRD adalah minimal 80% pengguna uji dapat menyelesaikan skenario pengambilan keputusan tanpa bantuan. fileciteturn8file15L1-L12

---

# 36. Final UI/UX Rules

1. DATARA menggunakan responsive web application.
2. Primary actor adalah Pemilik UMKM.
3. Dashboard berorientasi pada Business Health dan key metrics.
4. Recommendation selalu disertai alasan.
5. User tetap memiliki kontrol atas keputusan.
6. Harga tidak berubah hanya karena recommendation dibuat.
7. Restock tidak dilakukan hanya karena recommendation dibuat.
8. Apply action harus memberikan feedback yang jelas.
9. Before/after digunakan untuk keputusan yang berdampak pada business metric.
10. Business Health menggunakan `SEHAT`, `PERLU_PERHATIAN`, `BERISIKO`.
11. Recommendation status harus jelas.
12. Loading, empty, error, dan success state wajib ditangani.
13. Data penting tidak boleh hanya direpresentasikan dengan warna.
14. Chart harus memiliki supporting context.
15. UI menggunakan `id-ID` untuk format bisnis Indonesia.
16. UI harus usable pada desktop, tablet, dan mobile.
17. Navigation utama menggunakan delapan modul utama yang sudah ditetapkan.
18. Business Assistant bersifat cross-feature dan tidak harus menjadi menu utama.
19. Frontend menggunakan API sebagai sumber data production.
20. Business calculation authoritative dilakukan backend.
21. Shared components digunakan untuk menjaga konsistensi.
22. Rebranding KIRA → DATARA harus tuntas.
23. UI tidak menampilkan role Staff sebagai actor produk.
24. Visual design memprioritaskan clarity daripada dekorasi.
25. UX harus membantu user bergerak dari data menuju insight, recommendation, decision, dan monitoring.

---

# 37. Document Status

**UI/UX SPECIFICATION: FINAL**

Dokumen ini menjadi acuan untuk:

- Implementasi frontend.
- Design system.
- Page layout.
- Navigation.
- Responsive behavior.
- Component usage.
- User interaction.
- Recommendation presentation.
- API integration state.
- Accessibility.
- Production migration dari mock data ke backend.
