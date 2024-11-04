from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
from schemas import RequestCreateUser, ReqeustUpdateUser


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
        id = request.id,
        email = request.email,
        user_name = request.user_name,
        password = request.password
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
    
def crud_update_user(user_id: int, request: ReqeustUpdateUser, db: Session):
    pass