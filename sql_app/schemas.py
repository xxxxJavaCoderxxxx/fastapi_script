from datetime import datetime
from http import HTTPStatus
from typing import Any, List

from fastapi import HTTPException
from pydantic import BaseModel, Field, root_validator, validator
from pytz import timezone

from settings import HOUR


class ItemBase(BaseModel):
    geo_name_id: int = Field(alias='geoNameId')
    name: str
    ascii_name: str = Field(alias='asciiName')
    alternate_names: str = Field(alias='alternateNames')
    latitude: float
    longitude: float
    feature_class: str = Field(alias='featureClass')
    feature_code: str = Field(alias='featureCode')
    country_code: str = Field(alias='countryCode')
    alt_cc: str = Field(alias='altCC')
    admin1_code: str = Field(alias='admin1Code')
    admin2_code: str = Field(alias='admin2Code')
    admin3_code: str = Field(alias='admin3Code')
    admin4_code: str = Field(alias='admin4Code')
    population: int
    elevation: str
    dem: str
    timezone: str
    modification_date: str = Field(alias='modificationDate')


class Item(ItemBase):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ResponseModelItems(BaseModel):
    next: str | None
    previous: str | None
    result: List[Item]

    class Config:
        orm_mode = True

        @staticmethod
        def schema_extra(schema: dict[str, Any]) -> None:
            for prop in ('next', 'previous'):
                schema.get('properties')[prop].update({'x-nullable': True})

    @validator('result', always=True)
    def validate_result(cls, value):
        if len(value) == 0:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Населенные пункты не найдены.'
            )
        return value


class ResponseModelCities(BaseModel):
    firstCity: Item | None
    secondCity: Item | None
    northCity: str | None = Field(
        title='Наименование населенного пункта расположенного севернее.'
    )
    timezone: int | None = Field(
        title='Разница во времени между городами.'
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @root_validator
    def validate(cls, values):
        if not any(values.values()):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Города не найдены.'
            )
        if all(values.values()):
            first_city = values.get('firstCity')
            second_city = values.get('secondCity')
            north_city = first_city.name if (
                    first_city.latitude > second_city.latitude
            ) else second_city.name
            values.update({'northCity': north_city})
            current_time = datetime.now()
            first_timezone = timezone(
                first_city.timezone
            ).localize(current_time)
            second_timezone = timezone(
                second_city.timezone
            ).localize(current_time)
            time_diff = int(
                abs(
                    (first_timezone - second_timezone).total_seconds() / HOUR
                )
            )
            values.update({'timezone': time_diff})
        else:
            values.update(
                {
                    'northCity': None,
                    'timezone': None,
                }
            )
        return values


class ResponseModelHelp(BaseModel):
    cities: List[str]
