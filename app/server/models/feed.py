from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, Field

# class UserModel(BaseModel):
#     username: str = Field(...)
#     email: EmailStr = Field(...)
#     full_name: str = Field(...)
#     disabled: bool = Field(...)

class UserModel(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(UserModel):
    hashed_password: str

class TokenModel(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    
class MachOPSchema(BaseModel):
    machine_name: str = Field(...)
    sensor_id: int = Field(...)
    is_heater_on: bool = Field(...)
    oxygen_level: int = Field(..., gt=0, lt=9)
    humidity_level: float = Field(...)
    temperature: float = Field(...)
    moisture_level: float = Field(...)
    start_date: datetime = Field(...) 

    class Config:
        schema_extra = {
            "example": {
                "machine_name": "Biowaste_Process_1",
                "sensor_id": 13223,
                "is_heater_on": "true",
                "oxygen_level": 2,
                "humidity_level": "3.0",
                "temperature": "36.7",
                "moisture_level": "10",
                "start_date": '2022-06-16T22:31:18.130822+00:00'    
                }
        }


class UpdateMachOPModel(BaseModel):
    machine_name: Optional[str]
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


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
