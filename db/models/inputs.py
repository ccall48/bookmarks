from typing import Optional
from pydantic import BaseModel


class CreateInputs(BaseModel):
    author: str
    category: str
    link: str


class PutInputs(BaseModel):
    bookmark_id: int
    author: Optional[str] = None
    category: Optional[str] = None
    link: Optional[str] = None


class DeleteInputs(BaseModel):
    bookmark_id: int
