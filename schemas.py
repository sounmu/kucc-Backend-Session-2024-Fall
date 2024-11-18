from pydantic import BaseModel, Field, EmailStr

class RequestCreateUser(BaseModel):
    email: EmailStr
    user_name: str = Field(min_length=2, max_length=20)
    password: str
    

class ResponseUser(BaseModel):
    id: int = Field(gt=0)
    email: EmailStr
    user_name: str = Field(min_length=2, max_length=20)

class RequestUpdateUser(BaseModel):
    id: int = Field(gt=0)
    user_name: str = Field(min_length=2, max_length=20)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
