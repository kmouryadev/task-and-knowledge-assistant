import google.generativeai as genai

_MODEL = "models/gemini-embedding-001"


class EmbeddingClient:
    def __init__(self, api_key: str, output_dimensionality: int = 768):
        self._api_key = api_key
        self._output_dimensionality = output_dimensionality
        genai.configure(api_key=api_key)

    def embed_texts(
        self, texts: list[str], task_type: str = "retrieval_document"
    ) -> list[list[float]]:
        if not texts:
            raise ValueError("texts must not be empty")
        return [
            genai.embed_content(
                model=_MODEL,
                content=text,
                task_type=task_type,
                output_dimensionality=self._output_dimensionality,
            )["embedding"]
            for text in texts
        ]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_texts([text], task_type="retrieval_query")[0]
