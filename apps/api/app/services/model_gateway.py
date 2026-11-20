from app.core.config import settings
class ModelConfigurationError(RuntimeError): pass
async def generate_text(prompt: str, tier: str = "balanced") -> dict:
    """Minimal provider adapter. Extend with retries, usage accounting and structured outputs."""
    provider = settings.default_model_provider.lower()
    if provider == "openai":
        if not settings.openai_api_key: raise ModelConfigurationError("OPENAI_API_KEY is not configured")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.responses.create(model=settings.openai_model, input=prompt)
        return {"provider": "openai", "model": settings.openai_model, "text": response.output_text}
    if provider == "anthropic":
        if not settings.anthropic_api_key: raise ModelConfigurationError("ANTHROPIC_API_KEY is not configured")
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        response = await client.messages.create(model=settings.anthropic_model, max_tokens=3000, messages=[{"role":"user","content":prompt}])
        text = "\n".join(block.text for block in response.content if getattr(block, "type", None) == "text")
        return {"provider":"anthropic", "model":settings.anthropic_model, "text":text}
    raise ModelConfigurationError(f"Unsupported provider: {provider}")
