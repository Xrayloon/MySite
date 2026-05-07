from pydantic import BaseModel, ConfigDict, EmailStr, Field



class UserFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str = Field(min_length=4, max_length=25)
    email: EmailStr
    phone_number: str | None

class UserCreate(BaseModel):
    username: str = Field(min_length=6)
    email: EmailStr
    password: str = Field(min_length=8)


