from typing import List, Optional

import uvicorn
from fastapi import FastAPI, status

from db.config import engine, Base, async_session
from db.dals.bookmark_dal import BookmarksDAL
from db.models.bookmarks import Bookmark
from db.models.inputs import CreateInputs, PutInputs, BookmarkID


app = FastAPI(title = 'Bookmarks API')


@app.on_event('startup')
async def startup():
    # create db table/s
    async with engine.begin() as conn:
        if 'bookmarks' not in Base.metadata.tables.keys():
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


##########
# Create a bookmark
#
@app.post('/bookmarks', status_code = status.HTTP_201_CREATED)
async def create_bookmark(data: CreateInputs):
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            await bookmark_dal.create_bookmark(data.author, data.tags, data.url)
            return {'success': 200, 'data': data}


##########
# Return all bookmarks
#
@app.get('/bookmarks', status_code = status.HTTP_200_OK)
async def get_all_bookmarks() -> List[Bookmark]:
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            return await bookmark_dal.get_all_bookmarks()


##########
# Return a bookmark by id
#
@app.get('/bookmark', status_code = status.HTTP_200_OK )
async def get_a_bookmark(data: BookmarkID):
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            return await bookmark_dal.get_a_bookmark(data.id)


##########
# Update a bookmark by id
#
@app.put('/bookmarks', status_code = status.HTTP_200_OK)
async def update_bookmark(data: PutInputs):
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            await bookmark_dal.update_bookmark(data.id, data.author, data.tags, data.url)
            return {'success': 200, 'data': data}


##########
# Delete a bookmark by id
#
@app.delete('/bookmarks')
async def delete_bookmark(data: BookmarkID):
    async with async_session() as session:
        async with session.begin():
            bookmark_dal = BookmarksDAL(session)
            lookup = await bookmark_dal.get_bookmark(data.id)
            """Check bookmark exists before deleting"""
            if lookup:
                await bookmark_dal.delete_bookmark(data.id)
                return {'success': f'{data.id} removed'}
            else:
                return {'error': f'{data.id} does not exist'}


if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=1111, debug=True)
