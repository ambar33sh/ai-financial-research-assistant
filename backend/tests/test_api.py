from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_documents_list_is_persistent_registry_backed():
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_document_lookup_returns_404_for_unknown_id():
    response = client.get("/api/v1/documents/not-a-real-document")
    assert response.status_code == 404


def test_metrics_zero_division_returns_422():
    response = client.post("/api/v1/analytics/metrics", json={
        "revenue": 100,
        "previous_revenue": 0,
    })
    assert response.status_code == 422
    assert "zero" in response.json()["detail"].lower()
