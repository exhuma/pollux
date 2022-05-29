from fastapi import Depends

from pollux.datasource import DataSource, create_datasource
from pollux.settings import Settings


def get_settings() -> Settings:
    """
    Create and return the default application settings
    """
    settings = Settings()
    return settings


def get_data_source(settings: Settings = Depends(get_settings)) -> DataSource:
    """
    Create and return the default data-source
    """
    return create_datasource(settings)
