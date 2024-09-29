from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import users_db

router = APIRouter(
    prefix="/register"
)

class User(BaseModel):
    id: int | None
    email: str
    username: str
    password: str

@router.post(
    "/"
)
def create_user(
    user: User,
):
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already exitst")

    user.id = len(users_db) + 1
    users_db.append(user.model_dump())
    
    return {"message": "User registered successfully"}

@router.get(
    "/users"
)
def get_users():
    return users_db





