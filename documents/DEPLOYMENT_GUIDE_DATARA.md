# Panduan Deployment DATARA (Vercel + Render + TiDB Cloud)

> **Versi:** 1.0
> **Tanggal:** 2026-08-14
> **Status:** Final

Panduan langkah demi langkah untuk men-deploy DATARA secara **gratis ($0)** dan **tanpa kartu kredit**, dengan arsitektur:

```text
Frontend Next.js (Vercel — free)
        |
        | HTTPS (REST API)
        v
Backend FastAPI (Render — free)
        |
        | MySQL-compatible (TLS)
        v
Database TiDB Cloud Starter (free)
```

---

## 1. Ringkasan Biaya & Platform

| Platform | Komponen | Biaya | Batasan penting |
|---|---|---|---|
| **Vercel** (Hobby) | Frontend Next.js | **$0 — free forever** | 100 GB bandwidth/bln, ±100K–1M function invocations, non-komersial (cocok untuk kompetisi) |
| **Render** (free) | Backend FastAPI | **$0 — free forever** | 512 MB RAM, 0.1 CPU, tidur setelah 15 menit idle (cold start 30–60 detik), 750 jam/bln |
| **TiDB Cloud Starter** | Database MySQL-compatible | **$0 — free forever** | 25 GiB storage + 250 M Request Units/bln per organisasi; kuota reset tiap bulan (throttle, bukan tagihan) |

Poin penting:

- **Tidak ada kartu kredit** yang diminta di ketiga platform.
- Yang kedaluwarsa 30 hari hanya PostgreSQL/Redis bawaan Render — **tidak digunakan** pada arsitektur ini.
- Jika kuota TiDB habis, koneksi baru ditolak/di-throttle sampai bulan berikutnya; **tidak ada tagihan** tanpa kartu kredit.
- Fitur AI Assistant butuh `GEMINI_API_KEY` dari Google AI Studio (free tier Google, terpisah dari hosting). Tanpa key, chat AI menampilkan pesan fallback "belum aktif" — aplikasi tetap berjalan normal.

---

## 2. Prasyarat

