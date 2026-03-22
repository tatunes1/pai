from app.services.embedding.embedder import embedder

vector = embedder.embed_text("my query")
print(f"vector: {vector}")