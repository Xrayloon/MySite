from pydantic import BaseModel, ConfigDict, EmailStr, Field



class UserFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str = Field(min_length=4)
    email: EmailStr
    phone_number: str | None

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
