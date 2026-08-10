# DATARA

## Business Rules & Decision Logic

**Application:** DATARA
**Full Name:** Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM
**Document:** Business Rules & Decision Logic
**Status:** Final
**Version:** 1.0

---

# 1. Business Rules Overview

## 1.1 Purpose

Dokumen ini mendefinisikan aturan bisnis, logika perhitungan, logika pengambilan keputusan, dependency antarfitur, serta batas penggunaan AI/LLM pada DATARA.

Business Rules menjadi dasar bagi:

* Backend development
* Database design
* API design
* Decision Support System (DSS)
* Smart Pricing
* Sales Forecasting
* Smart Restock
* Business Health
* Growth Map
* Notification
* AI/LLM Business Assistant

Dokumen ini harus menjadi **source of truth** untuk aturan bisnis DATARA.

---

## 1.2 Core Principle

DATARA dirancang untuk membantu pemilik UMKM makanan dan minuman skala mikro mengambil keputusan bisnis berdasarkan data.

Prinsip utama:

> **Data → Analisis → Keputusan → Rekomendasi → Insight**

DATARA tidak hanya mencatat data transaksi, tetapi mengolah data tersebut menjadi rekomendasi yang dapat digunakan oleh pengguna.

---

# 2. User & Business Scope

## 2.1 Target User

Target utama DATARA adalah:

> Pemilik UMKM makanan dan minuman skala mikro yang telah memiliki transaksi harian tetapi belum memanfaatkan data penjualan untuk mengambil keputusan bisnis.

Pengguna diasumsikan memiliki pemahaman bisnis yang praktis dan sederhana, sehingga sistem harus menghindari kompleksitas akuntansi atau analitik yang tidak diperlukan.

---

## 2.2 User Role

Untuk versi awal DATARA hanya menggunakan satu peran utama:

> **Business Owner / UMKM Owner**

Role Admin atau Staff tidak digunakan dalam MVP karena belum ditemukan fungsi bisnis yang cukup kuat untuk membenarkan kompleksitas tambahan tersebut.

---

## 2.3 Business Decision Scope

DATARA berfokus pada keputusan:

* Penentuan harga jual
* Analisis HPP dan profitabilitas
* Analisis performa penjualan
* Sales forecasting
* Restock inventory
* Evaluasi kesehatan bisnis
* Penentuan arah pertumbuhan bisnis
* Pemberian rekomendasi bisnis

---

# 3. Product & Cost Rules

## 3.1 Product

Setiap produk minimal memiliki:

* Nama produk
* Unit
* Harga jual
* HPP per unit jika sudah tersedia
* Status aktif/nonaktif

Produk yang sudah memiliki historical transaction tidak boleh dihapus secara permanen karena dapat merusak histori analisis.

Produk tersebut sebaiknya diubah menjadi:

```text
Active
Inactive
```

Produk inactive tidak digunakan untuk transaksi baru, tetapi historical transaction tetap tersedia untuk analisis.

---

# 4. HPP & Profitability Logic

## 4.1 HPP Definition

HPP dihitung dari biaya yang berhubungan langsung dengan pembuatan produk.

Komponen utama:

```text
HPP / Unit
=
Bahan Baku
+
Kemasan
+
Tenaga Kerja Langsung
+
Allocated Production Overhead
```

Untuk tahap awal, overhead produksi dapat dialokasikan menggunakan metode sederhana.

DATARA tidak bertujuan membuat sistem akuntansi biaya yang kompleks.

---

## 4.2 Fixed Cost

Fixed Cost seperti:

* Sewa tempat
* Gaji tetap
* Biaya administrasi
* Biaya operasional tetap lainnya

tidak dimasukkan langsung ke HPP produk.

Fixed Cost dicatat sebagai:

> **Operating Expense**

---

## 4.3 Variable Cost

Variable Cost yang berhubungan langsung dengan produk dimasukkan ke HPP.

Contoh:

* Bahan baku
* Kemasan
* Tenaga kerja langsung berdasarkan produksi

Biaya seperti listrik atau gas yang sulit ditelusuri secara langsung ke satu produk dapat dicatat sebagai:

> **Production Overhead / Operating Cost**

sesuai kebutuhan implementasi.

---

## 4.4 HPP per Unit

DATARA menghitung HPP per unit karena HPP menjadi dasar untuk:

* Smart Pricing
* Margin calculation
* Product profitability
* Profit analysis
* Decision Support System

Struktur:

```text
HPP / Unit
      ↓
Smart Pricing
      ↓
Margin
      ↓
Profit
      ↓
DSS
      ↓
Growth Map
```

---

## 4.5 Revenue

Revenue dihitung berdasarkan transaksi penjualan yang valid.

Formula:

```text
Revenue
=
Σ (Quantity × Selling Price)
```

Contoh:

```text
Quantity = 5
Selling Price = Rp12.000

Revenue = 5 × Rp12.000
        = Rp60.000
```

Revenue dihitung oleh backend dan menjadi source of truth.

---

## 4.6 Gross Profit

Gross Profit dihitung:

```text
Gross Profit
=
Revenue - COGS
```

