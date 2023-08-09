from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    host: str = Field("localhost", alias="DB_HOST")
    port: int = Field(5432, alias="DB_PORT")
    user: str = Field("username", alias="DB_USER")
    password: str = Field("password", alias="DB_PASS")
    name: str = Field("database", alias="DB_NAME")

    def __init__(self):
        super().__init__()
        self.url: str = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    jwt_secret_key: str = Field("secret_key", alias="SECRET_KEY")
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()


settings = Settings()
