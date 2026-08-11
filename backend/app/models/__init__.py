"""Registrasi semua model agar mapper/relationship ter-resolve dengan benar.

Sebagian relasi memakai string reference (mis. ``Business.configuration``),
sehingga kelas target harus sudah ter-import sebelum mapper dikonfigurasi.
Dengan memuat ``base_models`` di sini, siapa pun yang meng-import model
(service, repository, script, test) otomatis meregistrasi seluruh model.
"""
from app.db import base_models  # noqa: F401
