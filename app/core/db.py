from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(settings.db_url_object())

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # ? autocommit=False : 데이터 변경 후 commit()을 해야만 데이터베이스에 적용
