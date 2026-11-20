"""Model gateway: tier-aware routing, provider fallback and token metering.

Providers
- openai, anthropic: approved paid providers (ADR-0001).
- free_proxy: optional OpenAI-compatible free-tier aggregator (ADR-0002). OFF by default.

Safety rule: the free-tier proxy is used ONLY when the caller marks the request
data_class="public" AND tier="economy". Free tiers may log prompts and generally
forbid production use, so internal/customer data never goes there.
"""
from __future__ import annotations

import logging
import time

from app.core.config import settings

log = logging.getLogger(__name__)

TIERS = {"economy", "balanced", "premium"}
DATA_CLASSES = {"public", "internal", "customer"}
PAID_PROVIDERS = ("openai", "anthropic")


class ModelConfigurationError(RuntimeError):
    """No usable provider is configured for this request."""


class ModelUnavailableError(RuntimeError):
    """Every eligible provider failed."""


def _configured(provider: str) -> bool:
    if provider == "openai":
        return bool(settings.openai_api_key)
    if provider == "anthropic":
        return bool(settings.anthropic_api_key)
    if provider == "free_proxy":
        return bool(settings.free_proxy_enabled and settings.free_proxy_api_key)
    return False


def plan_route(tier: str, data_class: str) -> list[str]:
    """Ordered list of configured providers eligible for this request."""
    if tier not in TIERS:
        raise ValueError(f"Unknown tier: {tier}")
    if data_class not in DATA_CLASSES:
        raise ValueError(f"Unknown data_class: {data_class}")
    preferred = settings.default_model_provider.lower()
    paid = [p for p in [preferred, *PAID_PROVIDERS] if p in PAID_PROVIDERS]
    paid = list(dict.fromkeys(paid))
    order: list[str] = []
    if tier == "economy" and data_class == "public":
        order.append("free_proxy")
    order.extend(paid)
    return [p for p in order if _configured(p)]


async def _call_openai(prompt: str) -> dict:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=settings.model_timeout_seconds)
    r = await client.responses.create(model=settings.openai_model, input=prompt)
    u = getattr(r, "usage", None)
    return {"model": settings.openai_model, "text": r.output_text,
            "input_tokens": getattr(u, "input_tokens", 0) or 0, "output_tokens": getattr(u, "output_tokens", 0) or 0}


async def _call_anthropic(prompt: str) -> dict:
    from anthropic import AsyncAnthropic
    client = AsyncAnthropic(api_key=settings.anthropic_api_key, timeout=settings.model_timeout_seconds)
    r = await client.messages.create(model=settings.anthropic_model, max_tokens=3000,
                                     messages=[{"role": "user", "content": prompt}])
    text = "\n".join(b.text for b in r.content if getattr(b, "type", None) == "text")
    u = getattr(r, "usage", None)
    return {"model": settings.anthropic_model, "text": text,
            "input_tokens": getattr(u, "input_tokens", 0) or 0, "output_tokens": getattr(u, "output_tokens", 0) or 0}


async def _call_free_proxy(prompt: str) -> dict:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(base_url=settings.free_proxy_base_url, api_key=settings.free_proxy_api_key,
                         timeout=settings.model_timeout_seconds)
    r = await client.chat.completions.create(model=settings.free_proxy_model,
                                             messages=[{"role": "user", "content": prompt}])
    u = getattr(r, "usage", None)
    return {"model": getattr(r, "model", None) or settings.free_proxy_model,
            "text": r.choices[0].message.content or "",
            "input_tokens": getattr(u, "prompt_tokens", 0) or 0, "output_tokens": getattr(u, "completion_tokens", 0) or 0}


_CALLERS = {"openai": _call_openai, "anthropic": _call_anthropic, "free_proxy": _call_free_proxy}


async def generate_text(prompt: str, tier: str = "balanced", data_class: str = "internal") -> dict:
    """Generate text. Returns provider, model, text, token usage, latency and any failed providers.

    data_class defaults to "internal", so nothing reaches the free-tier proxy unless
    the caller deliberately passes data_class="public".
    """
    route = plan_route(tier, data_class)
    if not route:
        raise ModelConfigurationError("No model provider is configured for this request (check API keys / FREE_PROXY_*).")
    failures: list[dict] = []
    for provider in route:
        started = time.monotonic()
        try:
            out = await _CALLERS[provider](prompt)
        except Exception as exc:  # log class only: messages can echo prompts or keys
            failures.append({"provider": provider, "error": type(exc).__name__})
            log.warning("model provider %s failed: %s", provider, type(exc).__name__)
            continue
        out.update(provider=provider, tier=tier, data_class=data_class,
                   latency_ms=int((time.monotonic() - started) * 1000), failed_providers=failures)
        return out
    raise ModelUnavailableError(f"All eligible providers failed: {failures}")
