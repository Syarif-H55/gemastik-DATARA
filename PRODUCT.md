# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Pemilik UMKM Food & Beverage skala mikro di Indonesia (satu actor, tidak ada peran Staff/Owner terpisah). Pengguna mencatat transaksi harian di gerai/kios miliknya sendiri, bekerja dengan HP atau laptop, dan membutuhkan keputusan bisnis (harga, stok, kelayakan produk) tanpa latar belakang akuntansi atau analitik.

## Product Purpose

DATARA (Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM) adalah Decision Support System yang mengubah data sederhana — penjualan, HPP (rincian biaya produk), biaya operasional, dan stok — menjadi indikator bisnis serta rekomendasi terjelaskan (profitability, smart pricing, smart restock, forecasting, business health, growth map, decision monitoring). Keberhasilan = pemilik memahami kondisi bisnisnya dan mengambil keputusan yang lebih baik (menaikkan harga, menambah stok, mengevaluasi produk).

## Positioning

Kalkulasi bisnis (HPP, margin, revenue, COGS, rekomendasi) seluruhnya dihitung backend sebagai source of truth; LLM/AI hanya menjelaskan hasil dan tidak pernah mengarang angka, mengubah harga, atau menyentuh database. User tetap pengambil keputusan akhir (recommendation → review → apply/ignore).

## Operating Context

- Aplikasi web desktop-first dengan shell sidebar; seluruh UI berbahasa Indonesia (kecuali nama modul seperti Business Dashboard, Product Profitability, Sales Forecasting, Smart Pricing, Smart Restock — bahasa Inggris sesuai dokumen PRD).
- Alur kerja utama: catat transaksi harian (POS sederhana) → stok berkurang otomatis → dashboard/profitability/forecasting/pricing/restock membaca data aktual → user meninjau rekomendasi → apply atau abaikan → keputusan dimonitor.
- Produk (menu) memiliki rincian HPP per unit yang diisi/diubah user (mis. cup, teh, gula), sumber perhitungan margin & harga.
- Kompetisi nasional Gemastik; proyek monorepo frontend/backend dengan dokumen spesifikasi di `documents/`.

## Capabilities and Constraints

- Modul: Dashboard, Catat Transaksi (CRUD produk + rincian HPP), Product Profitability (drill-down HPP), Smart Pricing, Smart Restock, Sales Forecasting, Keputusan & Monitoring, Roadmap Pertumbuhan, AI Business Assistant, auth (email/password + Google).
- Backend FastAPI + MySQL adalah source of truth; frontend Next.js hanya menampilkan.
- Tanpa data palsu: semua metrik dari transaksi aktual; forecasting dengan data terbatas memakai Simple Estimate + low confidence.
- UI harus tetap fungsional dengan jumlah produk dan transaksi UMKM nyata (bukan data demo).

## Brand Commitments

Nama produk DATARA (singkatan resmi). Tidak ada aset visual (logo, warna, tipografi) yang sudah terikat — identitas visual bebas ditentukan. Bahasa UI: Indonesia; nama modul utama tetap Inggris sesuai dokumen PRD.

## Evidence on Hand

- Dokumen spesifikasi lengkap di `documents/` (PRD v1.2, Data Dictionary, Business Rules & Decision Logic, API Contract, AI/ML Spec, UI/UX Spec, System Architecture).
- Frontend Next.js berjalan dengan shell sidebar shadcn, 11 halaman, semua terhubung API nyata.
- Backend FastAPI berjalan dengan seed data demo (8 produk F&B Indonesia: es teh manis, es jeruk, kopi susu gula aren, ayam geprek, nasi goreng, kentang goreng, pisang goreng keju, air mineral).
- Tanpa testimonial, press, atau aset pemasaran resmi; jangan membuat klaim komersial palsu.

## Product Principles

1. Kejelasan data di atas dekorasi: angka & rekomendasi selalu bisa ditelusuri ke sumbernya.
2. Backend adalah kebenaran; frontend tidak pernah menghitung ulang otoritatif.
3. Rekomendasi tidak pernah memaksa: user meninjau, menyetujui, atau mengabaikan.
4. Kesederhanaan untuk pemilik mikro: istilah bisnis Indonesia yang familiar, tanpa jargon akuntansi.
5. Pengalaman bekerja di kedua tema (light/dark) dan perangkat layar sempit tanpa kehilangan fungsi.

## Accessibility & Inclusion

Pemilik UMKM dengan perangkat beragam; kontras WCAG AA untuk teks, ukuran teks cukup besar untuk layar kecil, fokus keyboard terlihat. (Belum ada standar aksesibilitas khusus yang ditetapkan.)
