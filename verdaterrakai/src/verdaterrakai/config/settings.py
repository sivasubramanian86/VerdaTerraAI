from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_cloud_project: str = "local-dev-project"
    gcp_region: str = "us-central1"
    alloydb_uri: str = "sqlite:///verdaterra.db"
    api_key: str = "local-dev-api-key"
    
    log_level: str = "INFO"
    environment: str = "development"
    local_dev_mode: bool = True  # Toggles MCP python stubbing vs HTTP transport

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()


