from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Interview Server"
    DEBUG: bool = False
    API_V1_STR: str = "/v1"

    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    LOG_LEVEL: str = "info"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
