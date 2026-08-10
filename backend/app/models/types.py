"""Type & kolom bersama agar konsisten dengan DATA DICTIONARY (BIGINT UNSIGNED, DECIMAL, dsb)."""
from sqlalchemy import BigInteger
from sqlalchemy.dialects import mysql


def pk_bigint() -> BigInteger:
    return BigInteger().with_variant(mysql.BIGINT(unsigned=True), "mysql")


def fk_bigint() -> BigInteger:
    return BigInteger().with_variant(mysql.BIGINT(unsigned=True), "mysql")
