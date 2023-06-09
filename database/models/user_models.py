# from pydantic import BaseModel

# class User(BaseModel):
#     id: int | None 
#     username: str
#     email: str

from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    username: str
    email: str