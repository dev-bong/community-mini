"""
명령어 uvicorn app.main:app --reload 대용
명령어 python run.py 이용 가능
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)