from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialMetrics:
    revenue_growth: float | None = None
    cagr: float | None = None
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None
    fcf_margin: float | None = None
    debt_to_equity: float | None = None
    current_ratio: float | None = None
    quick_ratio: float | None = None
    roe: float | None = None
    roa: float | None = None
    roic: float | None = None


def pct_change(current: float, previous: float) -> float:
    if previous == 0:
        raise ValueError("Previous value cannot be zero")
    return (current - previous) / abs(previous) * 100


def margin(numerator: float, denominator: float) -> float:
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    return numerator / denominator * 100


def cagr(beginning: float, ending: float, years: float) -> float:
    if beginning <= 0 or ending < 0 or years <= 0:
        raise ValueError("CAGR requires positive beginning value and years > 0")
    return ((ending / beginning) ** (1 / years) - 1) * 100


def calculate_metrics(
    *, revenue: float | None = None,
    previous_revenue: float | None = None,
    beginning_revenue: float | None = None,
    years: float | None = None,
    gross_profit: float | None = None,
    operating_income: float | None = None,
    net_income: float | None = None,
    free_cash_flow: float | None = None,
    debt: float | None = None,
    equity: float | None = None,
    current_assets: float | None = None,
    current_liabilities: float | None = None,
    quick_assets: float | None = None,
    net_income_for_return: float | None = None,
    average_equity: float | None = None,
    average_assets: float | None = None,
    invested_capital: float | None = None,
) -> FinancialMetrics:
    growth = pct_change(revenue, previous_revenue) if revenue is not None and previous_revenue is not None else None
    growth_cagr = cagr(beginning_revenue, revenue, years) if beginning_revenue is not None and revenue is not None and years else None
    return FinancialMetrics(
        revenue_growth=growth,
        cagr=growth_cagr,
        gross_margin=margin(gross_profit, revenue) if gross_profit is not None and revenue else None,
        operating_margin=margin(operating_income, revenue) if operating_income is not None and revenue else None,
        net_margin=margin(net_income, revenue) if net_income is not None and revenue else None,
        fcf_margin=margin(free_cash_flow, revenue) if free_cash_flow is not None and revenue else None,
        debt_to_equity=debt / equity if debt is not None and equity else None,
        current_ratio=current_assets / current_liabilities if current_assets is not None and current_liabilities else None,
        quick_ratio=quick_assets / current_liabilities if quick_assets is not None and current_liabilities else None,
        roe=net_income_for_return / average_equity * 100 if net_income_for_return is not None and average_equity else None,
        roa=net_income_for_return / average_assets * 100 if net_income_for_return is not None and average_assets else None,
        roic=operating_income / invested_capital * 100 if operating_income is not None and invested_capital else None,
    )
