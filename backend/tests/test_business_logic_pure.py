"""Test deterministik business logic murni (tanpa MySQL).

Mencakup:
- Forecasting: dynamic confidence & exponential smoothing.
- Decision monitoring: derive status & enum UNKNOWN.
- Expense: mapping kategori <-> enum.
- Health label: tidak ada label demo "Cukup".
"""
from datetime import datetime

import pytest

from app.models.enums import DecisionAppliedStatus
from app.schemas.finance import expense_category_to_enum, expense_enum_to_category
from app.services.analytics_service import _health_label, _health_status
from app.services.decision_service import _derive_status
from app.services.forecasting_service import _coefficient_of_variation, _dynamic_confidence, _exponential_smoothing_forecast


# ---------------------------------------------------------------- Forecasting

def test_exponential_smoothing_flat_series() -> None:
    series = [10.0, 10.0, 10.0, 10.0]
    result = _exponential_smoothing_forecast(series, alpha=0.3)
    assert abs(result - 10.0) < 1e-9


def test_exponential_smoothing_trend() -> None:
    series = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = _exponential_smoothing_forecast(series, alpha=0.5)
    assert result > 4.0  # memberi bobot lebih pada data terbaru (di atas rata-rata 3)


def test_exponential_smoothing_empty() -> None:
    assert _exponential_smoothing_forecast([], alpha=0.3) == 0.0


def test_dynamic_confidence_in_bounds() -> None:
    for model in ("insufficient", "simple", "moving", "exponential"):
        for active_days in (0, 1, 7, 14, 30):
            conf = _dynamic_confidence(model, active_days, [10.0] * active_days)
            assert isinstance(conf, int)
            assert 5 <= conf <= 92


def test_dynamic_confidence_high_variability_lower() -> None:
    stable = _dynamic_confidence("moving", 7, [10.0] * 7)
    volatile = _dynamic_confidence("moving", 7, [10.0, 0.0, 25.0, 2.0, 18.0, 0.0, 20.0])
    assert volatile < stable


def test_coefficient_of_variation() -> None:
    assert _coefficient_of_variation([]) == 99.0
    assert abs(_coefficient_of_variation([10.0, 10.0, 10.0]) - 0.0) < 1e-9
    assert _coefficient_of_variation([0.0, 0.0]) == 99.0


# ---------------------------------------------------------------- Health labels

def test_health_labels_no_demo_label() -> None:
    assert _health_label(80) == "Sehat"
    assert _health_label(60) == "Perlu Perhatian"
    assert _health_label(30) == "Berisiko"
    assert "Cukup" not in _health_label(60)


def test_health_status_mapping() -> None:
    assert _health_status(80) == "SEHAT"
    assert _health_status(60) == "PERLU_PERHATIAN"
    assert _health_status(30) == "BERISIKO"


# ---------------------------------------------------------------- Decision monitoring

def test_derive_status_improved_when_any_growth() -> None:
    before = {"revenue": 100.0, "margin": 10.0, "stock": 5.0}
    after = {"revenue": 120.0, "margin": 10.0, "stock": 5.0}
    status, notes = _derive_status(before, after)
    assert status == DecisionAppliedStatus.IMPROVED
    assert notes


def test_derive_status_regressed_when_any_drop() -> None:
    before = {"revenue": 100.0, "margin": 10.0, "stock": 5.0}
    after = {"revenue": 90.0, "margin": 10.0, "stock": 5.0}
    status, _ = _derive_status(before, after)
    assert status == DecisionAppliedStatus.REGRESSED


def test_derive_status_flat_when_all_equal() -> None:
    before = {"revenue": 100.0, "margin": 10.0, "stock": 5.0}
    status, _ = _derive_status(before, dict(before))
    assert status == DecisionAppliedStatus.FLAT


def test_decision_unknown_status_available() -> None:
    assert DecisionAppliedStatus.UNKNOWN.value == "UNKNOWN"


def test_has_post_decision_data_structure(monkeypatch) -> None:
    """Verifikasi helper monitoring mengecek tx_count pada rentang pasca keputusan."""
    from app.services import decision_service

    applied_at = datetime(2026, 8, 1, 10, 0, 0)
    calls: list = []

    class _FakeTxRepo:
        def count_after(self, db, business_id, start):
            calls.append(start)
            return 3

    monkeypatch.setattr(decision_service.transaction_repository, "count_after", _FakeTxRepo().count_after)
    assert decision_service._has_post_decision_data(None, 1, applied_at) is True

    class _FakeTxRepoEmpty:
        def count_after(self, db, business_id, start):
            return 0

    monkeypatch.setattr(decision_service.transaction_repository, "count_after", _FakeTxRepoEmpty().count_after)
    assert decision_service._has_post_decision_data(None, 1, applied_at) is False

    assert calls[0] == applied_at


# ---------------------------------------------------------------- Expense mapping

def test_expense_category_roundtrip() -> None:
    for category in ("rent", "fixed_salary", "administrative", "other"):
        enum_value = expense_category_to_enum(category)
        assert expense_enum_to_category(enum_value) == category


def test_expense_category_unknown_rejected() -> None:
    with pytest.raises(KeyError):
        expense_category_to_enum("salary")