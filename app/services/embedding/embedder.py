from sentence_transformers import SentenceTransformer
from pydantic_settings import BaseSettings
from app.core.config import get_settings

class Embedder:
    settings: BaseSettings
    model: SentenceTransformer | None

    def __init__(self) -> None:
        print("initializing")
        self.settings = get_settings()
        self.model: SentenceTransformer | None = None
        print("initialized")
    
    def _get_model(self) -> SentenceTransformer:
        print("Getting model")
        if self.model is None:
            self.model = SentenceTransformer(self.settings.embed_model)
        return self.model
    
    def embed_text(self, text) -> list[float]:
        print("Getting vector")
        vector = self._get_model().encode(text, normalize_embeddings=True)
        print("got vector")
        return vector.tolist()
    
    def embed_batch(self, texts) -> list[list[float]]:
        vector = self._get_model().encode(texts, normalize_embeddings=True, batch_size=32)
        return vector.tolist()

embedder = Embedder()