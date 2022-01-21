from typing import Optional
from pydantic import BaseModel


##########
# Create inputs
#
class CreateInputs(BaseModel):
    author: str
    tags: str
    url: str


##########
# Put inputs
#
class PutInputs(BaseModel):
    id: str
    author: Optional[str] = None
    tags: Optional[str] = None
    url: Optional[str] = None


##########
# Find Bookmark by ID
#
class BookmarkID(BaseModel):
    id: str
