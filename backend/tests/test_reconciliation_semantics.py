"""Test targeted reconciliation — Inventory Movement Type & Decision Dismiss.

Validasi dua fuzzy point yang diselesaikan:

1. Inventory movement type (API Contract bab 9.2 lowercase <-> Data Dictionary
   bab 9.2 enum DB), termasuk `sale` dan roundtrip request-database-response.

2. Decision dismiss lifecycle: hanya rekomendasi PENDING yang dapat di-dismiss;
   rekomendasi/keputusan yang sudah di-apply (ACCEPTED / DecisionApplied)
   ditolak. Generic dismiss simetris dengan apply_generic.
"""
from types import SimpleNamespace

import pytest

from app.core.errors import BusinessError, ConflictError, NotFoundError
from app.models.enums import MovementType, RecommendationStatus
from app.schemas.inventory import InventoryMovementCreateRequest
from app.services import decision_service, inventory_service


# ---------------------------------------------------------------- Movement Type

def test_schema_accepts_all_contract_terms() -> None:
    for term in ("received", "waste", "adjustment", "sale"):
        req = InventoryMovementCreateRequest(product_id=1, movement_type=term, quantity=2)
        assert req.movement_type == term


def test_schema_rejects_unknown_movement_type() -> None:
    with pytest.raises(Exception):
        InventoryMovementCreateRequest(product_id=1, movement_type="issued", quantity=2)


def test_movement_map_db_enum_consistency() -> None:
    """Setiap API term (kontrak) terpetakan ke enum DB canonikal, tanpa duplikat."""
    assert inventory_service._MOVEMENT_MAP["received"] is MovementType.RESTOCK
    assert inventory_service._MOVEMENT_MAP["sale"] is MovementType.SALE
    assert inventory_service._MOVEMENT_MAP["waste"] is MovementType.WASTE
    assert inventory_service._MOVEMENT_MAP["adjustment"] is MovementType.ADJUSTMENT
    assert len(inventory_service._MOVEMENT_MAP) == 4


def test_api_term_roundtrip_all_db_enums() -> None:
    """Roundtrip enum DB -> API term -> enum DB identik (response konsisten)."""
    for enum_value in MovementType:
        term = inventory_service._MOVEMENT_API_TERM[enum_value]
        assert inventory_service._MOVEMENT_MAP[term] is enum_value


def test_compute_delta_received_adds() -> None:
    assert inventory_service._compute_delta("received", 5) == 5


def test_compute_delta_waste_subtracts() -> None:
    assert inventory_service._compute_delta("waste", 3) == -3


def test_compute_delta_sale_subtracts() -> None:
    assert inventory_service._compute_delta("sale", 4) == -4


def test_compute_delta_adjustment_is_signed() -> None:
    assert inventory_service._compute_delta("adjustment", 7) == 7
    assert inventory_service._compute_delta("adjustment", -7) == -7


def test_compute_delta_rejects_non_positive_received() -> None:
    with pytest.raises(BusinessError):
        inventory_service._compute_delta("received", 0)
    with pytest.raises(BusinessError):
        inventory_service._compute_delta("received", -1)


def test_compute_delta_rejects_non_positive_waste() -> None:
    with pytest.raises(BusinessError):
        inventory_service._compute_delta("waste", 0)


def test_compute_delta_rejects_non_positive_sale() -> None:
    with pytest.raises(BusinessError):
        inventory_service._compute_delta("sale", 0)


# ---------------------------------------------------------------- Decision Dismiss

def _pending_pricing_rec() -> SimpleNamespace:
    return SimpleNamespace(id=11, status=RecommendationStatus.PENDING)


def _accepted_pricing_rec() -> SimpleNamespace:
    return SimpleNamespace(id=11, status=RecommendationStatus.ACCEPTED)


def _fake_db() -> SimpleNamespace:
    return SimpleNamespace(commit=lambda: None)


