from typing import Dict

from fastapi import Request
from sqlalchemy import inspect

from sql_app import models, schemas
from sql_app.crud import get_count
from sql_app.database import SessionLocal, engine


def load_db() -> None:
    if not inspect(engine).has_table(models.GeoName.__tablename__):
        db = SessionLocal()
        models.Base.metadata.create_all(bind=engine)
        with open('RU.txt', encoding='utf-8') as data:
            for line in data:
                line = line.strip().split('\t')
                item = models.GeoName(
                    **dict(zip(schemas.ItemBase.__fields__.keys(), line))
                )
                db.add(item)
            db.commit()
        db.close()


def pages(page: int, limit: int, request: Request) -> Dict:
    page = 0 if page < 0 else page
    page = page + 1 if page == 0 else page
    db = SessionLocal()
    count = get_count(db=db)
    db.close()
    next = page + 1 if page * limit < count else None
    previous = page - 1 if 1 <= page - 1 else None
    next_page = request.url.replace_query_params(
        **{'page': next, 'limit': limit}
    )
    previous_page = request.url.replace_query_params(
        **{'page': previous, 'limit': limit}
    )
    return {
        'next': None if next is None else str(next_page),
        'previous': None if previous is None else str(previous_page),
        'result': None,
    }
