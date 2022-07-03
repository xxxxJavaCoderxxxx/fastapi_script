from sqlalchemy import Column, Float, Integer, String

from .database import Base


class GeoName(Base):
    __tablename__ = "geoname"

    geo_name_id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True
    )
    name = Column(String)
    ascii_name = Column(String)
    alternate_names = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    feature_class = Column(String)
    feature_code = Column(String)
    country_code = Column(String)
    alt_cc = Column(String)
    admin1_code = Column(String)
    admin2_code = Column(String)
    admin3_code = Column(String)
    admin4_code = Column(String)
    population = Column(Integer)
    elevation = Column(Integer)
    dem = Column(Integer)
    timezone = Column(String)
    modification_date = Column(String)
