from datetime import datetime
from http import HTTPStatus
from typing import Any, List

from fastapi import HTTPException
from pydantic import BaseModel, Field, root_validator, validator
from pytz import timezone

from settings import HOUR


class ItemBase(BaseModel):
    geo_name_id: int
    name: str
    ascii_name: str
    alternate_names: str
    latitude: float
    longitude: float
    feature_class: str
    feature_code: str
    country_code: str
    alt_cc: str
    admin1_code: str
    admin2_code: str
    admin3_code: str
    admin4_code: str
    population: int
    elevation: str
    dem: str
    timezone: str
    modification_date: str


class Item(ItemBase):
    class Config:
        orm_mode = True


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
    firstCity: Item | None = Field(
        title='Данные населенного пункта 1.'
    )
    secondCity: Item | None = Field(
        title='Данные населенного пункта 2.'
    )
    northCity: str | None = Field(
        title='Наименование населенного пункта расположенного севернее.'
    )
    timezone: int | None = Field(
        title='Разница во времени между городами.'
    )

    class Config:
        orm_mode = True

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
