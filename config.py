from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    POSTGRES_USER: str = Field()
    POSTGRES_PASSWORD: str = Field()
    POSTGRES_HOST: str = Field()
    POSTGRES_PORT: int = Field()
    POSTGRES_DATABASE: str = Field()

    @property
    def postgresql_url(self) -> str:
        return (f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}")

    @property
    def async_postgresql_url(self) -> str:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}")

    class Config:
        env_file = ".env"


settings = Settings()

engine = create_engine(settings.postgresql_url, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)