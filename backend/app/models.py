import phonenumbers

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated, Union
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

E164NumberType = Annotated[Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format='E164')] # https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#normal-usage

class UserPrivate(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    phone_number: E164NumberType | None = None
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
