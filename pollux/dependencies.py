from pollux.datasource import DataSource
from pollux.settings import Settings


def get_settings() -> Settings:
    """
    Create and return the default application settings
    """
    settings = Settings()
    return settings


def get_data_source() -> DataSource:
    """
    Create and return the default data-source
    """
    return DataSource.default()