def test_dismiss_pricing_pending_succeeds(monkeypatch) -> None:
    rec = _pending_pricing_rec()
    monkeypatch.setattr(decision_service.recommendation_repository, "get_pricing_recommendation",
                        lambda db, rid, bid: rec)
    result = decision_service.dismiss_pricing(_fake_db(), SimpleNamespace(id=1), 11)
    assert result == {"id": 11, "status": "dismissed"}
    assert rec.status is RecommendationStatus.DISMISSED


def test_dismiss_pricing_accepted_rejected(monkeypatch) -> None:
    rec = _accepted_pricing_rec()
    monkeypatch.setattr(decision_service.recommendation_repository, "get_pricing_recommendation",
                        lambda db, rid, bid: rec)
    with pytest.raises(ConflictError):
        decision_service.dismiss_pricing(_fake_db(), SimpleNamespace(id=1), 11)
    assert rec.status is RecommendationStatus.ACCEPTED  # status tidak berubah


def test_dismiss_restock_pending_succeeds(monkeypatch) -> None:
    rec = SimpleNamespace(id=22, status=RecommendationStatus.PENDING)
    monkeypatch.setattr(decision_service.recommendation_repository, "get_restock_recommendation",
                        lambda db, rid, bid: rec)
    result = decision_service.dismiss_restock(_fake_db(), SimpleNamespace(id=1), 22)
    assert result == {"id": 22, "status": "dismissed"}
    assert rec.status is RecommendationStatus.DISMISSED


def test_dismiss_restock_accepted_rejected(monkeypatch) -> None:
    rec = SimpleNamespace(id=22, status=RecommendationStatus.ACCEPTED)
    monkeypatch.setattr(decision_service.recommendation_repository, "get_restock_recommendation",
                        lambda db, rid, bid: rec)
    with pytest.raises(ConflictError):
        decision_service.dismiss_restock(_fake_db(), SimpleNamespace(id=1), 22)
    assert rec.status is RecommendationStatus.ACCEPTED


def test_generic_dismiss_resolves_pending_pricing(monkeypatch) -> None:
    """Generic /decisions/{id}/dismiss harus bisa me-dismiss rekomendasi PENDING."""
    rec = _pending_pricing_rec()
    monkeypatch.setattr(decision_service.recommendation_repository, "get_pricing_recommendation",
                        lambda db, rid, bid: rec)
    result = decision_service.dismiss(_fake_db(), SimpleNamespace(id=1), 11)
    assert result["status"] == "dismissed"
    assert rec.status is RecommendationStatus.DISMISSED


def test_generic_dismiss_rejects_applied_decision(monkeypatch) -> None:
    """Applied decision (DecisionApplied) tidak boleh di-dismiss."""
    decision = SimpleNamespace(id=55)
    monkeypatch.setattr(decision_service.recommendation_repository, "get_pricing_recommendation",
                        lambda db, rid, bid: None)
    monkeypatch.setattr(decision_service.recommendation_repository, "get_restock_recommendation",
                        lambda db, rid, bid: None)
    monkeypatch.setattr(decision_service.recommendation_repository, "get_decision",
                        lambda db, did, bid: decision)
    with pytest.raises(ConflictError):
        decision_service.dismiss(_fake_db(), SimpleNamespace(id=1), 55)


def test_generic_dismiss_unknown_rejected(monkeypatch) -> None:
    monkeypatch.setattr(decision_service.recommendation_repository, "get_pricing_recommendation",
                        lambda db, rid, bid: None)
    monkeypatch.setattr(decision_service.recommendation_repository, "get_restock_recommendation",
                        lambda db, rid, bid: None)
    monkeypatch.setattr(decision_service.recommendation_repository, "get_decision",
                        lambda db, did, bid: None)
    with pytest.raises(NotFoundError):
        decision_service.dismiss(_fake_db(), SimpleNamespace(id=1), 999)