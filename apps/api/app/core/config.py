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
    cors_origins: str = "http://localhost:3000"
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_jwks_url: str | None = None
    oidc_org_roles_claim: str = "org_roles"
    dev_auth_enabled: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
