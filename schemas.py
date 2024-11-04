from pydantic import BaseModel, Field, EmailStr

class RequestCreateUser(BaseModel):
    id: int | None = Field(example=1, gt=0)
    email: EmailStr
    user_name: str = Field(min_length=2, max_length=20)
    password: str
    

class ResponseUser(BaseModel):
    id: int = Field(gt=0)
    email: EmailStr
    user_name: str = Field(min_length=2, max_length=20)


class ReqeustUpdateUser(BaseModel):
    pass