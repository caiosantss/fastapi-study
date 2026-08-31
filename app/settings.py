from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class SQLiteSettings(BaseModel):
    host: str
    port: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    sqlite: SQLiteSettings
    DATABASE_URL: str

print(Settings())
