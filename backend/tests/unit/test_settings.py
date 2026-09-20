from app.core.settings import get_settings


def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("AGENT_ENABLED", raising=False)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.app_name == "engineering-knowledge-assistant"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.agent_enabled is True


def test_settings_reads_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("AGENT_ENABLED", "false")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.environment == "production"
    assert settings.agent_enabled is False


def test_settings_rag_defaults(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("QDRANT_URL", raising=False)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.gemini_api_key == ""
    assert settings.qdrant_url == "http://localhost:6333"
    assert settings.qdrant_collection == "engineering_knowledge"
    assert settings.embedding_dimension == 768


def test_settings_rag_reads_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
    monkeypatch.setenv("QDRANT_URL", "http://qdrant:6333")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.gemini_api_key == "test-key-123"
    assert settings.qdrant_url == "http://qdrant:6333"


def test_settings_work_items_db_path_default(monkeypatch):
    monkeypatch.delenv("WORK_ITEMS_DB_PATH", raising=False)
    get_settings.cache_clear()
    assert get_settings().work_items_db_path == "work_items.db"


def test_settings_work_items_db_path_reads_env(monkeypatch):
    monkeypatch.setenv("WORK_ITEMS_DB_PATH", "/data/items.db")
    get_settings.cache_clear()
    assert get_settings().work_items_db_path == "/data/items.db"
