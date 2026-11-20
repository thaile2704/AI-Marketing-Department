import asyncio
import pytest
from app.core.config import settings
from app.services import model_gateway as gw


@pytest.fixture(autouse=True)
def configured(monkeypatch):
    monkeypatch.setattr(settings, "openai_api_key", "sk-test")
    monkeypatch.setattr(settings, "anthropic_api_key", "sk-ant-test")
    monkeypatch.setattr(settings, "free_proxy_enabled", True)
    monkeypatch.setattr(settings, "free_proxy_api_key", "freellmapi-test")
    monkeypatch.setattr(settings, "default_model_provider", "openai")


def fake(name, fail=False):
    async def _call(prompt):
        if fail:
            raise RuntimeError("boom")
        return {"model": name, "text": f"from {name}", "input_tokens": 3, "output_tokens": 5}
    return _call


def test_free_proxy_used_only_for_public_economy():
    assert gw.plan_route("economy", "public")[0] == "free_proxy"
    assert "free_proxy" not in gw.plan_route("balanced", "public")


@pytest.mark.parametrize("data_class", ["internal", "customer"])
def test_free_proxy_never_sees_non_public_data(data_class):
    assert "free_proxy" not in gw.plan_route("economy", data_class)


def test_free_proxy_off_by_default(monkeypatch):
    monkeypatch.setattr(settings, "free_proxy_enabled", False)
    assert "free_proxy" not in gw.plan_route("economy", "public")


def test_default_data_class_is_not_public(monkeypatch):
    monkeypatch.setitem(gw._CALLERS, "free_proxy", fake("free"))
    monkeypatch.setitem(gw._CALLERS, "openai", fake("openai"))
    out = asyncio.run(gw.generate_text("hi", tier="economy"))
    assert out["provider"] == "openai"


def test_falls_back_and_records_failure(monkeypatch):
    monkeypatch.setitem(gw._CALLERS, "free_proxy", fake("free", fail=True))
    monkeypatch.setitem(gw._CALLERS, "openai", fake("openai"))
    out = asyncio.run(gw.generate_text("hi", tier="economy", data_class="public"))
    assert out["provider"] == "openai"
    assert out["failed_providers"] == [{"provider": "free_proxy", "error": "RuntimeError"}]
    assert out["input_tokens"] == 3 and out["output_tokens"] == 5


def test_all_providers_fail(monkeypatch):
    for p in gw._CALLERS:
        monkeypatch.setitem(gw._CALLERS, p, fake(p, fail=True))
    with pytest.raises(gw.ModelUnavailableError):
        asyncio.run(gw.generate_text("hi", tier="economy", data_class="public"))


def test_no_provider_configured(monkeypatch):
    monkeypatch.setattr(settings, "openai_api_key", None)
    monkeypatch.setattr(settings, "anthropic_api_key", None)
    monkeypatch.setattr(settings, "free_proxy_enabled", False)
    with pytest.raises(gw.ModelConfigurationError):
        asyncio.run(gw.generate_text("hi"))


def test_unknown_tier_or_data_class_rejected():
    with pytest.raises(ValueError):
        gw.plan_route("ultra", "public")
    with pytest.raises(ValueError):
        gw.plan_route("economy", "secret")