Dengan:

```text
COGS
=
Σ (Quantity × HPP per Unit)
```

---

## 4.7 Net Profit

Net Profit:

```text
Net Profit
=
Gross Profit - Operating Expense
```

Dengan demikian:

```text
Revenue
   ↓
COGS
   ↓
Gross Profit
   ↓
Operating Expense
   ↓
Net Profit
```

---

## 4.8 Margin

Margin digunakan untuk mengevaluasi kemampuan produk/bisnis menghasilkan keuntungan.

Untuk produk:

```text
Gross Margin
=
(Selling Price - HPP) / Selling Price × 100%
```

Target margin dapat ditentukan oleh user.

DATARA tidak menggunakan satu target margin universal untuk seluruh UMKM.

---

# 5. Smart Pricing Decision Logic

## 5.1 Objective

Smart Pricing digunakan untuk memberikan rekomendasi harga jual yang:

* Menghasilkan profit
* Mempertimbangkan HPP
* Memenuhi target margin
* Tetap realistis bagi pasar
* Dapat mempertimbangkan faktor eksternal

---

## 5.2 Required Input

Minimal:

```text
HPP / Unit
Target Margin
Current Selling Price
```

Faktor tambahan dapat digunakan:

```text
Competitor Price
Historical Sales
Business Pricing Context
```

Data kompetitor bersifat **optional** dan hanya menjadi faktor pendukung.

---

## 5.3 Pricing Principle

User input menjadi faktor utama.

Faktor eksternal tidak boleh menjadi satu-satunya dasar keputusan.

Struktur:

```text
Internal Business Data
        ↓
Primary Factor
        +
External Market Factor
        ↓
Supporting Factor
        ↓
Recommended Price
```

---

## 5.4 Minimum Profitable Price

Harga rekomendasi tidak boleh menghasilkan kerugian.

Secara prinsip:

```text
Recommended Price > HPP
```

Untuk target margin:

```text
Required Price
=
HPP / (1 - Target Margin)
```

Contoh:

```text
HPP = Rp8.000
Target Margin = 30%

Required Price
=
8.000 / (1 - 0.30)
=
Rp11.429
```

Harga akhir dapat dibulatkan ke nilai yang realistis untuk digunakan pengguna.

---

## 5.5 Pricing Recommendation

Rekomendasi dapat mempertimbangkan:

* Harga saat ini
* HPP
* Target margin
* Harga kompetitor jika tersedia
* Posisi harga terhadap pasar
* Profitability

Sistem tetap harus mengutamakan harga yang realistis dan profitable.

---

# 6. Sales & Transaction Logic

## 6.1 Valid Transaction

Transaksi penjualan minimal memiliki:

* Transaction Date
* Product
* Quantity
* Selling Price

---

## 6.2 Transaction Quantity

Quantity harus:

```text
Quantity > 0
```

Nilai nol atau negatif tidak diperbolehkan untuk transaksi penjualan normal.

---

## 6.3 Transaction Status

Transaksi yang dibatalkan tidak digunakan dalam:

* Revenue
* Sales analysis
* Sales forecasting
* Inventory calculation

---

## 6.4 Historical Sales

Historical sales digunakan sebagai dasar:

```text
Sales Transaction
      ↓
Historical Sales
      ↓
Sales Analysis
      ↓
Forecasting
```

Kualitas dan kelengkapan historical sales akan memengaruhi kualitas forecast.

---

# 7. Inventory Rules

## 7.1 Stock

Current stock tidak boleh bernilai negatif dalam kondisi normal.

```text
Current Stock >= 0
```

---

## 7.2 Insufficient Stock

Jika user mencatat transaksi melebihi stok:

```text
Current Stock = 3
Transaction Quantity = 5
```

sistem menolak transaksi dan memberikan pesan:

> Stok tidak mencukupi. Stok saat ini 3 unit, sedangkan transaksi membutuhkan 5 unit.

DATARA tidak mengizinkan stock menjadi negatif dalam MVP.

---

## 7.3 Lead Time

Lead Time merupakan waktu yang dibutuhkan untuk memperoleh atau menerima stok dari supplier.

```text
Lead Time >= 0
```

Satuan default:

> Hari

---

## 7.4 Safety Days

User dapat menentukan Safety Days.

Safety Days memiliki default awal yang dapat dikonfigurasi oleh user.

```text
Safety Days >= 0
```

Safety Days digunakan sebagai faktor perlindungan tambahan dalam Smart Restock.

---

# 8. Sales Forecasting & Smart Restock

## 8.1 Sales Forecasting

Smart Restock memerlukan Sales Forecasting.

Alur:

```text
Historical Sales
      ↓
Sales Forecast
      ↓
Expected Demand
      ↓
Smart Restock
```

---

## 8.2 Forecast Period

Forecast digunakan untuk memprediksi kebutuhan penjualan pada periode mendatang.

Periode analisis utama dapat menggunakan periode bulanan sesuai kebutuhan dashboard dan evaluasi bisnis.

---

## 8.3 Insufficient Forecast Data

Jika data penjualan belum mencukupi:

