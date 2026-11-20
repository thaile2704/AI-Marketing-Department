from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "AI Marketing Department"
    app_env: str = "development"
    database_url: str = "postgresql+asyncpg://marketing:marketing_dev_only@db:5432/marketing"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-5"
    default_model_provider: str = "openai"
    model_timeout_seconds: float = 60.0
    # Optional free-tier proxy (FreeLLMAPI or any OpenAI-compatible endpoint). OFF by default. See docs/adr/0002.
    free_proxy_enabled: bool = False
    free_proxy_base_url: str = "http://host.docker.internal:3001/v1"
    free_proxy_api_key: str | None = None
    free_proxy_model: str = "freellmapi/auto"
    cors_origins: str = "http://localhost:3000"
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_jwks_url: str | None = None
    oidc_org_roles_claim: str = "org_roles"
    dev_auth_enabled: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
