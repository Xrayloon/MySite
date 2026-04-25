from pydantic import BaseModel, ConfigDict, Field
"""
Field - добавление ограничений, длины, значений и тд
BaseModel - Основа для наших моделей
ConfigDict  
"""

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)

class PostCreate(PostBase):
    pass 


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) 
    """
    этот флаг нужен, чтобы Pydantic-схемы могли напрямую принимать ORM-объекты,
    извлекая из них нужные поля без ручного преобразования в словари
    B итоге post["title"] -> post.title что упрощает взаимодействие c orm 
    """
    id: int
    date_posted: str

