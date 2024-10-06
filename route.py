from fastapi import APIRouter, HTTPException
from schemas import RequestCreateUser, ResponseUser
from database import users_db

router = APIRouter(
    prefix="/register"
)

@router.post(
    "/"
)
def create_user(
    user: RequestCreateUser,
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
    result = [
        ResponseUser(
            id=user['id'],
            email=user['email'],
            username=user['username']
        ) for user in users_db
    ] 
    #또는 
    """
    result = [
        ResponseUser(
            **user
        ) for user in users_db
    ]
    """
    return result




