from pymongo import ASCENDING
from app.database import database
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    email: str
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    message: str
