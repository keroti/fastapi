from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings(
    database_hostname="shutterlink.postgres.database.azure.com",
    database_port="5432",
    database_password=f"{os.environ.get('database_password')}",
    database_name="fastapi",
    database_username="keroti",
    secret_key=f"{os.environ.get('secret_key')}",
    algorithm="HS256",
    access_token_expire_minutes=60,
)
