from pydantic_settings import BaseSettings, SettingsConfigDict

class CollectorConfig(BaseSettings):
    # Host of the Buscador Jurídico API
    host: str
    # Path to the search endpoint
    path_search: str

    # Model configuration
    model_config = SettingsConfigDict(
        env_prefix = "EXTRACTOR_"
    )

class Config(BaseSettings):
    extractor: CollectorConfig = CollectorConfig()