# DATARA Backend

Backend REST API untuk **DATARA — Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM**.

- **Stack:** FastAPI + SQLAlchemy + MySQL + Alembic + Pydantic v2
- **Business API canonical prefix:** `/api/v1`
- **Health check prefix:** `/api` (`/api/health`, `/api/health/db`)
- **Kontrak:** `../documents/API_CONTRACT_API_SPECIFICATION_DATARA.md`, Data Model di `../documents/DATA_DICTIONARY_AND_DATA_MODEL_DATARA.md`

## Struktur

```text
backend/
├── app/
│   ├── main.py            # FastAPI app (CORS, error handlers, router)
│   ├── core/              # config, errors, exception handlers
│   ├── db/                # engine, session, Base, registrasi model
│   ├── models/            # entity SQLAlchemy (sesuai Data Model)
│   ├── schemas/           # Pydantic request/response
│   ├── api/               # router + deps + health, v1 untuk rute bisnis
│   ├── services/          # business logic / decision engine (source of truth)
│   └── repositories/      # akses data per entitas
├── alembic/               # migration
├── tests/                 # pytest
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

copy .env.example .env          # lalu isi koneksi MySQL
```

### Environment variables

| Variable       | Wajib | Deskripsi                                                        |
| -------------- | ----- | ---------------------------------------------------------------- |
| `DATABASE_URL` | Ya    | DSN MySQL, contoh `mysql+pymysql://user:pass@localhost:3306/datara` |
| `DB_USER`/`DB_PASSWORD`/`DB_HOST`/`DB_PORT`/`DB_NAME` | Opsional | Fallback bila `DATABASE_URL` tidak diset |
| `CORS_ORIGINS` | Opsional | Origin frontend diizinkan, pisahkan dengan koma. Default `http://localhost:3000` |
| `JWT_SECRET` | Ya    | Secret acak (min. 32 karakter) untuk access token JWT |
| `JWT_ALGORITHM` | Opsional | Algoritma JWT, default `HS256` |
| `JWT_EXPIRE_MINUTES` | Opsional | Masa berlaku token, default `1440` (1 hari) |

Kredensial tidak di-hardcode. Semua nilai rahasia dibaca dari `.env` (git-ignored).

## Menjalankan

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

python.exe -m uvicorn app.main:app --reload --port 8000
```

Dokumentasi otomatis (OpenAPI): `http://localhost:8000/docs`.

### Health check

```text
GET /api/health       -> {"success": true, "data": {"status": "ok", ...}}
GET /api/health/db    -> 200 bila MySQL dapat dihubungi, 503 bila tidak
```

### Authentication

```text
POST /api/v1/auth/login     -> {"success": true, "data": {"user": {...}, "access_token": "..."}}
GET  /api/v1/auth/me        -> user terautentikasi (Authorization: Bearer <token>)
POST /api/v1/auth/logout    -> {"success": true, "message": "Logged out successfully"}
GET  /api/v1/business       -> business milik user terautentikasi (ownership server-side)
```

Token: JWT (stateless, `Authorization: Bearer <access_token>`). Password di-hash dengan bcrypt — tidak pernah disimpan/dikembalikan plaintext.

Buat akun demo (API Contract MVP tidak punya endpoint `register`):

```bash
python -m scripts.seed_demo_user --email owner@umkm.id --name "Budi" \
    --password rahasia123 --business "Kedai Contoh" --business-type food_beverage
```

## Migration (Alembic)

```bash
alembic upgrade head          # terapkan semua migration
alembic revision --autogenerate -m "desc"   # buat migration baru dari model
alembic downgrade -1          # rollback satu step
```

Verifikasi tanpa database:

```bash
alembic upgrade head --sql    # render SQL offline
```

## Test

```bash
pytest
```

## Catatan

- Backend adalah **source of truth** untuk seluruh kalkulasi bisnis.
- Business API canonical URL: `http://localhost:8000/api/v1` (setting `NEXT_PUBLIC_API_URL` frontend disesuaikan saat tahap integrasi).
- Setiap request business data wajib melalui authenticated user + business ownership (diimplementasikan pada task autentikasi).
- Rute bisnis versi `v1` mengikuti API Contract dan ditambahkan di `app/api/v1/router.py`.
- Endpoint health tetap di `/api/health` dan `/api/health/db` (di luar versioning).
