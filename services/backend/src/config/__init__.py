from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: str

    model_config = SettingsConfigDict(env_prefix='postgres_')


class Settings(BaseSettings):
    logging_level: str = 'INFO'

    database: DatabaseConfig = DatabaseConfig()


settings = Settings()
