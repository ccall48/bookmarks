from sqlalchemy import Column, Integer, String
#from pydantic import BaseModel
from db.config import Base


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False)
    link = Column(String, nullable=False)
