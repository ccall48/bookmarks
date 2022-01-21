from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.bookmarks import Bookmark


##########
# Bookmarks Data Access Layer
#
class BookmarksDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session


    async def create_bookmark(self, author: str, tags: str, url: str):
        """Create a new bookmark"""
        new_bookmark = Bookmark(author=author, tags=tags, url=url)
        self.db_session.add(new_bookmark)
        await self.db_session.flush()


    async def get_all_bookmarks(self) -> List[Bookmark]:
        """Return all bookmarks in collection"""
        query = await self.db_session.execute(select(Bookmark).order_by(Bookmark.id))
        return query.scalars().all()


    async def get_a_bookmark(self, id: str):
        """Return one bookmark if exists"""
        query = await self.db_session.execute(select(Bookmark).where(Bookmark.id == id))
        return query.scalars().all()


    async def update_bookmark(
        self,
        id: str,
        author: Optional[str],
        tags: Optional[str],
        url: Optional[str]
    ):
        """Update a bookmark by id"""
        query = update(Bookmark).where(Bookmark.id == id)
        if author:
            query = query.values(author=author)
        if tags:
            query = query.values(tags=tags)
        if url:
            query = query.values(url=url)
        query.execution_options(synchronize_session='fetch')
        await self.db_session.execute(query)


    async def delete_bookmark(self, id: str):
        """Delete a bookmark by id"""
        query = delete(Bookmark).where(Bookmark.id == id)
        await self.db_session.execute(query)
