from fastapi import APIRouter, Depends
from schemas import RequestCreateUser, ResponseUser, Token, UserLogin, RequestUpdateUser
from sqlalchemy.orm import Session
from database import get_db
from crud import crud_create_user, crud_update_user, crud_login_user
from dependency import get_current_user


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
    result = crud_create_user(request, db)
    return result

@router.get(
    "/users",
    # response_model= ???
)
def get_users():
    pass


@router.put(
    "/update-user-name",
)
def update_user(
    request: RequestUpdateUser,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = crud_update_user(current_user_id, request, db)
    return result



@router.post(
    "/login", response_model=Token
)
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    result = crud_login_user(request, db)

    return result
    