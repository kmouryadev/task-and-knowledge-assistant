import httpx
import pytest

from app.tools import PermissionLevel
from app.tools.web import PERMISSIONS, search_web

FAKE_DDG_RESPONSE = {
    "AbstractText": "FastAPI is a modern, fast web framework for building APIs with Python.",
    "AbstractURL": "https://duckduckgo.com/FastAPI",
    "RelatedTopics": [
        {
            "Text": "Starlette - The ASGI framework FastAPI is built on.",
            "FirstURL": "https://duckduckgo.com/Starlette",
        },
        {
            "Name": "Related frameworks",
            "Topics": [
                {
                    "Text": "Flask - A lightweight WSGI web framework.",
                    "FirstURL": "https://duckduckgo.com/Flask",
                }
            ],
        },
    ],
}


def _mock_transport(request: httpx.Request) -> httpx.Response:
    assert request.url.host == "api.duckduckgo.com"
    assert request.url.params["q"] == "fastapi"
    return httpx.Response(200, json=FAKE_DDG_RESPONSE)


def test_search_web_returns_abstract_and_related_topics():
    client = httpx.Client(transport=httpx.MockTransport(_mock_transport))

    results = search_web("fastapi", limit=5, client=client)

    assert results[0].url == "https://duckduckgo.com/FastAPI"
    assert "modern, fast web framework" in results[0].snippet
    urls = {r.url for r in results}
    assert "https://duckduckgo.com/Starlette" in urls
    assert "https://duckduckgo.com/Flask" in urls


def test_search_web_respects_limit():
    client = httpx.Client(transport=httpx.MockTransport(_mock_transport))

    results = search_web("fastapi", limit=1, client=client)

    assert len(results) == 1


def test_search_web_rejects_empty_query():
    with pytest.raises(ValueError):
        search_web("")


def test_permissions_tagged():
    assert PERMISSIONS["search_web"] == PermissionLevel.READ
