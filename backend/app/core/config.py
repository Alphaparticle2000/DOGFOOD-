from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SUPABASE_JWT_SECRET: str = "Sahil-vro"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()