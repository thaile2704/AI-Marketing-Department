from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "AI Marketing Department"
    app_env: str = "development"
    database_url: str = "sqlite+aiosqlite:///./marketing.db"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-5"
    default_model_provider: str = "openai"
    cors_origins: str = "http://localhost:3000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
