from pydantic import BaseModel, Field

class Books(BaseModel):
    label: str
    author: str
    year: int
    ibsn: str
    value: int

class Readers(BaseModel):
    name: str
    email: str
    comment: str

class Users(BaseModel):
    name: str
    fullname: str
    hashedpassword: str
    email: str
    
class SUserAuth(BaseModel):
    name: str = Field(min_length=3, max_length=10, description="Логин пользователя")
    password: str = Field(min_length=3, max_length=50, description="Пароль, от 5 до 50 знаков")
