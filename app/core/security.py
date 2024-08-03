from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    # 평문 비밀번호 암호화
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 비밀번호 검증 (평문 비밀번호, 암호화 비밀번호 비교)
    return pwd_context.verify(plain_password, hashed_password)
