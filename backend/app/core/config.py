import secrets
from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict  

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
    )
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 * 24 * 6 = 6 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 6 


    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()

