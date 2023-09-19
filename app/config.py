from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expires: int

    class Config:
        env_file = ".env"


settings = Settings()