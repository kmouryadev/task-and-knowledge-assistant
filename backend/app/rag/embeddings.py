import google.generativeai as genai

_MODEL = "models/text-embedding-004"


class EmbeddingClient:
    def __init__(self, api_key: str):
        self._api_key = api_key
        genai.configure(api_key=api_key)

    def embed_texts(
        self, texts: list[str], task_type: str = "retrieval_document"
    ) -> list[list[float]]:
        if not texts:
            raise ValueError("texts must not be empty")
        return [
            genai.embed_content(model=_MODEL, content=text, task_type=task_type)["embedding"]
            for text in texts
        ]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_texts([text], task_type="retrieval_query")[0]
