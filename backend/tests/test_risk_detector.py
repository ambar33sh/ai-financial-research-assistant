from app.services.language_risk_detector import detect_language_risks
from app.services.risk_detector import detect_financial_risks


def test_negative_growth_creates_revenue_risk():
    flags = detect_financial_risks(revenue_growth=-4.2)
    assert flags[0].category == "Revenue"
    assert flags[0].severity == "high"


def test_positive_metrics_do_not_create_false_flags():
    flags = detect_financial_risks(revenue_growth=8.0, free_cash_flow=20.0, debt=90, previous_debt=100, current_ratio=1.5)
    assert flags == []


def test_multiple_financial_risks_are_detected():
    flags = detect_financial_risks(revenue_growth=-4.0, free_cash_flow=-10.0, current_ratio=0.8)
    categories = {flag.category for flag in flags}
    assert {"Revenue", "Cash Flow", "Liquidity"}.issubset(categories)


def test_management_language_rules():
    text = "The company identified a material weakness in internal controls and substantial doubt about going concern."
    flags = detect_language_risks(text)
    categories = {flag.category for flag in flags}
    assert "Internal controls" in categories
    assert "Going concern" in categories
