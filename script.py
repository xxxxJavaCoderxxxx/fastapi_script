from http import HTTPStatus
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Query, Session
from transliterate import translit

from sql_app import crud, schemas
from sql_app.database import SessionLocal
from sql_app.schemas import ResponseModelItems
from utils import load_db, pages

app = FastAPI(openapi_tags=[
    {
        'name': 'items',
        'description': 'Manage items.',
    },
])

load_db()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/items/{geo_name_id}', response_model=schemas.Item, tags=['items'])
def read_item(geo_name_id: int, db: Session = Depends(get_db)) -> Query:
    db_item = crud.get_item(
        db,
        geo_name_id=geo_name_id
    )
    if db_item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='GeoNameId {} не найден.'.format(geo_name_id)
        )
    return db_item


@app.get('/items', response_model=ResponseModelItems, tags=['items'])
def read_items(
        request: Request,
        page: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> dict:
    db_items = crud.get_items(
        db,
        page=page,
        limit=limit
    )
    response = pages(page, limit, request)
    response['result'] = db_items
    return response


@app.get(
    '/cities',
    response_model=schemas.ResponseModelCities,
    tags=['cities']
)
def read_cities(
        first_city: str,
        second_city: str,
        db: Session = Depends(get_db)
) -> dict:
    first_city = translit(
        first_city,
        'ru',
        reversed=True
    )
    second_city = translit(
        second_city,
        'ru',
        reversed=True
    )

    first_city = crud.get_city_by_name(
        db,
        first_city,
    )
    second_city = crud.get_city_by_name(
        db,
        second_city
    )
    response = {
        'firstCity': first_city,
        'secondCity': second_city
    }
    return response


@app.get('/help', response_model=schemas.ResponseModelHelp, tags=['cities'])
def help_cities(
        city: str,
        db: Session = Depends(get_db)
) -> dict:
    city = translit(
        city,
        'ru',
        reversed=True
    )
    cities = crud.get_help(
        db,
        city
    )
    response = {'cities': list(*zip(*cities))}
    return response
