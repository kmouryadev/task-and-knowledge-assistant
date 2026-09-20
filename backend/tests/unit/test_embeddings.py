from unittest.mock import patch

import pytest

from app.rag.embeddings import EmbeddingClient


def test_embed_texts_calls_gemini_per_text_and_returns_vectors():
    fake_response = {"embedding": [0.1, 0.2, 0.3]}
    with patch("app.rag.embeddings.genai.embed_content", return_value=fake_response) as mock_embed:
        client = EmbeddingClient(api_key="fake-key")
        vectors = client.embed_texts(["hello world", "second text"])

    assert vectors == [[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]
    assert mock_embed.call_count == 2
    _, kwargs = mock_embed.call_args
    assert kwargs["task_type"] == "retrieval_document"
    assert kwargs["output_dimensionality"] == 768


def test_embed_query_uses_retrieval_query_task_type():
    fake_response = {"embedding": [0.4, 0.5, 0.6]}
    with patch("app.rag.embeddings.genai.embed_content", return_value=fake_response) as mock_embed:
        client = EmbeddingClient(api_key="fake-key")
        vector = client.embed_query("what is the checkout flow?")

    assert vector == [0.4, 0.5, 0.6]
    _, kwargs = mock_embed.call_args
    assert kwargs["task_type"] == "retrieval_query"


def test_embed_texts_rejects_empty_list():
    client = EmbeddingClient(api_key="fake-key")
    with pytest.raises(ValueError):
        client.embed_texts([])
