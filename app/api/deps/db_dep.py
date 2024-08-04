from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.db import SessionLocal


def get_db():  # 데이터베이스 세션 관리
    db = SessionLocal()
    try:
        yield db  # 세션 생성
    finally:
        db.close()  # 세션 종료


DatabaseDep = Annotated[Session, Depends(get_db)]
