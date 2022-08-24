from sqlalchemy import asc, desc
from sqlalchemy.orm import Query, Session

from .models import GeoName


def get_item(
        db: Session,
        geo_name_id: int
) -> Query:
    """
    Получить населенный пункт по id (НП).
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
    :param db ссесия базы.
    :param page страница.
    :param limit количество НП на странице.
    """
    return db.query(GeoName).order_by(asc(GeoName.geo_name_id)).offset(
        (page - 1) * limit
    ).limit(limit).all()


def get_count(db: Session) -> int:
    """
    Получить количество записей в БД.
    :param db ссесия базы.
    """
    return db.query(GeoName).count()


def get_city_by_name(
        db: Session,
        city_name: str,
) -> Query:
    """
    Получить населенный пункт (НП) по названию.
    :param db сессия базы.
    :param city_name название НП.
    """
    return db.query(GeoName).filter(
        GeoName.name == city_name
    ).order_by(desc(GeoName.population)).first()


def get_help(
        db: Session,
        help_city: str,
) -> Query:
    """
    Получить предположительные населенные пункты.
    :param db ссесия базы.
    :param help_city: часть наименования
    """
    return db.query(GeoName.name).filter(
        GeoName.name.like(f'{help_city}%')).all()
