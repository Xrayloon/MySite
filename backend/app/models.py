from pydantic import BaseModel, ConfigDict, EmailStr, Field



class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(min_length=4, max_length=25)



class register_user(User):

    email: EmailStr
    password: str = Field(min_length=8)


