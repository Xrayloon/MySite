from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserPrivate(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=150)
    phone_number: str | None = Field(default=None)
    first_name: str | None = Field(default=None, min_length=2, max_length=20)
    second_name: str | None = Field(default=None, max_length=20)
    
class UserCreate(BaseModel):
    username: str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    username: str = Field(default=None, min_length=4)
    email: EmailStr = Field(default=None)
    password: str = Field(min_length=8)

class Token(BaseModel):
    access_token: str
    Token_type: str
