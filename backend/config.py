from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "StudyHero"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    # API Keys
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str = ""
    GOOGLE_CLOUD_VISION_API_KEY: str = ""

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    # OCR Settings
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    MAX_IMAGE_SIZE_MB: int = 10

    # Rate Limiting
    FREE_TIER_DAILY_LIMIT: int = 5
    PREMIUM_TIER_DAILY_LIMIT: int = 999999

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:8081"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
