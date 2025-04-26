from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    logging_level: str = 'INFO'
    api_token: str


settings = Settings()
