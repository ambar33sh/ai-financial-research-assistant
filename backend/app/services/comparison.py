from app.services.analytics import margin, pct_change


def compare_companies(company_a: dict, company_b: dict) -> dict:
    """Compare already-source-verified financial inputs without LLM arithmetic."""
    metrics = [
        "revenue_growth",
        "gross_margin",
        "operating_margin",
        "net_margin",
        "fcf_margin",
        "debt_to_equity",
        "roe",
    ]
    return {
        "company_a": company_a.get("company"),
        "company_b": company_b.get("company"),
        "metrics": {
            metric: {"a": company_a.get(metric), "b": company_b.get(metric)}
            for metric in metrics
        },
    }
