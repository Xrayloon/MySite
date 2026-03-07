import uuid
from sqlmodel import Field, SQLModel,Relationship

class UserDataBase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nickname: str
    name: str  | None = None
    second_name: str | None = None
    age: int = None
    admin_status: bool = False
    online_status: bool = False 

class UserCreate(UserDataBase):
    password: str



class Items(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | str = Field(min_length=4, max_length=40)
       




