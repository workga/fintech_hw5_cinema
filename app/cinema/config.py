from pydantic import BaseSettings


class CinemaSettings(BaseSettings):
    page_size: int

    class Config:
        env_file = 'app/cinema/.env'
        env_file_encoding = 'utf-8'


cinema_settings = CinemaSettings()
