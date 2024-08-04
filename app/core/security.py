from uuid import uuid4

from passlib.context import CryptContext
import redis

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_client = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)


def get_password_hash(password: str) -> str:
    # 평문 비밀번호 암호화
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 비밀번호 검증 (평문 비밀번호, 암호화 비밀번호 비교)
    return pwd_context.verify(plain_password, hashed_password)


def create_session(user_id: int) -> str:
    # 세션 생성
    session_id = str(uuid4())
    # key: session_id, value: user_id
    redis_client.setex(session_id, settings.SESSION_EXP, user_id)

    return session_id


def get_session(session_id: str) -> int | None:
    # 세션 정보 얻기 (user_id)
    user_id = redis_client.get(session_id)
    return int(user_id) if user_id else None


def delete_session(session_id: str):
    # 세션 삭제
    redis_client.delete(session_id)
