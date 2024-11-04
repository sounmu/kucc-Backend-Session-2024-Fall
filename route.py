from fastapi import APIRouter, Depends
from schemas import RequestCreateUser, ResponseUser
from sqlalchemy.orm import Session
from database import get_db
from crud import crud_create_user


router = APIRouter(
    prefix="/auth"
)

@router.post(
    "/",
    response_model=ResponseUser
)
def create_user(
    request: RequestCreateUser,
    db: Session = Depends(get_db)
):  
    user = crud_create_user(request, db)
    return user

@router.get(
    "/users",
    # response_model= ???
)
def get_users():
    pass


@router.put(
    "/"
)
def update_user():
    pass



