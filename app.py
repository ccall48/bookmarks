from typing import List, Optional

import uvicorn
from fastapi import FastAPI

from db.config import engine, Base, async_session
from db.dals.bookmark_dal import BookmarksDAL
from db.models.bookmarks import Bookmark
from db.models.inputs import CreateInputs, PutInputs, DeleteInputs


app = FastAPI()


@app.on_event('startup')
async def startup():
    # create db table/s
    async with engine.begin() as conn:
        if 'bookmarks' not in Base.metadata.tables.keys():
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


@app.post('/bookmarks')
async def create_bookmark(data: CreateInputs):
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            await bookmark_dal.create_bookmark(data.author, data.category, data.link)
            return {'success': 200, 'data': data}


@app.get('/bookmarks')
async def get_all_bookmarks() -> List[Bookmark]:
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            return await bookmark_dal.get_all_bookmarks()


@app.put('/bookmarks')
async def update_bookmark(data: PutInputs):
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            await bookmark_dal.update_bookmark(data.bookmark_id, data.author, data.category, data.link)
            return {'success': 200, 'data': data}


@app.delete('/bookmarks')
async def delete_bookmark(data: DeleteInputs):
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            lookup = await bookmark_dal.get_bookmark(data.bookmark_id)
            """Check bookmark exists before deleting"""
            if lookup:
                await bookmark_dal.delete_bookmark(data.bookmark_id)
                return {'success': f'bookmark {data.bookmark_id} removed'}
            else:
                return {'error': f'bookmark {data.bookmark_id} does not exist'}


if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=1111, debug=True)
