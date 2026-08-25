"""
Tests for configuration settings and catalog.
"""

from octo_harness.config import Settings, get_settings
from octo_harness.models import ModelCapability, ProviderType, RoutingStrategy


def test_default_settings():
    settings = Settings()
    assert settings.app_name == "Octo Harness - Cowork & Grok AI Router"
    assert settings.version == "1.0.0"
    assert settings.default_strategy == RoutingStrategy.GROK_PRIMARY
    assert "grok-3" in settings.model_catalog
    assert "gpt-4o" in settings.model_catalog
    assert "claude-3-5-sonnet-20241022" in settings.model_catalog


def test_model_catalog_capabilities():
    settings = Settings()
    grok3 = settings.model_catalog["grok-3"]
    assert grok3.provider_type == ProviderType.GROK
    assert ModelCapability.REASONING in grok3.capabilities
    assert ModelCapability.CODE in grok3.capabilities
    assert grok3.context_window >= 128000


def test_get_settings_cached():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
