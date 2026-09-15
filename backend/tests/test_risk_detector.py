from app.services.risk_detector import detect_financial_risks


def test_negative_growth_creates_revenue_risk():
    flags = detect_financial_risks(revenue_growth=-4.2)
    assert flags[0].category == "Revenue"
    assert flags[0].severity == "high"


def test_positive_metrics_do_not_create_false_flags():
    flags = detect_financial_risks(revenue_growth=8.0, free_cash_flow=20.0, debt=90, previous_debt=100, current_ratio=1.5)
    assert flags == []
