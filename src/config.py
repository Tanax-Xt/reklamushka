"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "prod-second-25" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-second-25

Modifications made by Danila Sedelnikov on February 2025.
"""

from pydantic import DirectoryPath, NewPath, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

GeneratedPath = NewPath | DirectoryPath


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "root"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "db"
    POSTGRES_DATABASE: str = "prod3"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    DATE_PREFIX: str = "current_date"
    MODERATION_PREFIX: str = "moderation"

    MINIO_ADDRESS: str = "s3-storage:9000"
    MINIO_PUBLIC_ADDRESS: str = "http://localhost:9000"
    MINIO_ROOT_USER: str = "root"
    MINIO_ROOT_PASSWORD: str = "password"
    MINIO_BUCKET_NAME: str = "files-bucket"

    @computed_field
    @property
    def POSTGRES_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE,
        )

    @computed_field
    @property
    def POSTGRES_TEST_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path="test",
        )


settings = Settings()
