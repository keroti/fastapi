from pydantic_settings import BaseSettings


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
    database_password="@99kigan",
    database_name="fastapi",
    database_username="keroti",
    secret_key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    algorithm="HS256",
    access_token_expire_minutes=60,
)
