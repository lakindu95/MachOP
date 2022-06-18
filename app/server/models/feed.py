from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator
from datetime import datetime, timezone


class FeedModel(BaseModel):
    machine_name: Union[str, None] = None
    machine_id: Union[int, None] = None
    sensor_id: Union[int, None] = None
    is_heater_on: Union[bool, None] = None
    oxygen_level: Optional[int] = None
    humidity_level: Optional[float] = None
    temperature: Optional[float] = None
    moisture_level: Optional[float] = None
    start_date: Union[datetime, None] = None

    class Config:
        schema_extra = {
            "example": {
                "machine_name": "Biowaste_Process_1",
                "machine_id": 112,
                "sensor_id": 13223,
                "is_heater_on": "true",
                "oxygen_level": 2,
                "humidity_level": "3.0",
                "temperature": "36.7",
                "moisture_level": "10",
                "start_date": '2022-06-11T22:31:18.130822+00:00'
                }
        }


class UpdateFeedModel(BaseModel):
    machine_name: Optional[str]
    machine_id : Optional[int]
    sensor_id: Optional[int]
    is_heater_on: Optional[bool]
    oxygen_level: Optional[int]
    humidity_level: Optional[float]
    temperature: Optional[float]
    moisture_level: Optional[float]
    start_date: Optional[datetime]


    class Config:
        schema_extra = {
            "example": {
                "machine_name": "Biowaste_Process_1",
                "sensor_id": 13223,
                "is_heater_on": "true",
                "oxygen_level": 4,
                "humidity_level": "4.0",
                "temperature": "36.7",
                "moisture_level": "10",
                "start_date": '2022-06-16T22:31:18.130822+00:00'
            }
        }