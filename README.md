# DATARA

**Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM**

Decision Support System (DSS) untuk membantu pemilik UMKM *food & beverage* skala mikro mengambil keputusan bisnis berdasarkan data — bukan perkiraan.

| | |
|---|---|
| **Versi** | v1.2 (9 Agustus 2026) |
| **Team** | Pisang — Agil Kurniawan, Syarif Hidayatullah, Raifa Aziz F. P. H. |
| **Stakeholder** | UMKM |
| **Status** | Pengembangan aktif |

---

## Latar Belakang

Usaha mikro di sektor makanan dan minuman menghasilkan data transaksi dan biaya operasional setiap hari. Namun, sebagian besar pemilik masih menentukan harga, mengelola stok, dan mengevaluasi kinerja produk berdasarkan **perkiraan atau pengalaman**. Keterbatasan pemahaman terhadap HPP, margin keuntungan, dan pola penjualan membuat data yang sebenarnya tersedia belum dimanfaatkan secara optimal.

Akibatnya, pemilik rentan mengalami:

- **Kesalahan penetapan harga** — harga jual tidak mencerminkan HPP dan target margin.
- **Risiko stok tidak optimal** — kelebihan atau kekurangan persediaan karena tidak ada dasar kebutuhan yang jelas.
- **Keputusan bisnis kurang tepat** — evaluasi produk dan arah usaha tidak berbasis data, sehingga berpotensi menurunkan profitabilitas.

### Problem Statement

> Pemilik usaha mikro makanan dan minuman tidak dapat mengambil keputusan bisnis secara optimal karena belum mampu mengolah data penjualan, HPP, biaya, stok, dan profitabilitas menjadi informasi yang dapat digunakan, sehingga penetapan harga, pengelolaan persediaan, dan evaluasi kinerja produk masih banyak bergantung pada perkiraan dan berisiko menurunkan keuntungan usaha.

### Siapa yang Terdampak

- **Pemilik UMKM makanan dan minuman skala mikro** — pengguna utama yang kesulitan mengubah data harian menjadi keputusan bisnis.
- **Karyawan / pengelola operasional** — aktivitas pencatatan transaksi dan stok jadi kurang terarah tanpa kondisi persediaan yang jelas.
- **Usaha itu sendiri** — keputusan berbasis perkiraan menghambat profitabilitas dan pertumbuhan.

---

## Solusi

DATARA mengubah siklus **Data → Analisis → Keputusan → Rekomendasi → Insight** menjadi alur yang terukur:

1. **Input data bisnis** — transaksi penjualan, produk & HPP, stok, biaya operasional, target.
2. **Analisis** — perhitungan HPP, revenue, COGS, gross/net profit, margin, sales forecasting, klasifikasi produk.
3. **Rekomendasi** — Smart Pricing, Smart Restock, Business Health, Growth Map.
4. **Keputusan & monitoring** — pencatatan keputusan yang diterapkan beserta perkembangan indikator bisnis.
5. **Business Assistant (AI/LLM)** — menjelaskan hasil analisis dan rekomendasi dalam bahasa yang mudah dipahami.

### Fitur Utama

- **Business Dashboard** — omzet, laba, HPP, margin, tren penjualan, dan kondisi kesehatan bisnis.
- **Analisis Profitabilitas Produk** — pendapatan, HPP, laba, dan margin per produk.
- **Smart Pricing** — rekomendasi harga jual berbasis HPP dan target margin.
- **Sales Forecasting** — prediksi penjualan sebagai dasar pengelolaan persediaan.
- **Smart Restock** — rekomendasi waktu dan jumlah restock berdasarkan forecast, stok, lead time, dan safety days.
- **Business Health** — penilaian kondisi bisnis (Sehat / Perlu Perhatian / Berisiko).
- **Growth Map** — arah pertumbuhan bisnis berdasarkan kondisi dan performa.
- **Riwayat Keputusan** — monitoring dampak keputusan yang telah diterapkan.
- **AI Business Assistant** — penjelasan insight dan rekomendasi (non source-of-truth).

---

## Arsitektur

Monorepo dengan arsitektur **decoupled** (frontend & backend terpisah):

```
gemastik-
├── documents/        # Spesifikasi: PRD, Data Dictionary, Business Rules, catatan teknis
├── frontend/         # Next.js 16 (App Router) + React 19 + Tailwind CSS v4 + shadcn/ui
└── backend/          # FastAPI + SQLAlchemy + Alembic + MySQL (sedang dikembangkan)
```

- **Frontend** mengonsumsi REST API dari backend melalui `frontend/src/lib/api.ts` (`NEXT_PUBLIC_API_URL`, default `http://localhost:8000/api`).
- **Backend** menyediakan REST API, validation, decision engine (HPP, pricing, restock, health, growth), forecasting pipeline, dan context builder untuk AI.
- **Prinsip**: backend/decision engine menghasilkan angka dan keputusan berbasis data, rule, atau model; AI/LLM hanya menjelaskan hasil — AI **bukan** source of truth untuk angka bisnis.

## Struktur Dokumen

| Dokumen | Isi |
|---|---|
| `documents/PRD DATARA.docx.md` | Spesifikasi produk (problem, objectives, scope, FR) |
| `documents/DATA_DICTIONARY_AND_DATA_MODEL_DATARA.md` | Skema database & data model (FINAL) |
| `documents/bussiness-rule-dan-decision-logic.md` | Aturan bisnis & logika pengambilan keputusan (FINAL) |
| `documents/laporan-frontend-DATARA.md` | Laporan implementasi frontend |
| `documents/catatan-inkonsistensi-frontend-DATARA.md` | Catatan inkonsistensi kontrak frontend vs dokumen |

---

## Menjalankan

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
# siapkan database MySQL `datara`, sesuaikan kredensial di backend/.env
alembic upgrade head
uvicorn app.main:app --reload
```

---

## Status Pengembangan

- [x] Frontend demo (mock data) — dapat dijalankan
- [x] Skema database MySQL (Alembic migration awal)
- [ ] Backend FastAPI (API endpoints)
- [ ] Decision engine & forecasting pipeline
- [ ] Integrasi frontend ↔ backend
- [ ] Autentikasi nyata
