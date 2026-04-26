from pydantic_settings import BaseSettings
import os


class AppSettings(BaseSettings):
   
    APP_NAME: str = "E commerce API"
    ENVIRONMENT: str = "production"

    
    DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
