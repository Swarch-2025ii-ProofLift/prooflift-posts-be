from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "ProofLift - Posting Service"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int = 5432
    DB_DRIVERNAME: str = "postgresql+psycopg"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    MQ_HOST: str
    MQ_PORT: int = 5672
    MQ_USER: str
    MQ_PASSWORD: str
    MQ_QUEUE: str = "notifications_queue"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()