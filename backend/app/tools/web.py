import httpx
from pydantic import BaseModel

from app.tools import PermissionLevel

_DDG_URL = "https://api.duckduckgo.com/"

PERMISSIONS: dict[str, PermissionLevel] = {
    "search_web": PermissionLevel.READ,
}


class WebResult(BaseModel):
    title: str
    url: str
    snippet: str


def _flatten_topics(topics: list[dict]) -> list[dict]:
    flat = []
    for topic in topics:
        if "Topics" in topic:
            flat.extend(_flatten_topics(topic["Topics"]))
        elif topic.get("FirstURL") and topic.get("Text"):
            flat.append(topic)
    return flat


def search_web(query: str, limit: int = 5, client: httpx.Client | None = None) -> list[WebResult]:
    if not query.strip():
        raise ValueError("query must not be empty")

    owns_client = client is None
    client = client or httpx.Client(timeout=10.0)
    try:
        response = client.get(
            _DDG_URL,
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
        )
        response.raise_for_status()
        data = response.json()
    finally:
        if owns_client:
            client.close()

    results: list[WebResult] = []

    if data.get("AbstractText") and data.get("AbstractURL"):
        results.append(
            WebResult(title=query, url=data["AbstractURL"], snippet=data["AbstractText"])
        )

    for topic in _flatten_topics(data.get("RelatedTopics", [])):
        if len(results) >= limit:
            break
        results.append(
            WebResult(
                title=topic["Text"].split(" - ")[0], url=topic["FirstURL"], snippet=topic["Text"]
            )
        )

    return results[:limit]
