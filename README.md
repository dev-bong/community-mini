# 미니 게시판 프로젝트

### ☝️ 요구사항
<div>
  <img src="https://img.shields.io/badge/python-3.11_|_3.12-blue">
  <img src="https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D">
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white">
</div>

***

### 👩‍💻 설치 및 시작
#### 1. .env 파일 작성 (postgresql, redis)
```
# .env 파일

DB_USER = {USERNAME}
DB_PASSWORD = {PASSWORD}
DB_HOST = {HOSTNAME}
DB_DATABASE = {DATABASENAME}

REDIS_HOST = {HOSTNAME}
```
#### 2. poetry로 패키지 내려받기
```
poetry install
```
#### 3. poetry 가상환경 시작
```
poetry shell
```
#### 4. 서비스 시작
```
python run.py
```
