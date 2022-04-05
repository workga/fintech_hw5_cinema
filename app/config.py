from pydantic import BaseSettings


class AppSettings(BaseSettings):
    db_url: str
    db_url_testing: str
    logger_name: str
    logger_level: str

    class Config:
        env_file = 'app/.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
