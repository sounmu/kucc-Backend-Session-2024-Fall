from fastapi import FastAPI
from route import router

app = FastAPI(
    title="24-2 백엔드 세션"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello World."}