```text
Forecast Status
=
INSUFFICIENT
```

Sistem tidak boleh menghasilkan nilai forecast yang dibuat-buat.

Perbedaan:

```text
Forecast = 0
```

berarti sistem memperkirakan tidak ada penjualan.

Sedangkan:

```text
Forecast = NULL
Status = INSUFFICIENT
```

berarti data belum cukup untuk menghasilkan prediksi.

---

## 8.4 Smart Restock

Smart Restock menggunakan:

* Sales Forecast
* Current Stock
* Lead Time
* Safety Days
* Expected Demand

Tujuan:

> Menentukan kapan dan berapa banyak stok yang perlu direstock.

---

## 8.5 Stock Status

Untuk MVP digunakan tiga kondisi:

```text
Aman
Perlu Restock
Prioritas Restock
```

### Aman

Stok masih cukup untuk memenuhi estimasi kebutuhan.

### Perlu Restock

Stok mulai mendekati batas kebutuhan.

### Prioritas Restock

Stok berisiko habis sebelum kebutuhan dapat dipenuhi berdasarkan forecast dan lead time.

---

## 8.6 Stock Coverage

Secara prinsip:

```text
Stock Coverage Days
=
Current Stock / Average Daily Demand
```

Jika:

```text
Stock Coverage <= Lead Time
```

maka produk berpotensi masuk:

> Prioritas Restock

Safety Days digunakan sebagai buffer tambahan.

---

## 8.7 Restock Quantity

Jumlah rekomendasi restock harus mempertimbangkan:

```text
Expected Demand
+
Safety Stock
-
Current Stock
```

Jumlah rekomendasi tidak boleh menghasilkan stok yang tidak realistis atau berlebihan tanpa dasar kebutuhan.

---

# 9. Business Growth & Decision Support System

## 9.1 DSS Objective

Decision Support System digunakan untuk mengubah hasil analitik menjadi keputusan bisnis yang dapat ditindaklanjuti.

Alur:

```text
Business Data
     ↓
Analysis
     ↓
Business Problem
     ↓
Decision
     ↓
Recommendation
```

---

## 9.2 Growth Strategy

DATARA menggunakan beberapa arah pertumbuhan utama:

```text
Increase Sales
Improve Profitability
Optimize Inventory
Scale Business
```

Strategi dipilih berdasarkan kondisi bisnis dan masalah utama.

---

## 9.3 Primary Problem

DATARA dapat menentukan masalah utama berdasarkan indikator yang menunjukkan kondisi paling membutuhkan perhatian.

Contoh:

```text
Sales ↓
Profit ↑
Inventory Aman

→ Primary Problem:
Sales Performance
```

Maka:

```text
Growth Strategy:
Increase Sales
```

---

## 9.4 Growth Map

Growth Map menghubungkan:

```text
Business Health
+
Primary Problem
+
Business Metrics
      ↓
Growth Strategy
```

Contoh:

```text
Health = Perlu Perhatian
Problem = Profitability
       ↓
Improve Profitability
```

---

## 9.5 Target

User dapat menentukan target bisnis seperti:

* Target penjualan
* Target revenue
* Target profit
* Target margin

Target merupakan:

> **Apa yang ingin dicapai user**

sedangkan forecast merupakan:

> **Apa yang diperkirakan akan terjadi berdasarkan data**

Keduanya tidak boleh disamakan.

---

## 9.6 Business Progress

DATARA dapat membandingkan performa bisnis antarperiode.

Contoh:

```text
Month 1:
Profit = Rp2.000.000

Month 2:
Profit = Rp2.400.000
```

Maka:

```text
Profit Growth = +20%
```

Perubahan performa dapat digunakan untuk mengevaluasi apakah kondisi bisnis mengalami perkembangan.

---

# 10. Business Health & Overall Decision Logic

## 10.1 Objective

Business Health memberikan gambaran kondisi bisnis secara keseluruhan.

Output hanya terdiri dari:

```text
Sehat
Perlu Perhatian
Berisiko
```

---

## 10.2 Health Indicators

Indikator utama:

* Revenue
* Profit
* Margin
* Sales
* Inventory

---

## 10.3 Indicator Status

Setiap indikator dapat memiliki status:

```text
Positive
Neutral
Negative
```

---

## 10.4 Revenue Status

Contoh threshold awal:

```text
Revenue Growth >= +10%
→ Positive

-10% < Revenue Growth < +10%
→ Neutral

Revenue Growth <= -10%
→ Negative
```

Threshold dapat dikonfigurasi apabila implementasi membutuhkan pendekatan yang lebih adaptif.

---

## 10.5 Sales Status

Sales menggunakan prinsip serupa:

```text
Sales Growth >= +10%
→ Positive

-10% < Sales Growth < +10%
→ Neutral

Sales Growth <= -10%
→ Negative
```

---

## 10.6 Profit Status

Profit menjadi indikator dengan prioritas tinggi.

### Positive

```text
Current Profit > 0
AND
Profit Growth >= 0%
```

### Neutral

```text
Current Profit > 0
AND
Profit Growth < 0%
```

### Negative

