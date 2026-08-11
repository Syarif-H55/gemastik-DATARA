"""Repository akses data untuk rekomendasi, keputusan, forecast, health & growth."""
from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models.business_configuration import BusinessConfiguration
from app.models.business_health_assessment import BusinessHealthAssessment
from app.models.decision_applied import DecisionApplied
from app.models.enums import (
    DecisionAppliedStatus,
    DecisionAppliedType,
    HealthStatus,
    RecommendationStatus,
)
from app.models.forecast_result import ForecastResult
from app.models.growth_recommendation import GrowthRecommendation
from app.models.pricing_recommendation import PricingRecommendation
from app.models.restock_recommendation import RestockRecommendation


def get_configuration(db: Session, business_id: int) -> BusinessConfiguration | None:
    return (
        db.query(BusinessConfiguration)
        .filter(BusinessConfiguration.business_id == business_id)
        .first()
    )


def get_pricing_recommendation(db: Session, recommendation_id: int, business_id: int) -> PricingRecommendation | None:
    return (
        db.query(PricingRecommendation)
        .filter(
            PricingRecommendation.id == recommendation_id,
            PricingRecommendation.business_id == business_id,
        )
        .first()
    )


def list_pricing_recommendations(db: Session, business_id: int) -> list[PricingRecommendation]:
    return (
        db.query(PricingRecommendation)
        .filter(PricingRecommendation.business_id == business_id)
        .order_by(PricingRecommendation.generated_at.desc())
        .all()
    )


def create_pricing_recommendation(
    db: Session,
    *,
    business_id: int,
    product_id: int,
    current_price: float,
    current_hpp: float,
    recommended_price: float,
    estimated_margin: float,
    reason_code: str | None,
    reason: str | None,
) -> PricingRecommendation:
    rec = PricingRecommendation(
        business_id=business_id,
        product_id=product_id,
        current_price=current_price,
        current_hpp=current_hpp,
        recommended_price=recommended_price,
        estimated_margin=estimated_margin,
        reason_code=reason_code,
        reason=reason,
        status=RecommendationStatus.PENDING,
    )
    db.add(rec)
    db.flush()
    return rec


def get_restock_recommendation(db: Session, recommendation_id: int, business_id: int) -> RestockRecommendation | None:
    return (
        db.query(RestockRecommendation)
        .filter(
            RestockRecommendation.id == recommendation_id,
            RestockRecommendation.business_id == business_id,
        )
        .first()
    )


def list_restock_recommendations(db: Session, business_id: int) -> list[RestockRecommendation]:
    return (
        db.query(RestockRecommendation)
        .filter(RestockRecommendation.business_id == business_id)
        .order_by(RestockRecommendation.generated_at.desc())
        .all()
    )


def create_restock_recommendation(
    db: Session,
    *,
    business_id: int,
    product_id: int,
    current_stock: float,
    forecasted_demand: float,
    safety_days: float,
    recommended_quantity: float,
    reason_code: str | None,
    reason: str | None = None,
) -> RestockRecommendation:
    rec = RestockRecommendation(
        business_id=business_id,
        product_id=product_id,
        current_stock=current_stock,
        forecasted_demand=forecasted_demand,
        safety_days=safety_days,
        recommended_quantity=recommended_quantity,
        reason_code=reason_code,
        reason=reason,
        status=RecommendationStatus.PENDING,
    )
    db.add(rec)
    db.flush()
    return rec


def get_forecasts_by_product(db: Session, product_id: int) -> list[ForecastResult]:
    return (
        db.query(ForecastResult)
        .filter(ForecastResult.product_id == product_id)
        .order_by(ForecastResult.forecast_date.asc())
        .all()
    )


def create_forecast(
    db: Session,
    *,
    business_id: int,
    product_id: int,
    forecast_date: date,
    predicted_quantity: float,
    model_version: str | None,
) -> ForecastResult:
    forecast = ForecastResult(
        business_id=business_id,
        product_id=product_id,
        forecast_date=forecast_date,
        predicted_quantity=predicted_quantity,
        model_version=model_version,
    )
    db.add(forecast)
    db.flush()
    return forecast


def list_applied_decisions(db: Session, business_id: int) -> list[DecisionApplied]:
    return (
        db.query(DecisionApplied)
        .filter(DecisionApplied.business_id == business_id)
        .order_by(DecisionApplied.applied_at.desc(), DecisionApplied.id.desc())
        .all()
    )


def get_decision(db: Session, decision_id: int, business_id: int) -> DecisionApplied | None:
    return (
        db.query(DecisionApplied)
        .filter(DecisionApplied.id == decision_id, DecisionApplied.business_id == business_id)
        .first()
    )


def create_decision(
    db: Session,
    *,
    business_id: int,
    recommendation_id: int | None,
    decision_type: DecisionAppliedType,
    title: str,
    summary: str | None,
    reasoning: str | None,
    metrics_before: dict,
    status: DecisionAppliedStatus,
    outcome_notes: str | None = None,
) -> DecisionApplied:
    decision = DecisionApplied(
        business_id=business_id,
        recommendation_id=recommendation_id,
        type=decision_type,
        title=title,
        summary=summary,
        reasoning=reasoning,
        metrics_before=metrics_before,
        status=status,
        outcome_notes=outcome_notes,
    )
    db.add(decision)
    db.flush()
    db.refresh(decision)  # muat server_default (applied_at/created_at)
    return decision


def count_applied_decisions(db: Session, business_id: int) -> int:
    return (
        db.query(DecisionApplied)
        .filter(DecisionApplied.business_id == business_id)
        .count()
    )


def get_latest_health(db: Session, business_id: int) -> BusinessHealthAssessment | None:
    return (
        db.query(BusinessHealthAssessment)
        .filter(BusinessHealthAssessment.business_id == business_id)
        .order_by(BusinessHealthAssessment.generated_at.desc())
        .first()
    )


def create_health_assessment(
    db: Session,
    *,
    business_id: int,
    period_start: date,
    period_end: date,
    health_status: HealthStatus,
    score: float,
) -> BusinessHealthAssessment:
    assessment = BusinessHealthAssessment(
        business_id=business_id,
        period_start=period_start,
        period_end=period_end,
        health_status=health_status,
        score=score,
    )
    db.add(assessment)
    db.flush()
    return assessment


def list_growth_recommendations(db: Session, business_id: int) -> list[GrowthRecommendation]:
    return (
        db.query(GrowthRecommendation)
        .filter(GrowthRecommendation.business_id == business_id)
        .order_by(GrowthRecommendation.generated_at.desc())
        .all()
    )
