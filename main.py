from fastapi import FastAPI
from route import router
import models
from database import engine

app = FastAPI(
    title="24-2 백엔드 세션"
)

app.include_router(router)

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello World."}
