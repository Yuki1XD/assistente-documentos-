from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Assistente Inteligente de Documentos"
    app_version: str = "1.0.0"
    database_url: str = "sqlite:///./data/assistente.db"
    max_upload_mb: int = 15
    ai_api_base: str = "https://api.openai.com/v1"
    ai_api_key: str = ""
    ai_model: str = ""
    ai_timeout_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
