from sqlalchemy import asc, desc
from sqlalchemy.orm import Query, Session

from .models import GeoName


def get_item(
        db: Session,
        geo_name_id: int
) -> Query:
    """
    Получить населенный пункт (НП).
    :param db это база.
    :param geo_name_id номер НП.
    """
    return db.query(GeoName).filter(
        GeoName.geo_name_id == geo_name_id
    ).first()


def get_items(
        db: Session,
        page: int = 0,
        limit: int = 10
) -> Query:
    """
    Получить населенные пункты (НП).
    :param db это база.
    :param page страница.
    :param limit количество НП на странице.
    """
    return db.query(GeoName).order_by(asc(GeoName.geo_name_id)).offset(
        (page - 1) * limit
    ).limit(limit).all()


def get_count(db: Session) -> int:
    """
    Получить количество записей в БД.
    :param db это база.
    """
    return db.query(GeoName).count()


def get_cities(
        db: Session,
        first_city: str,
        second_city: str,

) -> dict:
    """
    Получить населенные пункты по названию.
    :param db это база.
    :param first_city город 1.
    :param second_city город 2.
    """

    first_city = db.query(GeoName).filter(
        GeoName.name == first_city
    ).order_by(desc(GeoName.population)).first()
    second_city = db.query(GeoName).filter(
        GeoName.name == second_city
    ).order_by(desc(GeoName.population)).first()

    response = {
        'firstCity': first_city,
        'secondCity': second_city
    }
    return response


def get_help(
        db: Session,
        help_city: str,

) -> dict:
    """
    Получить населенные пункты по названию.
    :param help_city: часть наименования
    :param db это база.
    """
    cities = db.query(GeoName.name).filter(
        GeoName.name.like('{}%'.format(help_city))
    ).all()
    return {'cities': list(*zip(*cities))}
