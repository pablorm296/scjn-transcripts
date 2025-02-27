from pydantic_settings import BaseSettings, SettingsConfigDict

class CacheConfig(BaseSettings):
    # Redis host, port, and password
    host: str
    port: int
    password: str

    # Cache configuration
    model_config = SettingsConfigDict(
        env_prefix = "CACHE_",
        env_file = ".env.local",
        extra = "ignore"
    )

class MongoConfig(BaseSettings):
    # MongoDB host, port, user, password, and database
    host: str
    port: int
    user: str
    password: str
    database: str

    # Model configuration
    model_config = SettingsConfigDict(
        env_prefix = "MONGO_",
        env_file = ".env.local",
        extra = "ignore"
    )

class CollectorConfig(BaseSettings):
    # Host of the Buscador Jurídico API
    host: str
    # Path to the search endpoint
    path_search: str
    # Path to get the document details
    path_document: str
    # Path to get the print version of the document
    path_print: str

    # Model configuration
    model_config = SettingsConfigDict(
        env_prefix = "EXTRACTOR_",
        env_file = ".env.local",
        extra = "ignore"
    )

class Config(BaseSettings):
    collector: CollectorConfig = CollectorConfig()
    mongo: MongoConfig = MongoConfig()
    cache: CacheConfig = CacheConfig()

    model_config = SettingsConfigDict(
        extra = "ignore"
    )