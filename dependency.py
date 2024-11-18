from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from fastapi import HTTPException, Header, Depends, status
from models import User

SECRET_KEY: str = "BHiPQkv9shEqy4bfLcxq6Eb3w95fMIoz"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

    
async def get_current_user(token: str | None = Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    if payload is None:
        print("Failed to decode token")
        raise credentials_exception

    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user.id