```text
Current Profit <= 0
```

---

## 10.7 Margin Status

Margin dibandingkan dengan target margin user.

### Positive

```text
Current Margin >= Target Margin
```

### Neutral

```text
Current Margin < Target Margin
AND
Gross Profit > 0
```

### Negative

```text
Gross Profit <= 0
```

---

## 10.8 Inventory Status

Inventory menggunakan hasil Smart Restock.

```text
Semua produk utama Aman
→ Positive

Ada produk Perlu Restock
→ Neutral

Ada kondisi Prioritas Restock yang signifikan
→ Negative
```

Business Health tidak menghitung ulang status inventory.

---

## 10.9 Overall Health Classification

DATARA menggunakan **Priority Rule**, bukan weighted scoring.

Prioritas:

```text
Berisiko
   ↓
Perlu Perhatian
   ↓
Sehat
```

---

### Berisiko

Business Health = **Berisiko** jika terdapat minimal satu kondisi kritis:

```text
Profit Negative
OR
Gross Profit <= 0
OR
terdapat kondisi Prioritas Restock yang signifikan
```

---

### Perlu Perhatian

Jika tidak memenuhi kondisi Berisiko, tetapi terdapat:

```text
>= 2 indikator Negative
```

maka:

> **Perlu Perhatian**

---

### Sehat

Jika:

* Tidak terdapat kondisi kritis.
* Kurang dari dua indikator Negative.
* Profit masih positif.
* Tidak terdapat risiko inventory signifikan.

maka:

> **Sehat**

---

## 10.10 Health Decision Flow

```text
Business Metrics
      ↓
Evaluate Indicators
      ↓
Ada kondisi kritis?
   /          \
 YES          NO
  ↓            ↓
BERISIKO    Hitung Negative Indicators
                 ↓
             >= 2 ?
             /    \
           YES     NO
            ↓       ↓
       PERHATIAN   SEHAT
```

---

## 10.11 Health → Growth Strategy

Business Health menjadi salah satu input Growth Map.

| Business Health | Possible Direction                                          |
| --------------- | ----------------------------------------------------------- |
| Berisiko        | Recovery / Improve Profitability                            |
| Perlu Perhatian | Increase Sales / Improve Profitability / Optimize Inventory |
| Sehat           | Scale Business / Maintain                                   |

Business Health tidak sendirian menentukan strategi.

Primary Problem tetap digunakan.

---

# 11. AI/LLM Insight & Business Assistant Logic

## 11.1 Objective

AI/LLM DATARA berfungsi sebagai:

> **Business Communication & Advisory Layer**

AI mengubah hasil analisis terstruktur menjadi:

* Insight
* Explanation
* Advice
* Business Answer

AI bukan source of truth untuk perhitungan bisnis.

---

## 11.2 AI Responsibilities

AI memiliki empat fungsi utama.

### Explain

Menjelaskan hasil analisis backend.

### Interpret

Menghubungkan beberapa hasil analisis untuk memberikan konteks.

### Recommend

Menyampaikan rekomendasi berdasarkan hasil Decision Engine.

### Answer Business Questions

Menjawab pertanyaan user berdasarkan Business Context DATARA.

---

## 11.3 AI Input Context

AI tidak menerima seluruh database secara mentah.

Backend membuat:

> **Structured Business Context**

Contoh:

```json
{
  "business": {
    "health_status": "PERLU_PERHATIAN"
  },
  "performance": {
    "revenue_growth": 5.2,
    "sales_growth": 8.1,
    "profit_growth": -10.4
  },
  "pricing": {
    "products_below_target_margin": 2
  },
  "inventory": {
    "priority_restock_products": 1
  },
  "growth": {
    "primary_strategy": "IMPROVE_PROFITABILITY"
  }
}
```

Alur:

```text
Database
   ↓
Backend
   ↓
Structured Context
   ↓
AI / LLM
```

---

## 11.4 Conversation Context

AI menggunakan dua jenis konteks:

### Current Business Context

Kondisi bisnis terbaru:

* Revenue
* Profit
* Margin
* Sales
* Stock
* Forecast
* Health
* Growth Strategy

### Conversation Context

Percakapan yang sedang berlangsung.

Contoh:

```text
User:
Kenapa profit saya turun?

AI:
Profit turun karena HPP meningkat lebih cepat dibanding revenue.

User:
Produk mana yang paling berpengaruh?

AI:
Produk A memiliki penurunan margin terbesar.
```

AI dapat mempertahankan konteks percakapan tanpa harus menyimpan seluruh percakapan sebagai satu-satunya sumber pengetahuan bisnis.

---

## 11.5 Business Progress Conversation

DATARA dapat menggunakan historical business context untuk membantu user memahami perkembangan bisnis.

Contoh:

```text
Month 1
Health = Perlu Perhatian

Month 2
Health = Sehat
Profit Growth = +15%
```

Jika user bertanya:

> "Bisnis saya membaik nggak?"

AI dapat menjelaskan perubahan berdasarkan historical metrics.

---

## 11.6 AI Output Structure

Output AI idealnya memiliki struktur:

