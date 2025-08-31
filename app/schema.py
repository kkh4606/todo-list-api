from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class User(BaseModel):
    email: EmailStr
    password: str


class CreateUser(User):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Todo(BaseModel):
    content: str


class CreateTodo(Todo):
    pass


class UpdateTodo(Todo):
    pass


class TodoOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_completed: bool
    owner_id: int
    owner: UserOut


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str | None] = None
