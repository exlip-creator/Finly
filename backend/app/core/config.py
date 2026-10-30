from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True
    )

    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    db_host: str
    db_port: int = Field(ge=1, le=65535)

    app_name: str = "Finly API"


settings = Settings()