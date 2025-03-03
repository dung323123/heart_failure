from pydantic import BaseModel
from typing import Optional

class Account(BaseModel):
    id: str
    email: str
    username: str
    password: str

