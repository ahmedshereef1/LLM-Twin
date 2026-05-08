from pydantic import BaseSettings, SettingsConfigDict
from loguru import logger

from zenml import Client


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # AWS Sagemaker
    HF_MODEL_ID: str = "mlabonne/TwinLlama-3.1-8B-DPO"

    @classmethod
    def load_settings(cls) -> "Settings":
        """
        load the settings from ZenML secret store,  If the secret does not exist, it initializes the settings from the .env file and default values.

        Returns:
            Settings: The initialized settings object.
        """
        try:
            logger.info("Loading settings from ZenML secret store...")

            settings_secrets = Client().get_secret("settings")
            settings = Settings(**settings_secrets)
        except (RuntimeError, KeyError):
            logger.warning(
                "Failed to load settings from the ZenML secret store. Defaulting to loading the settings from the '.env' file."
            )
            settings = Settings()

        return settings


settings = Settings.load_settings()
