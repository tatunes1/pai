from app.config import get_settings
settings = get_settings()

print(f"{settings.es_host} {settings.es_index}")