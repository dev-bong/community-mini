from starlette.config import Config
from sqlalchemy import URL


class Settings:
    """
    각종 설정 및 상수 관리
    """

    config = Config(".env")  # .env 파일 불러오기

    DB_USER: str = config("DB_USER")
    DB_PASSWORD: str = config("DB_PASSWORD")
    DB_HOST: str = config("DB_HOST")
    DB_DATABASE: str = config("DB_DATABASE")

    def db_url_object(self):
        return URL.create(
            "postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            database=self.DB_DATABASE,
        )


settings = Settings()
