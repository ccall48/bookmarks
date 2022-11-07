from sqlalchemy import Column, Integer, String
# from pydantic import BaseModel
from db.config import Base
from uuid import uuid4


##########
# Helper functions
#
def genuuid() -> str:
    """Generate random uuid for primary key id"""
    return str(uuid4())


##########
# DB table models
#
class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(String, default=genuuid, primary_key=True)
    author = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    url = Column(String, nullable=False)


'''
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    bookmark_id = Column(String, nullable=False)
'''
