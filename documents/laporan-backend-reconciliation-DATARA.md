# Laporan Reconciliation Backend DATARA — Movement Type & Decision Dismiss

> Tanggal: 12 Agustus 2026 · Fase D (penutupan gap dari
> `laporan-backend-task-progress-DATARA.md` temuan 6.1 & 6.2).
> Scope: penyelarasan terminology inventory movement type dan semantik dismiss.

---

## 1. Rangkuman

Dua fuzzy point yang ditandai ⚠️ di laporan sebelumnya telah diselesaikan
dengan **perubahan kecil & deterministik**:

| Issue | Sebelum | Sesudah |
| --- | --- | --- |
| 1. Movement type | `POST /inventory/movements` menerima `received \| waste \| adjustment` (tanpa `sale`); response `movement_type` dalam UPPERCASE enum DB (`RESTOCK` dll). | API menerima **`received \| waste \| adjustment \| sale`**; response selalu **lowercase** sama dengan request (roundtrip konsisten). |
| 2. Dismiss | `dismiss_pricing` / `dismiss_restock` selalu menandai `DISMISSED` tanpa mengecek status; dismiss generic `/decisions/{id}/dismiss` hanya menolak keputusan ter-apply. | Hanya rekomendasi **`PENDING`** yang dapat di-dismiss. Rekomendasi `ACCEPTED` ditolak `ConflictError`. Dismiss generic simetris dengan `apply_generic` (resolve id → pricing/restock). |

**Sumber acuan:** API Contract bab 9.2 (lowercase `sale/received/waste/adjustment`)
dan Data Dictionary bab 9.2 (`RESTOCK / SALE / ADJUSTMENT / WASTE`).

---

## 2. File yang Diubah

### Backend

| File | Perubahan |
| --- | --- |
| `backend/app/schemas/inventory.py` | Pattern `movement_type` → `^(received\|waste\|adjustment\|sale)$`; komentar terminologi API. |
| `backend/app/services/inventory_service.py` | Tambah memetakan `sale` → `MovementType.SALE`; map balik `_MOVEMENT_API_TERM` (DB enum → lowercase); `_compute_delta` menangani `sale` (negatif, harus > 0); guard stok cukup untuk sale; response pakai lowercase. |
| `backend/app/services/decision_service.py` | `_dismiss_pricing_rec`/`_dismiss_restock_rec` memeriksa status `PENDING` sebelum `DISMISSED`; `dismiss` generic resolve ke pricing/restock rec (simetris `apply_generic`), tetap tolak keputusan ter-apply. |

### Frontend

| File | Perubahan |
| --- | --- |
| `frontend/src/lib/types.ts` | `ProductMovementType` → `"received" \| "waste" \| "adjustment" \| "sale"` (hapus alias `issued`). |

### Dokumen

| File | Perubahan |
| --- | --- |
| `documents/laporan-backend-task-progress-DATARA.md` | Status T05/T10 → ✅, temuan 6.1/6.2 → resolved, angka test 85, rekomendasi terbaru. |
| `documents/catatan-inkonsistensi-frontend-DATARA.md` | Item 4 / §3.4 / tabel keputusan B → resolved (lowercase). |

### Test

| File | Perubahan |
| --- | --- |
| `backend/tests/test_reconciliation_semantics.py` | **Baru** — 18 test deterministik movement type & dismiss. |

---

## 3. Semantik Final

### 3.1 Movement type

- **Kontrak API (lowercase):** `sale`, `received`, `waste`, `adjustment`.
- **Enum DB (uppercase):** `SALE`, `RESTOCK`, `WASTE`, `ADJUSTMENT`.
- Pemetaan berada di `inventory_service.py` (`_MOVEMENT_MAP` + `_MOVEMENT_API_TERM`).
- Response `GET /inventory/movements` dan `POST /inventory/movements` mengembalikan
  terminology API yang sama (lowercase) — konsisten dengan request.
- Tanda `quantity` di DB: `received` +, `sale` −, `waste` −, `adjustment` bertanda.
- Guard: `received`/`sale`/`waste` wajib `> 0`; `sale` menolak bila stok tidak cukup.

### 3.2 Decision dismiss

- `POST /pricing/dismiss` dan `POST /restock/dismiss` hanya me-dismiss rekomendasi
  dengan status `PENDING`; status `ACCEPTED` → `ConflictError`.
- `POST /decisions/{id}/dismiss` (generic):
  1. Resolve id ke pricing recommendation → dismiss bila `PENDING`;
  2. Jika bukan, resolve ke restock recommendation → dismiss bila `PENDING`;
  3. Jika id adalah DecisionApplied (keputusan sudah diterapkan) → `ConflictError`;
  4. Jika tidak ditemukan → `NotFoundError`.
- Simetris dengan `apply_generic` (id yang sama dapat di-apply ketika `PENDING`,
  dan di-dismiss ketika belum di-apply).

---

## 4. Verifikasi

| Item | Hasil |
| --- | --- |
| `pytest` (backend) | **85 passed**, 0 gagal (termasuk 18 test reconciliation baru) |
| `python -m compileall app` | OK |
| `alembic upgrade head --sql` | OK (tanpa perubahan skema — tidak perlu migrasi baru) |
| OpenAPI (`app.openapi()`) | `movement_type` pattern `^(received\|waste\|adjustment\|sale)$`; endpoint dismiss terdaftar |
| `npm run lint` (frontend) | OK |
| `npm run build` (frontend, typecheck) | OK |

Tidak ada perubahan model/database → tidak ada migrasi baru.

---

## 5. Catatan

- Tidak ada skema DB yang berubah: enum DB tetap `RESTOCK/SALE/ADJUSTMENT/WASTE`
  (Data Dictionary). Perubahan hanya pada lapisan API (schema + service mapping).
- Test baru bersifat *unit deterministik* (tanpa DB) dan dapat dieksekusi tanpa MySQL.
- Sisa item yang masih menunggu keputusan (di luar scope task ini) tercatat di
  `laporan-backend-task-progress-DATARA.md` §6: `Role` frontend, `.env` AI/Google,
  warning deprecation pytest, dan data smoke test lokal.