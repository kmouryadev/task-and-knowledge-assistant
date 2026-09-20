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
