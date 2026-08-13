# Akun Demo DATARA

Akun demo dibuat dengan script `backend/scripts/seed_demo_2users.py`. Data bertujuan untuk pengujian frontend, dengan satu akun "veteran" (sudah memakai aplikasi ±6 bulan) dan satu akun "pemula" (baru ±1 bulan).

## Ringkasan Akun

| | Akun Veteran | Akun Pemula |
|---|---|---|
| Email | `dummy.lama@umkm.id` | `dummy.baru@umkm.id` |
| Password | `demo123456` | `demo123456` |
| Nama | Dewi Anggraini | Sari Wulandari |
| Bisnis | Kopi Nusantara | Warung Makan Bu Sari |
| Lama pemakaian | ±6 bulan (180 hari data) | ±1 bulan (30 hari data) |
| Jumlah produk | 7 | 6 |
| Total transaksi | ±1.260 | ±170 |

## Detail Per Akun

### 1. Kopi Nusantara (veteran)

- Pemilik: Dewi Anggraini (`dummy.lama@umkm.id` / `demo123456`)
- Jenis: food & beverage (kedai kopi)
- Produk: Espresso, Kopi Susu Gula Aren, Kopi Tubruk, Es Teh Manis, Matcha Latte, Kentang Goreng, Roti Bakar Cokelat
- Karakteristik data: omzet tumbuh stabil dari ±9,6 juta/bulan menjadi ±45 juta/bulan, pola weekend lebih ramai, margin kotor ±67%, status kesehatan cenderung **SEHAT**.

### 2. Warung Makan Bu Sari (pemula)

- Pemilik: Sari Wulandari (`dummy.baru@umkm.id` / `demo123456`)
- Jenis: food & beverage (warung makan)
- Produk: Nasi Ayam Geprek, Nasi Goreng Ayam, Mie Goreng, Es Teh Manis, Es Jeruk, Kerupuk & Lalapan
- Karakteristik data: volume kecil dan masih fluktuatif (awal periode ada hari tidak tercatat), margin kotor ±54%, status kesehatan cenderung **PERLU PERHATIAN**.

## Cara Seed Ulang

```bash
python -m scripts.seed_demo_2users --password demo123456
```

Catatan: script melewati akun yang emailnya sudah ada. Untuk seed ulang dengan data baru, hapus user-nya dari database terlebih dahulu.

Script membuat: produk + HPP per komponen, inventori + riwayat movement (RESTOCK/SALE), transaksi harian (+6/1 bulan), biaya operasional bulanan, business target bulanan (COMPLETED/ACTIVE), dan konfigurasi bisnis.