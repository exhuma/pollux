from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str = "secret"
    auth_file: str = "users.json"
    upload_folder: str = "uploads"

    # Limit files to 16 MBs
    max_content_length: int = 16 * 1024 * 1024

    #: The CSV file containing our data
    filename: str = "data.csv"

    #: Local storage of scraped data-files
    scraping_cache: str = "cache"
