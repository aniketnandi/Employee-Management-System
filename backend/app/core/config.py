import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings, read from environment variables (or a local .env file)."""

    def __init__(self) -> None:
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ems.db")
        self.secret_key: str = os.getenv("SECRET_KEY", "dev-only-insecure-secret-change-me")
        self.algorithm: str = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        self.cors_origins: list[str] = [
            o.strip()
            for o in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
            if o.strip()
        ]
        # When enabled, an admin account and sample data are created on first startup.
        self.seed_demo_data: bool = os.getenv("SEED_DEMO_DATA", "false").lower() in ("1", "true", "yes")
        self.demo_admin_username: str = os.getenv("DEMO_ADMIN_USERNAME", "admin")
        self.demo_admin_password: str = os.getenv("DEMO_ADMIN_PASSWORD", "admin123")


settings = Settings()