```text
Insight
↓
Reason
↓
Recommendation
↓
Expected Impact
```

Tidak semua respons harus selalu menggunakan keempat bagian.

---

## 11.7 AI Decision Boundary

AI tidak boleh mengubah:

* HPP
* Revenue
* Profit
* Margin
* Forecast
* Recommended Price
* Recommended Restock
* Business Health
* Growth Strategy

AI hanya menjelaskan hasil yang telah ditentukan backend.

---

## 11.8 Insufficient Data

Jika data tidak cukup:

```text
Forecast Status = INSUFFICIENT
```

AI tidak boleh membuat nilai prediksi sendiri.

Contoh respons:

> Data penjualan yang tersedia belum cukup untuk menghasilkan forecast yang dapat digunakan. Tambahkan transaksi penjualan agar DATARA dapat melakukan analisis demand.

---

## 11.9 Hallucination Prevention

Backend dapat memberikan:

```text
Structured Context
+
Allowed Facts
```

AI hanya boleh membuat penjelasan berdasarkan fakta tersebut.

Jika informasi tidak tersedia:

> Data tersebut belum tersedia.

AI tidak boleh mengarang angka, kondisi bisnis, atau hasil analisis.

---

## 11.10 AI Response Modes

Untuk MVP digunakan tiga mode:

### Insight Mode

Digunakan untuk insight otomatis dari dashboard.

```text
Business Context
↓
AI
↓
Business Insight
```

### Question Mode

Digunakan ketika user mengajukan pertanyaan.

```text
User Question
+
Business Context
↓
AI
↓
Answer
```

### Recommendation Explanation Mode

Digunakan untuk menjelaskan rekomendasi tertentu.

```text
Recommendation
+
Decision Factors
↓
AI
↓
Explanation
```

---

## 11.11 AI Scope

AI dibatasi sebagai:

> **Business Assistant DATARA**

Namun AI tetap boleh menjawab pertanyaan umum selama relevan dengan bisnis UMKM.

### In-Scope

* Penjualan
* Pricing
* HPP
* Margin
* Profit
* Inventory
* Forecasting
* Promosi
* Marketing
* Produk
* Business growth
* Interpretasi data DATARA
* Business management
* Strategi UMKM

---

## 11.12 Context-Aware Business Questions

Pertanyaan umum yang masih relevan dengan bisnis boleh dijawab.

Contoh:

> "Apa strategi bundling yang cocok untuk bisnis makanan?"

Boleh dijawab berdasarkan pengetahuan umum.

Namun:

> "Bundling apa yang paling cocok untuk bisnis saya?"

harus menggunakan Business Context jika data yang dibutuhkan tersedia.

---

## 11.13 Out-of-Scope Handling

Jika pertanyaan tidak memiliki relevansi dengan bisnis UMKM, AI tidak perlu menjawab secara panjang.

Contoh:

> "Siapa presiden Indonesia?"

Respons diarahkan kembali:

> Saya dirancang sebagai Business Assistant DATARA, sehingga fokus saya adalah membantu hal-hal yang berkaitan dengan pengelolaan dan pertumbuhan bisnis UMKM.

---

## 11.14 General Knowledge Boundary

Prinsip:

> Semakin spesifik pertanyaan terhadap bisnis pengguna, semakin besar AI harus bergantung pada Business Context dari backend.

Sedangkan pertanyaan bisnis umum dapat dijawab menggunakan pengetahuan umum.

---

# 12. Notification & Alert Decision Logic

## 12.1 Objective

Notification digunakan untuk memberi tahu user ketika terdapat kondisi bisnis yang membutuhkan perhatian atau tindakan.

Prinsip:

> Tidak semua perubahan data harus menjadi notifikasi.

---

## 12.2 Notification Categories

Untuk MVP:

* Inventory Alert
* Sales Alert
* Profit Alert
* Business Alert

AI tidak menentukan apakah notification dibuat.

---

## 12.3 Inventory Alert

Berasal dari Smart Restock.

### Aman

Tidak menghasilkan notification.

### Perlu Restock

Menghasilkan notification dengan prioritas Warning.

### Prioritas Restock

Menghasilkan notification dengan prioritas Critical.

---

## 12.4 Sales Alert

Jika terjadi penurunan signifikan:

```text
Sales Growth <= -10%
```

sistem dapat membuat warning.

Contoh:

> Penjualan turun 12% dibanding periode sebelumnya.

Peningkatan signifikan dapat ditampilkan sebagai positive insight.

---

## 12.5 Sales Target Alert

Jika user menetapkan target:

```text
Actual Sales
vs
Sales Target
```

Contoh:

```text
Target = 500 unit
Actual = 420 unit

Achievement = 84%
```

DATARA dapat menampilkan:

> Penjualan saat ini baru mencapai 84% dari target periode.

Jika:

```text
Actual >= Target
```

maka:

> Target penjualan periode ini telah tercapai.

---

## 12.6 Profit Alert

Jika:

```text
Profit Growth <= -10%
```

maka dapat dibuat warning.

Jika:

```text
Current Profit <= 0
```

maka:

> Critical

Contoh:

