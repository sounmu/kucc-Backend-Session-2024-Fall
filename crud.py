from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
from schemas import RequestCreateUser, RequestUpdateUser, UserLogin
from passlib.context import CryptContext
from dependency import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def crud_login_user(request: UserLogin, db: Session):
    stmt = select(User).where(User.email == request.email)
    try:
        user = db.execute(stmt).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User no found")

        if not verify_password(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


def crud_get_user(user_id: int, db: Session):
    stmt = select(User).where(User.id == user_id)
    try:
        user = db.execute(stmt).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User no found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
        )
    
    return user


def crud_get_users(db: Session):
    pass


def crud_create_user(request: RequestCreateUser, db: Session):
    user = User(
        email = request.email,
        user_name = request.user_name,
        password = hash_password(request.password)
    )

    try:
        db.add(user)
        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Integrity Error occurred during create the new user. {str(e)}") from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Unexpected error occurred: {str(e)}") from e
    else:
        db.commit()
        db.refresh(user)
        return user
    
def crud_update_user(current_user_id: int, request: RequestUpdateUser, db: Session):
    if current_user_id is not request.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User id does not match with the request id")
    
    stmt = select(User).where(User.id == current_user_id)
    try:
        user = db.execute(stmt).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.user_name = request.user_name
        db.commit()
        db.refresh(user)
        return user

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}"
        )