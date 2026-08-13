"""Test deterministik Smart Pricing & Smart Restock (tanpa MySQL).

Validasi TASK 07 & 09 core business rules:
- Pricing tetap menguntungkan (HPP < harga rekomendasi), tanpa harga ekstrem,
  tanda margin bermasalah saat HPP >= price, dan reason_code yang benar.
- Restock urgency critical/low/healthy dan suggested_quantity tidak negatif.
"""
from types import SimpleNamespace

import pytest

from app.services import pricing_service, restock_service


# ---------------------------------------------------------------- Helpers

def _fake_product(*, selling_price: float, hpp: float) -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        name="Produk Test",
        sku="MIN001",
        selling_price=selling_price,
        low_stock_threshold=5,
    )


# ---------------------------------------------------------------- Pricing

def test_round_price_rounds_up_to_500() -> None:
    assert pricing_service._round_price(10_100) == 10_500
    assert pricing_service._round_price(10_000) == 10_000
    assert pricing_service._round_price(0) == 0


def test_pricing_normal_recommendation(monkeypatch) -> None:
    monkeypatch.setattr(pricing_service, "compute_unit_hpp", lambda db, pid: 8000.0)
    product = _fake_product(selling_price=12_000, hpp=8000)
    rec = pricing_service.build_recommendation(None, product, target_margin=50)

    assert rec["reason_code"] == "margin_below_target"
    assert rec["recommended_price"] > rec["hpp"]  # tetap profit
    # cost_based = 8000 / (1-0.5) = 16000, rounded up ke 16000
    assert rec["recommended_price"] == 16_000
    assert rec["estimated_margin"] == pytest.approx(50.0)


def test_pricing_already_healthy(monkeypatch) -> None:
    monkeypatch.setattr(pricing_service, "compute_unit_hpp", lambda db, pid: 4000.0)
    product = _fake_product(selling_price=12_000, hpp=4000)
    rec = pricing_service.build_recommendation(None, product, target_margin=50)

    assert rec["reason_code"] == "already_healthy"
    assert rec["recommended_price"] <= rec["current_price"]


def test_pricing_hpp_equals_price_flags_problem(monkeypatch) -> None:
    monkeypatch.setattr(pricing_service, "compute_unit_hpp", lambda db, pid: 12_000.0)
    product = _fake_product(selling_price=12_000, hpp=12_000)
    rec = pricing_service.build_recommendation(None, product, target_margin=30)

    assert rec["reason_code"] == "margin_below_target"
    assert rec["actual_margin_percent"] == pytest.approx(0.0)


def test_pricing_missing_hpp_no_fake_recommendation(monkeypatch) -> None:
    monkeypatch.setattr(pricing_service, "compute_unit_hpp", lambda db, pid: 0.0)
    product = _fake_product(selling_price=12_000, hpp=0)
    rec = pricing_service.build_recommendation(None, product, target_margin=30)

    assert rec["reason_code"] == "incomplete_hpp"
    assert rec["recommended_price"] == rec["current_price"]  # tidak membuat harga palsu


def test_pricing_very_high_target_margin_stays_profitable(monkeypatch) -> None:
    monkeypatch.setattr(pricing_service, "compute_unit_hpp", lambda db, pid: 10_000.0)
    product = _fake_product(selling_price=12_000, hpp=10_000)
    rec = pricing_service.build_recommendation(None, product, target_margin=90)

    assert rec["reason_code"] == "margin_below_target"
    assert rec["recommended_price"] > rec["hpp"]


# ---------------------------------------------------------------- Restock

def test_restock_critical_when_below_threshold(monkeypatch) -> None:
    monkeypatch.setattr(restock_service, "get_current_stock", lambda db, pid: 3.0)
    monkeypatch.setattr(
        restock_service.forecasting_service,
        "forecast_all",
        lambda db, business: [{"product_id": 1, "predicted_units": 5.0}],
    )
    product = _fake_product(selling_price=12_000, hpp=8000)
    rec = restock_service.build_recommendation(None, None, product, safety_days=3, lead_time=2)

    assert rec["urgency"] == "critical"
    # predicted * (lead+safety) - stock = 5*5 - 3 = 22
    assert rec["suggested_quantity"] == pytest.approx(22.0)


def test_restock_low_when_near_threshold(monkeypatch) -> None:
    monkeypatch.setattr(restock_service, "get_current_stock", lambda db, pid: 20.0)
    monkeypatch.setattr(
        restock_service.forecasting_service,
        "forecast_all",
        lambda db, business: [{"product_id": 1, "predicted_units": 5.0}],
    )
    product = _fake_product(selling_price=12_000, hpp=8000)
    rec = restock_service.build_recommendation(None, None, product, safety_days=3, lead_time=2)

    assert rec["urgency"] == "low"
    assert rec["suggested_quantity"] == pytest.approx(5.0)


def test_restock_healthy_when_sufficient(monkeypatch) -> None:
    monkeypatch.setattr(restock_service, "get_current_stock", lambda db, pid: 100.0)
    monkeypatch.setattr(
        restock_service.forecasting_service,
        "forecast_all",
        lambda db, business: [{"product_id": 1, "predicted_units": 5.0}],
    )
    product = _fake_product(selling_price=12_000, hpp=8000)
    rec = restock_service.build_recommendation(None, None, product, safety_days=3, lead_time=2)

    assert rec["urgency"] == "healthy"
    assert rec["suggested_quantity"] == 0.0


def test_restock_no_forecast_not_negative(monkeypatch) -> None:
    monkeypatch.setattr(restock_service, "get_current_stock", lambda db, pid: 2.0)
    monkeypatch.setattr(
        restock_service.forecasting_service,
        "forecast_all",
        lambda db, business: [],
    )
    product = _fake_product(selling_price=12_000, hpp=8000)
    rec = restock_service.build_recommendation(None, None, product, safety_days=3, lead_time=2)

    assert rec["suggested_quantity"] == 0.0
    assert rec["urgency"] == "critical"  # stok di bawah threshold tanpa forecast
    assert rec["predicted_daily"] == 0.0


def test_restock_quantity_never_negative_on_zero_stock(monkeypatch) -> None:
    monkeypatch.setattr(restock_service, "get_current_stock", lambda db, pid: 0.0)
    monkeypatch.setattr(
        restock_service.forecasting_service,
        "forecast_all",
        lambda db, business: [{"product_id": 1, "predicted_units": 4.0}],
    )
    product = _fake_product(selling_price=12_000, hpp=8000)
    rec = restock_service.build_recommendation(None, None, product, safety_days=1, lead_time=1)

    assert rec["suggested_quantity"] >= 0
    assert rec["urgency"] == "critical"


def test_restock_suggested_quantity_is_whole_unit(monkeypatch) -> None:
    """suggested_quantity harus unit bulat (ceil), bukan pecahan seperti 6,2."""
    monkeypatch.setattr(restock_service, "get_current_stock", lambda db, pid: 10.0)
    monkeypatch.setattr(
        restock_service.forecasting_service,
        "forecast_all",
        lambda db, business: [{"product_id": 1, "predicted_units": 5.4}],
    )
    product = _fake_product(selling_price=12_000, hpp=8000)
    rec = restock_service.build_recommendation(None, None, product, safety_days=1, lead_time=2)

    # 5.4 * (2+1) - 10 = 6.2 -> dibulatkan ke atas = 7 unit (bukan 6.2)
    assert rec["suggested_quantity"] == 7
    assert isinstance(rec["suggested_quantity"], int)