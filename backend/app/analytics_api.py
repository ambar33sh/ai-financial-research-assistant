from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.analytics import calculate_metrics
from app.services.risk_detector import detect_financial_risks

router = APIRouter(prefix="/analytics", tags=["analytics"])


class MetricsRequest(BaseModel):
    revenue: float | None = None
    previous_revenue: float | None = None
    beginning_revenue: float | None = None
    years: float | None = None
    gross_profit: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    free_cash_flow: float | None = None
    debt: float | None = None
    equity: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    quick_assets: float | None = None
    net_income_for_return: float | None = None
    average_equity: float | None = None
    average_assets: float | None = None
    invested_capital: float | None = None


class RiskRequest(BaseModel):
    revenue_growth: float | None = None
    operating_margin: float | None = None
    previous_operating_margin: float | None = None
    free_cash_flow: float | None = None
    debt: float | None = None
    previous_debt: float | None = None
    current_ratio: float | None = None


@router.post("/metrics")
def metrics(request: MetricsRequest) -> dict:
    try:
        return calculate_metrics(**request.model_dump()).__dict__
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/risks")
def risks(request: RiskRequest) -> list[dict]:
    return [flag.__dict__ for flag in detect_financial_risks(**request.model_dump())]
