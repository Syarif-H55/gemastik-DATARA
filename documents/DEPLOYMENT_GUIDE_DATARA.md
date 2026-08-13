# Panduan Deployment DATARA (Vercel + Vercel + TiDB Cloud)

> **Versi:** 2.0
> **Tanggal:** 2026-08-14
> **Status:** Final

Panduan langkah demi langkah untuk men-deploy DATARA secara **gratis ($0)** dan **tanpa kartu kredit** — seluruh aplikasi (frontend + backend) berjalan di Vercel sebagai dua project terpisah dari satu repo, dengan arsitektur:

```text
Frontend Next.js  (Vercel — project #1, free)
        |
        | HTTPS (REST API)
        v
Backend FastAPI (Vercel — project #2, Python runtime, free)
        |
        | MySQL-compatible (TLS)
        v
Database TiDB Cloud Starter (free)
```

> Riwayat keputusan: backend awalnya direncanakan di Render, tetapi Render mewajibkan verifikasi kartu kredit saat membuat service meski free tier (tanpa kartu, service tidak bisa dibuat). Karena itu backend dipindah ke Vercel — platform yang sama dengan frontend — yang tidak meminta kartu sama sekali.

---

## 1. Ringkasan Biaya & Platform

| Platform | Komponen | Biaya | Batasan penting |
|---|---|---|---|
| **Vercel** (Hobby) | Frontend Next.js (`frontend/`) | **$0 — free forever** | 100 GB bandwidth/bln, ±100K function invocations, non-komersial (cocok untuk kompetisi) |
| **Vercel** (Hobby) | Backend FastAPI (`backend/`, Python runtime) | **$0 — free forever** | Satu Vercel Function; max `maxDuration` 60 detik (diatur `backend/vercel.json`); masuk kuota invocations & CPU-hours yang sama |
| **TiDB Cloud Starter** | Database MySQL-compatible | **$0 — free forever** | 25 GiB storage + 250 M Request Units/bln per organisasi; kuota reset tiap bulan (throttle, bukan tagihan) |

Poin penting:

- **Tidak ada kartu kredit di mana pun** — Vercel Hobby dan TiDB Starter eksplisit tidak memintanya.
- Serverless Vercel "scale-to-zero": tidak ada tagihan saat idle, cold start singkat (±50–150 ms) — lebih baik dari free tier Render.
- Fungsi AI Assistant berlari di dalam function; jawaban Gemini yang lambat (>60 detik) bisa timeout — untuk demo biasanya aman (jawaban <30 detik).
- Jika kuota TiDB habis, koneksi baru ditolak/di-throttle sampai bulan berikutnya; **tidak ada tagihan** tanpa kartu kredit.
- Fitur AI Assistant butuh `GEMINI_API_KEY` dari Google AI Studio (free tier Google, terpisah dari hosting). Tanpa key, chat AI menampilkan pesan fallback "belum aktif" — aplikasi tetap berjalan normal.

---

## 2. Prasyarat

