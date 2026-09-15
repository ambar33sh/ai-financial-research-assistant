import pytest

from app.services.analytics import cagr, margin, pct_change, ratio


def test_pct_change():
    assert pct_change(125, 100) == pytest.approx(25.0)


def test_margin():
    assert margin(25, 100) == pytest.approx(25.0)


def test_cagr():
    assert cagr(100, 121, 2) == pytest.approx(10.0)


def test_zero_previous_rejected():
    with pytest.raises(ValueError):
        pct_change(100, 0)


def test_zero_margin_denominator_rejected():
    with pytest.raises(ValueError):
        margin(25, 0)


def test_zero_ratio_denominator_rejected():
    with pytest.raises(ValueError):
        ratio(25, 0, "Debt-to-equity")
