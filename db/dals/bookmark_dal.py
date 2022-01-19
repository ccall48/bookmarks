from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.bookmarks import Bookmark


class BookmarksDAL():
    '''Bookmark Data Access Layer'''
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_bookmark(self, author: str, category: str, link: str):
        """Create a new bookmark"""
        new_bookmark = Bookmark(author=author, category=category, link=link)
        self.db_session.add(new_bookmark)
        await self.db_session.flush()


    async def get_all_bookmarks(self) -> List[Bookmark]:
        """Return all bookmarks"""
        query = await self.db_session.execute(select(Bookmark).order_by(Bookmark.id))
        return query.scalars().all()


    async def get_bookmark(self, bookmark_id: int):
        """Return one bookmark or check if exists"""
        query = await self.db_session.execute(select(Bookmark).where(Bookmark.id == bookmark_id))
        return query.scalars().all()


    async def update_bookmark(
        self,
        bookmark_id: int,
        author: Optional[str],
        category: Optional[str],
        link: Optional[str]
    ):
        """Update a bookmark"""
        query = update(Bookmark).where(Bookmark.id == bookmark_id)
        if author:
            query = query.values(author=author)
        if category:
            query = query.values(category=category)
        if link:
            query = query.values(link=link)
        query.execution_options(synchronize_session='fetch')
        await self.db_session.execute(query)


    async def delete_bookmark(self, bookmark_id: int):
        """Delete a bookmark"""
        query = delete(Bookmark).where(Bookmark.id == bookmark_id)
        await self.db_session.execute(query)
