from dataclasses import dataclass


@dataclass(frozen=True)
class RiskFlag:
    category: str
    severity: str
    message: str
    rationale: str


def detect_financial_risks(
    *,
    revenue_growth: float | None = None,
    operating_margin: float | None = None,
    previous_operating_margin: float | None = None,
    free_cash_flow: float | None = None,
    debt: float | None = None,
    previous_debt: float | None = None,
    current_ratio: float | None = None,
) -> list[RiskFlag]:
    flags: list[RiskFlag] = []
    if revenue_growth is not None and revenue_growth < 0:
        flags.append(RiskFlag("Revenue", "high", "Revenue declined", f"Reported revenue growth is {revenue_growth:.2f}%"))
    if operating_margin is not None and previous_operating_margin is not None and operating_margin < previous_operating_margin:
        flags.append(RiskFlag("Profitability", "medium", "Operating margin pressure", f"Operating margin fell from {previous_operating_margin:.2f}% to {operating_margin:.2f}%"))
    if free_cash_flow is not None and free_cash_flow < 0:
        flags.append(RiskFlag("Cash Flow", "high", "Negative free cash flow", f"Free cash flow is {free_cash_flow:.2f}"))
    if debt is not None and previous_debt is not None and debt > previous_debt:
        flags.append(RiskFlag("Leverage", "medium", "Debt increased", f"Debt increased from {previous_debt:.2f} to {debt:.2f}"))
    if current_ratio is not None and current_ratio < 1:
        flags.append(RiskFlag("Liquidity", "high", "Current ratio below 1", f"Current ratio is {current_ratio:.2f}"))
    return flags
