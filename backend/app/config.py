from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_url: str = "postgresql+asyncpg://ims_user:ims_pass@localhost:5433/ims_db"
    mongo_url: str = "mongodb://localhost:27017"
    redis_url: str = "redis://localhost:6379"

settings = Settings()