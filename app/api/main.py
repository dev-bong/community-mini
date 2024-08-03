from fastapi import APIRouter

from app.api.routes import users, login, boards, posts

api_router = APIRouter()

api_router.include_router(login.router, tags=["로그인"])
api_router.include_router(users.router, prefix="/users", tags=["유저"])
api_router.include_router(boards.router, prefix="/boards", tags=["게시판"])
api_router.include_router(posts.router, prefix="/posts", tags=["게시글"])