- Repo GitHub yang berisi seluruh project (root `frontend/`, `backend/`, `documents/`) sudah di-push.
- Akun: [TiDB Cloud](https://tidbcloud.com) dan [Vercel](https://vercel.com) (login via GitHub).
- Generator secret acak (mis. `openssl rand -hex 32`) untuk `JWT_SECRET` (minimal 32 karakter).
- (Opsional) `GEMINI_API_KEY` dari [Google AI Studio](https://aistudio.google.com) dan `GOOGLE_CLIENT_ID` dari Google Cloud Console.
- ⚠️ **Jangan commit kredensial asli** (password DB, `JWT_SECRET`, `GEMINI_API_KEY`) ke repo — pakai placeholder, isi aslinya hanya di dashboard Vercel.

Catatan: file konfigurasi sudah tersedia di repo — `frontend/vercel.json` (framework Next.js) dan `backend/vercel.json` (max duration fungsi). Setiap deploy cukup: import repo dua kali sebagai dua project dengan Root Directory berbeda.

---

## 3. Langkah 1 — Database: TiDB Cloud Starter

1. Login ke [TiDB Cloud](https://tidbcloud.com) → **Create Cluster** (atau **Start for Free**).
2. Pilih **TiDB Cloud Starter** → beri nama cluster (mis. `datara`) → pilih region terdekat dengan pengguna demo (mis. **Singapore**) → **Create**.
   - Catat **Username** (format `<prefix>.root`), **Password**, **Host** (mis. `gateway01.ap-southeast-1.prod.aws.tidbcloud.com`), dan **Port `4000`**.
3. Buat database: buka tab **SQL Editor** (Chat2Query) di konsol, jalankan:
   ```sql
   CREATE DATABASE IF NOT EXISTS datara;
   ```
4. **TLS**: TiDB Starter hanya menerima koneksi TLS; sertifikatnya diterbitkan Let's Encrypt.
   - **Opsi A (utama, tanpa file CA)**: pakai param `ssl_disabled=false&ssl_verify_cert=false&ssl_verify_identity=false` — TLS tetap aktif, chain sertifikat tidak diverifikasi. Paling simpel untuk Vercel (tidak bergantung lokasi file).
   - **Opsi B (bila Opsi A gagal)**: unduh ISRG Root X1 dari `https://letsencrypt.org/certs/isrgrootx1.pem`, simpan sebagai `backend/tidb-ca.pem` (file publik, aman di-commit), lalu URL memakai `?ssl_ca=tidb-ca.pem`.
5. **Tes koneksi lokal sebelum deploy** (jalankan dari folder `backend/` — penting, `alembic.ini` berada di sana; ganti `<PASSWORD>` dengan password asli):
   ```powershell
   $env:DATABASE_URL="mysql+pymysql://<prefix>.root:<PASSWORD>@<host>:4000/datara?ssl_disabled=false&ssl_verify_cert=false&ssl_verify_identity=false"; alembic upgrade head
   ```
   - Perhatikan scheme wajib **`mysql+pymysql://`** (bukan `mysql://`).
   - Jika error TLS, ulangi dengan Opsi B:
     ```powershell
     $env:DATABASE_URL="mysql+pymysql://<prefix>.root:<PASSWORD>@<host>:4000/datara?ssl_ca=tidb-ca.pem"; alembic upgrade head
     ```
   - Jika migrasi selesai tanpa error, koneksi & TLS sudah benar.

---

## 4. Langkah 2 — Backend: Vercel (project #2)

1. Login ke [Vercel](https://vercel.com) → **Add New → Project** → **Import** repo GitHub yang sama (yang sudah dipakai untuk frontend).
2. **Root Directory: `backend`** (klik **Edit** pada setting Root Directory sebelum deploy).
3. Framework `FastAPI` terdeteksi otomatis (Python runtime; entrypoint `app/main.py` sudah didukung secara resmi).
4. **Build Command**: `alembic upgrade head` (menjalankan migrasi database saat build, sebelum aplikasi live — aman diulang tiap deploy).
5. Tambahkan **Environment Variables** di settings project:
   | Key | Contoh nilai | Keterangan |
   |---|---|---|
   | `DATABASE_URL` | `mysql+pymysql://<prefix>.root:<pw>@<host>:4000/datara?ssl_disabled=false&ssl_verify_cert=false&ssl_verify_identity=false` | Wajib sama dengan yang berhasil di tes lokal (Opsi A/B) |
   | `CORS_ORIGINS` | `https://<frontend>.vercel.app,http://localhost:3000` | Domain frontend yang sudah live (mis. `https://datara-murex.vercel.app`) |
   | `JWT_SECRET` | string acak min. 32 karakter | Dipakai menandatangani token login |
   | `GEMINI_API_KEY` | *(opsional)* | Untuk fitur AI Business Assistant |
   | `GOOGLE_CLIENT_ID` | *(opsional)* | Untuk login Google (endpoint `/auth/google`) |
6. Klik **Deploy** → tunggu build (instalasi dependensi + migrasi) selesai.
7. Buka domain yang diberikan (mis. `https://datara-api.vercel.app`):
   ```
   https://datara-api.vercel.app/api/health
   ```
   Hasil yang benar: `{"status": "ok", ...}`. Swagger di `/docs`.

Catatan `maxDuration`: file `backend/vercel.json` menetapkan fungsi berjalan hingga 60 detik. Endpoint AI chat yang memanggil Gemini termasuk hitungan ini; jika jawaban AI terlalu lama sehingga timeout, pertimbangkan pertanyaan yang lebih pendek atau optimasi waktu jawab model.

---

## 5. Langkah 3 — Frontend: Vercel (project #1)

1. Project frontend sudah dibuat dari repo yang sama dengan **Root Directory: `frontend`** (framework `Next.js` terdeteksi otomatis; `frontend/vercel.json` berisi build/install command).
2. Pastikan **Environment Variable** project:
   ```
   NEXT_PUBLIC_API_URL=https://datara-api.vercel.app/api/v1
   ```
   - Perhatikan suffix `/api/v1` — wajib ada (frontend memanggil path relatif ke base ini).
   - Ganti domain sesuai project backend Langkah 2.
3. Jika env berubah setelah deploy pertama → klik **Redeploy** di tab Deployments agar ter-pick-up.
4. Buka `https://<project>.vercel.app` — frontend siap dipakai.

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

- [ ] `https://datara-api.vercel.app/api/health` → `{"status": "ok", ...}`.
- [ ] `https://datara-api.vercel.app/docs` (Swagger UI) terbuka.
- [ ] Buka frontend → **Register** akun baru → **Login** berhasil (token tersimpan).
- [ ] Tambah **produk + HPP**, catat **transaksi**, cek dashboard & laporan menampilkan angka.
- [ ] Smart Pricing / Smart Restock / Forecasting menghasilkan rekomendasi.
- [ ] **AI Business Assistant** menjawab dengan data (mis. "berapa stok produk X?") — bukan pesan fallback.
- [ ] (Jika diaktifkan) Google Sign-In berhasil.
- [ ] Tidak ada error CORS di DevTools (frontend memanggil `https://datara-api.vercel.app`).

---

## 8. Pemeliharaan & Batasan

| Hal | Kondisi | Tindakan |
|---|---|---|
| **Kuota function Vercel** | ±100K invocations + CPU-hours/bln | Trafik demo sangat jauh di bawah; pantau di dashboard Vercel → Usage. |
| **Function timeout** | Maks 60 detik per request | Pertanyaan AI yang sangat berat saat demo — biarkan singkat; halaman lain aman. |
| **Kuota RU TiDB** | Reset tiap bulan; habis = throttled sampai bulan berikutnya | Pantau usage di dashboard TiDB; trafik demo normal jauh di bawah kuota. |
| **Bandwidth Vercel** | 100 GB/bln | Cukup jauh untuk trafik demo; jika hampir habis, cek "Usage" di dashboard Vercel. |
| **Update kode** | Push ke `main` → kedua project Vercel auto-deploy | Migrasi DB otomatis jalan di build backend (idempotent). |
| **DB tidak kedaluwarsa** | TiDB Starter free forever | Tidak perlu membuat ulang database. |
| **Nonaktif sementara** | Tidak dipakai | Pause project di Vercel (Settings → Pause) tanpa biaya; data TiDB tetap aman; resume kapan saja. |

---

## 9. Troubleshooting

| Masalah | Kemungkinan penyebab | Solusi |
|---|---|---|
| Login DB `1045 Access denied` | Kredensial salah; host/port salah | Periksa user `<prefix>.root`, port `4000`, password benar; tes via GUI TiDB "Connect". |
| Error TLS saat tes lokal / deploy | Param SSL tidak dikenali atau CA tidak ditemukan | Pakai Opsi A (`ssl_disabled=false&ssl_verify_cert=false&ssl_verify_identity=false`); atau Opsi B (`ssl_ca=tidb-ca.pem` + file ada di `backend/`). |
| Build gagal dengan `No module named ...` | Requirements tidak ter-install / root directory salah | Pastikan Root Directory `backend` dan tidak ada penyimpangan requirements. |
| Build gagal `No such file or directory: 'alembic'` | Build Command dijalankan dari repo root | Build Command dijalankan relatif terhadap Root Directory (`backend`) — pastikan Root Directory sudah diset `backend`. |
| CORS error di browser | `CORS_ORIGINS` tidak memuat domain frontend | Set ke `https://<frontend>.vercel.app,http://localhost:3000`, lalu redeploy backend. |
| Frontend memanggil `localhost:8000` | `NEXT_PUBLIC_API_URL` tidak terset | Set var di project frontend + redeploy. |
| Function timeout (504) saat AI chat | Jawaban Gemini >60 detik | Ajukan pertanyaan lebih pendek; atau optimasi nanti (streaming). |
| Login Google error `redirect_uri_mismatch` | Origin tidak terdaftar di Google Console | Tambah `https://<project>.vercel.app` ke Authorized JavaScript origins (Langkah 4). |
| AI chat menjawab fallback "belum aktif" | `GEMINI_API_KEY` kosong | Isi key di project backend → redeploy. |

---

## 10. Referensi

- `backend/vercel.json` — konfigurasi Vercel backend (max duration 60 detik untuk fungsi `app/main.py`).
- `frontend/vercel.json` — konfigurasi Vercel frontend (framework Next.js, build/install command).
- `frontend/src/lib/api.ts` — base URL API (dari `NEXT_PUBLIC_API_URL`, default `http://localhost:8000/api/v1`).
- `backend/app/core/config.py` — variabel env yang dibaca backend (`DATABASE_URL`, `CORS_ORIGINS`, `JWT_SECRET`, `GEMINI_API_KEY`, `GOOGLE_CLIENT_ID`).
- `backend/alembic/env.py` — migrasi memakai `DATABASE_URL` dari environment.
- Dokumentasi resmi: [Deploy FastAPI di Vercel](https://vercel.com/docs/frameworks/backend/fastapi), [Python Runtime](https://vercel.com/docs/functions/runtimes/python), [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/).