> Bisnis mengalami profit negatif pada periode berjalan. Periksa kembali harga jual, HPP, dan biaya operasional.

---

## 12.7 Margin Alert

Jika:

```text
Current Margin < Target Margin
```

maka sistem dapat memberikan warning.

Contoh:

> Margin rata-rata berada di bawah target yang ditetapkan.

Jika terdapat produk tertentu dengan margin rendah, produk tersebut dapat ditampilkan.

---

## 12.8 Business Health Alert

### Sehat

Tidak perlu alert kritis.

### Perlu Perhatian

Dapat memberikan warning:

> Kondisi bisnis memerlukan perhatian. Beberapa indikator mengalami penurunan.

### Berisiko

Memberikan critical alert:

> Kondisi bisnis saat ini berisiko. Periksa indikator finansial dan operasional yang menjadi penyebab utama.

---

## 12.9 Notification Priority

Tiga tingkat:

| Priority | Meaning                     |
| -------- | --------------------------- |
| Info     | Informasi biasa/positif     |
| Warning  | Membutuhkan perhatian       |
| Critical | Membutuhkan tindakan segera |

---

## 12.10 Notification Frequency

Notification yang sama tidak dibuat berulang-ulang selama kondisi tidak berubah secara signifikan.

Contoh:

```text
Monday:
Kopi Susu → Prioritas Restock

Tuesday:
Kondisi masih sama
→ Tidak membuat notification baru
```

Notification baru dapat dibuat jika kondisi berubah secara signifikan.

---

## 12.11 Notification Lifecycle

Untuk MVP:

```text
UNREAD
  ↓
READ
```

Action dilakukan dengan mengarahkan user ke halaman terkait.

Contoh:

> Stok Kopi Susu berisiko habis.

User memilih:

> Lihat Restock

kemudian diarahkan ke Smart Restock.

---

## 12.12 AI & Notification

AI tidak menentukan notification.

```text
Backend
   ↓
Alert Rule
   ↓
Notification
   ↓
AI Explanation (optional)
```

AI hanya menjelaskan alert yang sudah dihasilkan backend.

---

# 13. Data Validation & Business Data Integrity Rules

## 13.1 Objective

Data Validation memastikan data yang masuk ke DATARA valid dan dapat digunakan oleh sistem analitik.

Alur:

```text
Input Validation
      ↓
Business Validation
      ↓
Data Integrity
      ↓
Calculation / Analysis
```

---

## 13.2 General Data Rules

### BR-DATA-001

Field wajib harus diisi sebelum data disimpan.

### BR-DATA-002

Nilai numerik untuk harga, biaya, stok, jumlah, dan target tidak boleh negatif kecuali secara eksplisit diperbolehkan.

### BR-DATA-003

Harga dan biaya harus menggunakan nilai numerik valid.

### BR-DATA-004

Tanggal transaksi harus valid.

### BR-DATA-005

Data yang digunakan untuk analisis harus berasal dari record valid dan tidak dibatalkan.

### BR-DATA-006

Data yang belum lengkap tidak boleh digunakan sebagai dasar keputusan yang membutuhkan field tersebut.

---

## 13.3 Product Validation

Product Name:

```text
Required
```

Selling Price:

```text
>= 0
```

HPP:

```text
>= 0
```

Unit:

```text
Required
```

Produk yang telah memiliki historical transaction tidak dihapus permanen.

---

## 13.4 HPP Validation

HPP per unit tidak boleh negatif.

Jika komponen HPP tersedia, total HPP harus konsisten.

Operating Expense tidak dimasukkan ke HPP.

Jika HPP belum lengkap:

```text
Smart Pricing
→ Tidak dapat digunakan
```

---

## 13.5 Transaction Validation

Transaction minimal memiliki:

* Transaction Date
* Product
* Quantity
* Selling Price

Quantity:

```text
> 0
```

Selling Price:

```text
>= 0
```

Transaction Date harus valid.

Product harus valid.

Transaksi yang dibatalkan tidak digunakan dalam analisis.

---

## 13.6 Revenue Calculation

```text
Revenue
=
Σ (Quantity × Selling Price)
```

Backend menjadi source of truth.

---

## 13.7 Inventory Validation

```text
Current Stock >= 0
```

DATARA tidak mengizinkan stok negatif dalam MVP.

Jika transaksi melebihi stok:

```text
Validation Error
```

---

## 13.8 Lead Time & Safety Days

Lead Time:

```text
>= 0
```

Safety Days:

```text
>= 0
```

User dapat menggunakan default Safety Days dan mengubahnya sesuai kebutuhan bisnis.

---

## 13.9 Target Validation

Target bisnis:

```text
>= 0
```

Target merupakan nilai yang ditentukan user.

Target berbeda dengan forecast.

```text
Target
=
Desired Outcome

Forecast
=
Expected Outcome
```

---

## 13.10 Pricing Validation

Minimal:

```text
HPP / Unit
Target Margin
Current Selling Price
```

Competitor Price bersifat optional.

Jika tersedia:

```text
Competitor Price >= 0
```

---

## 13.11 Forecasting Data Validation

