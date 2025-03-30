from app.app_2.persistences.minio_file_storage_service import MinioFileStorageService
from pydantic_settings import BaseSettings, SettingsConfigDict

object_storage_service = MinioFileStorageService()
authentication_url = "0.0.0.0"


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PSQL_DB_")
    database: str
    username: str
    password: str
    host: str
    port: str


postgres_settings = PostgresSettings()

DATABASE_URL = "postgres://{}:{}@{}:{}/{}".format(
    postgres_settings.username,
    postgres_settings.password,
    postgres_settings.host,
    postgres_settings.port,
    postgres_settings.database,
)

models = ["app.authentication.models", "aerich.models"]
