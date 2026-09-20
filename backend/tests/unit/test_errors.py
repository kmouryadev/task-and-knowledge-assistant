from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.errors import NotFoundError, PolicyError, register_error_handlers


def make_app() -> FastAPI:
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/boom-404")
    def boom_404():
        raise NotFoundError("thing not found")

    @app.get("/boom-403")
    def boom_403():
        raise PolicyError("not allowed")

    return app


def test_not_found_error_returns_404():
    client = TestClient(make_app())
    response = client.get("/boom-404")
    assert response.status_code == 404
    assert response.json() == {"error": {"type": "NotFoundError", "detail": "thing not found"}}


def test_policy_error_returns_403():
    client = TestClient(make_app())
    response = client.get("/boom-403")
    assert response.status_code == 403
    assert response.json()["error"]["type"] == "PolicyError"