Forecast membutuhkan historical sales yang cukup.

Untuk MVP, minimal:

```text
>= 14 hari data penjualan
```

Namun jumlah record dan kualitas data juga harus dipertimbangkan.

Jika data tidak memadai:

```text
Forecast Status = INSUFFICIENT
Forecast Value = NULL
```

---

## 13.12 Business Health Validation

Business Health hanya dihitung jika indikator yang dibutuhkan tersedia.

Jika data tidak cukup:

```text
Health Status = INSUFFICIENT_DATA
```

UI dapat menyampaikan:

> Data belum cukup untuk menentukan kondisi bisnis secara menyeluruh.

---

## 13.13 Data Dependency Rules

### Product → HPP → Profitability

```text
Product Data
   ↓
HPP
   ↓
Profitability
   ↓
Business Health
   ↓
Growth Recommendation
```

### Sales → Forecast → Restock

```text
Sales Transaction
   ↓
Sales History
   ↓
Forecast
   ↓
Smart Restock
```

### HPP → Smart Pricing

```text
HPP
+
Selling Price
+
Target Margin
   ↓
Smart Pricing
```

Jika upstream data tidak tersedia, downstream feature harus memberikan:

```text
INSUFFICIENT_DATA
```

bukan menghasilkan nilai palsu.

---

## 13.14 Validation Error Principles

Pesan error kepada user harus menggunakan bahasa bisnis yang mudah dipahami.

Jangan menampilkan error teknis database.

Contoh:

> Stok tidak mencukupi. Stok saat ini 3 unit, sedangkan transaksi membutuhkan 5 unit.

atau:

> HPP produk belum lengkap. Lengkapi biaya bahan baku dan kemasan sebelum menggunakan Smart Pricing.

Backend dapat membedakan:

```text
Technical Error
```

dan:

```text
Business Validation Error
```

---

# 14. Business Rules Summary & Decision Engine Dependency Map

## 14.1 Core Business Flow

```text
USER INPUT
    │
    ├── Produk
    ├── HPP & Biaya
    ├── Transaksi Penjualan
    ├── Stok
    ├── Supplier / Lead Time
    ├── Safety Days
    └── Target Bisnis
          │
          ↓
   DATA VALIDATION
          │
          ↓
   BUSINESS DATABASE
          │
          ↓
   CALCULATION ENGINE
          │
    ┌─────┼────────────┐
    ↓     ↓            ↓
 Pricing Forecast   Profitability
    │     │            │
    └─────┼────────────┘
          ↓
      Inventory
          ↓
   DECISION ENGINE
          │
    ┌─────┼──────────────┐
    ↓     ↓              ↓
 Health Growth Map   Notification
    │     │
    └─────┼──────────────┘
          ↓
       AI / LLM
          ↓
 Insight + Explanation + Advice
```

---

## 14.2 Decision Engine Modules

| Module              | Input                                     | Output                             |
| ------------------- | ----------------------------------------- | ---------------------------------- |
| HPP & Profitability | Cost, HPP, Transaction                    | HPP, Revenue, Profit, Margin       |
| Smart Pricing       | HPP, Margin, Price, External Factor       | Recommended Price                  |
| Sales Forecasting   | Historical Sales                          | Forecast                           |
| Smart Restock       | Forecast, Stock, Lead Time, Safety Days   | Restock Status & Quantity          |
| Business Health     | Revenue, Profit, Margin, Sales, Inventory | Sehat / Perlu Perhatian / Berisiko |
| Growth Map          | Health + Business Metrics                 | Growth Strategy                    |
| Notification        | Decision Results                          | Alert                              |
| AI/LLM              | Structured Context                        | Insight & Advice                   |

---

## 14.3 Dependency Map

### HPP → Pricing & Profitability

```text
Raw Cost
   ↓
HPP / Unit
   ├────────→ Smart Pricing
   │
   └────────→ Profitability
```

### Sales → Forecast → Restock

```text
Sales Transaction
       ↓
Historical Sales
       ↓
Sales Forecast
       ↓
Average Daily Demand
       ↓
Smart Restock
       ↓
Restock Status
       ↓
Recommended Quantity
```

### Business Metrics → Health

```text
Revenue
Profit
Margin
Sales
Inventory
   │
   ↓
Business Health
   │
   ├── Sehat
   ├── Perlu Perhatian
   └── Berisiko
```

### Health + Problem → Growth Strategy

```text
Business Health
      +
Primary Business Problem
      ↓
Growth Strategy
      ↓
┌──────────────────────┐
│ Increase Sales       │
│ Improve Profitability│
│ Optimize Inventory   │
│ Scale Business       │
└──────────────────────┘
```

### Decision → AI

```text
Decision Engine
      ↓
Structured Business Context
      ↓
AI / LLM
      ↓
Explanation
+
Insight
+
Actionable Advice
```

---

# 15. Source of Truth

Setiap informasi memiliki source of truth yang jelas.

