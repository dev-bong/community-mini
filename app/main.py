from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router

app = FastAPI(title="게시판 API 서버", version="0.0.1")

# 허용 origin 목록
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://zzz.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # 쿠키 지원
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(api_router)
