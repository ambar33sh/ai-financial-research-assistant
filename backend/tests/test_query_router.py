from app.services.query_router import QueryRouter


def test_router_routes_calculation():
    assert QueryRouter().route("What is the revenue growth rate?") == "analytics"


def test_router_routes_research():
    assert QueryRouter().route("What risks did management mention?") == "rag"


def test_router_routes_hybrid():
    assert QueryRouter().route("Why did operating margin decline?") == "hybrid"