- Repo GitHub yang berisi seluruh project (root `frontend/`, `backend/`, `documents/`) sudah di-push.
- Akun: [TiDB Cloud](https://tidbcloud.com), [Render](https://render.com) (login via GitHub), [Vercel](https://vercel.com) (login via GitHub).
- Generator secret acak (mis. `openssl rand -hex 32`) untuk `JWT_SECRET` (minimal 32 karakter).
- (Opsional) `GEMINI_API_KEY` dari [Google AI Studio](https://aistudio.google.com) dan `GOOGLE_CLIENT_ID` dari Google Cloud Console.

Catatan: `backend/render.yaml` dan `vercel.json` (di root repo) sudah tersedia di repository — Render dan Vercel akan mendeteksinya otomatis sehingga sebagian besar konfigurasi tidak perlu diketik manual.

---

## 3. Langkah 1 — Database: TiDB Cloud Starter

1. Login ke [TiDB Cloud](https://tidbcloud.com) → **Create Cluster** (atau **Start for Free**).
2. Pilih **TiDB Cloud Starter** → beri nama cluster (mis. `datara`) → pilih region terdekat dengan pengguna demo (mis. **Singapore**) → **Create**.
   - Catat **Username** (format `<prefix>.root`), **Password**, **Host** (mis. `gateway01.ap-southeast-1.prod.aws.tidbcloud.com`), dan **Port `4000`**.
3. Buat database: buka tab **SQL Editor** (Chat2Query) di konsol, jalankan:
   ```sql
   CREATE DATABASE IF NOT EXISTS datara;
   ```
4. Unduh **CA certificate** dari dialog **Connect** (tombol "Generate CA certificate") → simpan sebagai `backend/tidb-ca.pem` di repo (file ini publik, bukan rahasia) → commit + push.
   - Alternatif tanpa file CA: gunakan param `ssl_verify_cert=false&ssl_verify_identity=false` pada URL (TLS tetap aktif, hanya saja CA tidak diverifikasi) — lihat Langkah 2.
5. **Tes koneksi lokal** sebelum deploy (dari folder `backend/`, pastikan `.env` diisi sementara atau gunakan variabel env langsung):
   ```powershell
   $env:DATABASE_URL="mysql://221q6c1RP7kNmFU.root:<PASSWORD>@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/datara"; alembic upgrade head
   ```
   Jika migrasi berjalan tanpa error, koneksi & CA sudah benar.

---

## 4. Langkah 2 — Backend: Render

1. Login ke [Render Dashboard](https://dashboard.render.com) → **New +** → **Blueprint**.
   - Pilih repo GitHub project ini → Render membaca `backend/render.yaml` dan membuat service `datara-api` secara otomatis (Root Directory = `backend`, start command = `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`, health check = `/api/health`).
   - Alternatif manual: **New + → Web Service** → pilih repo → **Root Directory: `backend`** → Environment: `Python` → Build Command: `pip install -r requirements.txt` → Start Command seperti di atas → Instance Type: **Free**.
2. Isi **Environment Variables** (`⚠️ sync: false` artinya wajib diisi manual):
   | Key | Contoh nilai | Keterangan |
   |---|---|---|
   | `DATABASE_URL` | `mysql+pymysql://<prefix>.root:<pw>@<host>:4000/datara?ssl_ca=/opt/render/project/src/backend/tidb-ca.pem` | Path absolut CA di container Render. Tanpa file CA: `...?ssl_ca=` dihapus dan tambahkan `&ssl_verify_cert=false&ssl_verify_identity=false` |
   | `CORS_ORIGINS` | `https://<frontend>.vercel.app,http://localhost:3000` | Origin yang boleh memanggil API |
   | `JWT_SECRET` | string acak min. 32 karakter | Dipakai menandatangani token login |
   | `GEMINI_API_KEY` | *(opsional)* | Untuk fitur AI Business Assistant |
   | `GOOGLE_CLIENT_ID` | *(opsional)* | Untuk login Google (endpoint `/auth/google`) |
3. Klik **Apply / Deploy**. Tunggu build selesai (±3–5 menit).
4. **Generate Domain** (jika belum ada, mis. `https://datara-api.onrender.com`), lalu buka:
   ```
   https://datara-api.onrender.com/api/health
   ```
   Hasil yang benar: `{"status": "ok", ...}`.
5. Verifikasi juga database aktif: jalankan migrasi otomatis tidak error di log deploy (start command menjalankan `alembic upgrade head` di setiap start — aman diulang).

Catatan: free tier Render akan *tidur* setelah 15 menit idle dan membutuhkan 30–60 detik saat pertama diakses lagi. Ini normal dan gratis.

---

## 5. Langkah 3 — Frontend: Vercel

1. Login ke [Vercel](https://vercel.com) → **Add New → Project** → **Import** repo GitHub ini.
2. Vercel otomatis membaca `vercel.json`: **Root Directory = `frontend`**, build command `npm run build`, install command `npm install`.
3. Tambahkan **Environment Variable** di tab Settings proyek (kategori Environments / General):
   ```
   NEXT_PUBLIC_API_URL=https://datara-api.onrender.com/api/v1
   ```
   - Perhatikan suffix `/api/v1` — wajib ada (frontend memanggil path relatif ke base ini).
   - Setelah menambah variable, **redeploy** agar ter-pick-up.
4. Klik **Deploy** → tunggu build selesai → buka domain `https://<project>.vercel.app`.

---

## 6. Langkah 4 — Google Sign-In (opsional)

Jika `GOOGLE_CLIENT_ID` diisi dan login Google dipakai:

1. Google Cloud Console → **APIs & Services → Credentials** → edit OAuth 2.0 Client (type: Web application).
2. Tambahkan ke **Authorized JavaScript origins**:
   ```
   https://<project>.vercel.app
   http://localhost:3000
   ```

---

## 7. Langkah 5 — Verifikasi End-to-End

Checklist setelah semua deploy:

- [ ] `https://datara-api.onrender.com/api/health` → `{"status": "ok", ...}`.
- [ ] `https://datara-api.onrender.com/docs` (Swagger UI) terbuka.
- [ ] Buka frontend → **Register** akun baru → **Login** berhasil (token tersimpan).
- [ ] Tambah **produk + HPP**, catat **transaksi**, cek dashboard & laporan menampilkan angka.
- [ ] Smart Pricing / Smart Restock / Forecasting menghasilkan rekomendasi.
- [ ] **AI Business Assistant** menjawab dengan data (mis. "berapa stok produk X?") — bukan pesan fallback.
- [ ] (Jika diaktifkan) Google Sign-In berhasil.
- [ ] Tidak ada error CORS di DevTools (frontend memanggil `https://datara-api.onrender.com`).

---

## 8. Pemeliharaan & Batasan

| Hal | Kondisi | Tindakan |
|---|---|---|
| **Cold start Render** | Service tidur setelah idle 15 menit | Terima (30–60 detik pertama setelah idle) atau pikat `/api/health` tiap 10 menit via monitoring gratis (UptimeRobot). Pastikan jam berjalan di bawah 750 jam/bln. |
| **Kuota RU TiDB** | Reset tiap bulan; habis = throttled sampai bulan berikutnya | Pantau usage di dashboard TiDB; trafik demo normal berada jauh di bawah kuota. |
| **Bandwidth Vercel** | 100 GB/bln | Cukup jauh untuk trafik demo; jika hampir habis, cek "Usage" di dashboard Vercel. |
| **Update kode** | Push ke branch → auto-deploy (Render & Vercel) | Cabang `main` dianggap produksi. |
| **DB tidak kedaluwarsa** | TiDB Starter free forever | Tidak perlu membuat ulang database. |
| **Nonaktif total** | Tidak dipakai sementara | Hapus service di Render (data di TiDB tetap aman); deploy ulang kapan saja lewat Blueprint. Frontend Vercel bisa "Pause" tanpa biaya. |

---

## 9. Troubleshooting

| Masalah | Kemungkinan penyebab | Solusi |
|---|---|---|
| `ora-... / 1045 Access denied` saat migrasi | Kredensial salah; host/port salah | Periksa user `<prefix>.root`, port `4000`, password benar; tes via GUI TiDB "Connect". |
| `SSL connection error: unable to get local issuer certificate` | CA tidak diverifikasi atau path salah | Pakai path absolut `/opt/render/project/src/backend/tidb-ca.pem`, atau tambah `&ssl_verify_cert=false&ssl_verify_identity=false`. |
| `ModuleNotFoundError` saat build Render | Requirements tidak ter-install | Pastikan Build Command `pip install -r requirements.txt` dan Root Directory `backend`. |
| Migrasi gagal di start command | `DATABASE_URL` kosong/tidak valid | Cek env var di tab Settings Render; start command menjalankan `alembic upgrade head` setiap start. |
| CORS error di browser | `CORS_ORIGINS` tidak memuat domain frontend | Set ke `https://<project>.vercel.app,http://localhost:3000`, redeploy backend. |
| Frontend memanggil `localhost:8000` | `NEXT_PUBLIC_API_URL` tidak terset di Vercel | Set var + redeploy. Periksa juga tidak ada fallback default yang tersisa di build. |
| Cold start terlalu lama saat demo | Free tier tidur 15 menit idle | Ping `/api/health` tiap 10 menit sebelum/saat demo (mis. via UptimeRobot). |
| Login Google error `redirect_uri_mismatch` | Origin tidak terdaftar di Google Console | Tambah `https://<project>.vercel.app` ke Authorized JavaScript origins (Langkah 4). |
| AI chat menjawab fallback "belum aktif" | `GEMINI_API_KEY` kosong | Isi key di Render → redeploy. |

---

## 10. Referensi

- `backend/render.yaml` — Blueprint Render (service, root dir, start command, env vars).
- `vercel.json` (root repo) — konfigurasi Vercel (root dir frontend, build/install command).
- `frontend/src/lib/api.ts` — base URL API (dari `NEXT_PUBLIC_API_URL`, default `http://localhost:8000/api/v1`).
- `backend/app/core/config.py` — variabel env yang dibaca backend (`DATABASE_URL`, `CORS_ORIGINS`, `JWT_SECRET`, `GEMINI_API_KEY`, `GOOGLE_CLIENT_ID`).
- `backend/alembic/env.py` — migrasi memakai `DATABASE_URL` dari environment.