from datetime import date, datetime, timedelta
from os.path import exists

from fastapi import Depends

from pollux.datasource import DataSource, create_datasource
from pollux.settings import Settings
from pollux.stream import background_download, to_csv


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
    # TODO: This function does too much. We're in the FastAPI layer here and
    # should not "initialise" the data with scraping. That's app-logic!

    # We start one week from now to make sure we're up-to-date. Pages are
    # published weekly and the current week may not yet be complete. Fetching
    # from one week in the past "overshoots" a bit but it should only result in
    # at most two requests. Which is acceptable
    if not exists(settings.filename):
        start = datetime.now() - timedelta(weeks=1)
        end = datetime.now()
        to_csv(start.date(), end.date(), settings.filename, cache_folder="")
        background_download(
            date(1996, 1, 1),
            datetime.now().date(),
            settings.filename,
            settings.scraping_cache,
        )
    return create_datasource(settings)