| Information             | Source of Truth        |
| ----------------------- | ---------------------- |
| Product Data            | Database               |
| Transaction             | Database               |
| HPP                     | Backend Calculation    |
| Revenue                 | Backend Calculation    |
| Profit                  | Backend Calculation    |
| Margin                  | Backend Calculation    |
| Recommended Price       | Smart Pricing Engine   |
| Forecast                | Forecasting Engine     |
| Restock Status          | Restock Engine         |
| Business Health         | Health Decision Engine |
| Growth Strategy         | Growth Decision Engine |
| Notification Priority   | Notification Engine    |
| Explanation / Narrative | AI/LLM                 |

Prinsip utama:

> **AI bukan Source of Truth untuk angka maupun keputusan bisnis.**

---

# 16. Business Rule Priority

Jika terdapat konflik antarhasil analisis, kondisi dengan risiko lebih tinggi harus diprioritaskan.

Contoh:

```text
Sales Growth = +15%
Revenue Growth = +10%
Profit = Negative
```

Business Health tetap:

```text
BERISIKO
```

karena profit negatif memiliki prioritas lebih tinggi.

Contoh lain:

```text
Stock = 10
Lead Time = 3 hari
Stock Coverage = 2 hari
```

maka:

```text
PRIORITAS RESTOCK
```

meskipun indikator bisnis lainnya sehat.

---

# 17. Golden Rules for Backend Development

Aturan berikut menjadi prinsip utama implementasi backend DATARA.

## Rule 1

**Backend adalah sumber kebenaran untuk seluruh perhitungan bisnis.**

## Rule 2

**AI tidak menghitung ulang data bisnis.**

## Rule 3

**AI tidak menentukan Business Health atau Growth Strategy.**

## Rule 4

**Data yang tidak cukup menghasilkan `INSUFFICIENT_DATA`, bukan angka hasil tebakan.**

## Rule 5

**Setiap rekomendasi harus dapat ditelusuri kembali ke data dan business rule yang mendasarinya.**

## Rule 6

**User input tetap menjadi faktor utama untuk parameter yang bersifat subjektif**, seperti:

* Target Margin
* Safety Days
* Target Penjualan
* Target Profit
* Parameter bisnis lainnya

## Rule 7

**Faktor eksternal seperti harga kompetitor merupakan faktor pendukung, bukan satu-satunya dasar keputusan.**

## Rule 8

**Rekomendasi harus tetap realistis dan mempertimbangkan profitabilitas.**

## Rule 9

**Modul downstream tidak boleh menghasilkan keputusan jika data upstream yang dibutuhkan belum tersedia.**

## Rule 10

**Historical data tidak boleh dihapus secara sembarangan jika masih digunakan oleh analisis bisnis.**

---

# 18. Overall Decision Chain

Keseluruhan rantai keputusan DATARA:

```text
                    USER DATA
                        ↓
                DATA VALIDATION
                        ↓
               BUSINESS DATABASE
                        ↓
              CALCULATION ENGINE
                        ↓
       ┌────────────────┼─────────────────┐
       ↓                ↓                 ↓
   PROFITABILITY     FORECASTING      INVENTORY
       │                │                 │
       ↓                ↓                 ↓
SMART PRICING      SALES FORECAST    SMART RESTOCK
       │                │                 │
       └────────────────┼─────────────────┘
                        ↓
                BUSINESS METRICS
                        ↓
                BUSINESS HEALTH
                        ↓
                  GROWTH MAP
                        ↓
                  RECOMMENDATION
                        ↓
                  NOTIFICATION
                        ↓
                    AI / LLM
                        ↓
             USER-FACING INSIGHT
```

---

# 19. Final Architecture Principle

DATARA menerapkan prinsip:

```text
                    USER
                     │
                     ↓
                FRONTEND
                     │
                     ↓
                   API
                     │
                     ↓
                BACKEND
                     │
          ┌──────────┼───────────┐
          ↓          ↓           ↓
       Database   Rule Engine   ML/Forecast
          │          │           │
          └──────────┼───────────┘
                     ↓
                Decision Engine
                     │
          ┌──────────┼───────────┐
          ↓          ↓           ↓
        Health    Growth       Alert
                     │
                     ↓
                AI / LLM Layer
                     │
                     ↓
               User Insight
```

Prinsip akhirnya:

> **DATARA menggunakan data dan rule-based decision engine sebagai fondasi keputusan, machine learning/forecasting untuk prediksi, dan AI/LLM sebagai lapisan komunikasi serta advisory.**

Dengan demikian, sistem tetap:

* Data-driven
* Explainable
* Traceable
* Realistic
* Terukur
* Tidak bergantung pada keputusan AI generatif semata

---

# 20. Document Status

**Business Rules & Decision Logic**

```text
Status  : FINAL
Version : 1.0
```

Dokumen ini menjadi dasar untuk dokumen teknis berikutnya:

```text
Business Rules
      ↓
Data Dictionary & Data Model
      ↓
System Architecture & Technical Specification
      ↓
API Contract
      ↓
AI / ML Specification
      ↓
UI/UX Specification
      ↓
Agent Context / AI Development Guidelines
```

Setiap dokumen berikutnya harus mengikuti business rules yang telah ditetapkan dalam dokumen ini.
