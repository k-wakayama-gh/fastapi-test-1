from typing import Optional, List
from fastapi import FastAPI, Request, HTTPException, Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from flask import session
from sqlmodel import SQLModel, Session, select
import uvicorn
from database import create_database, engine, get_db

from models import ItemOut, ItemUpdate, Items, ItemCreate

app = FastAPI()

app.mount('/assets', StaticFiles(directory='assets'), name='static')
templates = Jinja2Templates(directory='templates')



@app.on_event('startup')
def startup():
    create_database()



@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('index.html', context)





@app.post('/items', status_code=201, response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    item = Items(**item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
        




@app.get('/items', response_model=List[ItemOut])
def get_items(
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    search: Optional[int] = None,
):
    with Session(engine) as db:
        query = db.query(Items)
        if search:
            query = query.filter(Items.name.contains(search))
        if min_price:
            query = query.filter(Items.price >= min_price)
        if max_price:
            query = query.filter(Items.name <= max_price)
        return query.all()




@app.get('/items/{item_id}', response_model=ItemOut)
def get_item(item_id: int):
    with Session(engine) as db:
        item = db.query(Items).get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail='Item not found')
        return item



@app.put('/items/{item_id}', response_model=ItemOut)
def update_item(item_id: int, item: ItemUpdate):
    with Session(engine) as db:
        db_item = db.query(Items).get(item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail='item not found')
        item = item.dict(exclude_unset=True)
        for key in item:
            setattr(db_item, key, item[key])
        db.commit()
        db.refresh
        return db_item



@app.delete('items/{item_id}')
def delete_item(item_id: int):
    with Session(engine) as db:
        item = db.query(Items).get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail='Item not found')
        db.delete(item)
        db.commit()
        return {'message', 'Item deleted'}








@app.get('/users', response_class=HTMLResponse)
def index(request: Request):
    context = {
        'request': request,
    }
    pass


@app.get('/users/{user_id}', response_class=HTMLResponse)
async def index(request: Request, user_id: int):
    context = {
        'request': request,
        'user_id': user_id,
    }
    return templates.TemplateResponse('users.html', context)


# @app.get('/items/{item_id}', response_class=HTMLResponse)
# async def items(request: Request, item_id: str):
#     context ={
#         'request': request,
#         'item_id': item_id,
#     }
#     return templates.TemplateResponse('items.html', context)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
