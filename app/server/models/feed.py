from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class MachOPSchema(BaseModel):
    machinename: str = Field(...)
    email: EmailStr = Field(...)
    description: str = Field(...)
    isHeaterOn: bool = Field(...)
    oxygenLevel: int = Field(..., gt=0, lt=9)
    humidityLevel: float = Field(...)
    temperature: float = Field(...)
    moistureLevel: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "machinename": "John Doe",
                "email": "jdoe@x.edu.ng",
                "description": "Water resources engineering",
                "isHeaterOn": "true",
                "oxygenLevel": 2,
                "humidityLevel": "3.0",
                "temperature": "36.7",
                "moistureLevel": "10"
            }
        }


class UpdateMachOPModel(BaseModel):
    machinename: Optional[str]
    email: Optional[EmailStr]
    description: Optional[str]
    isHeaterOn: Optional[bool]
    oxygenLevel: Optional[int]
    humidityLevel: Optional[float]
    temperature: Optional[float]
    moistureLevel: Optional[float]


    class Config:
        schema_extra = {
            "example": {
                "machinename": "Biowaste_Process_1",
                "email": "jdoe@x.edu.ng",
                "description": "Water resources and environmental engineering",
                "isHeaterOn": "true",
                "oxygenLevel": 4,
                "humidityLevel": "4.0",
                "temperature": "36.7",
                "moistureLevel": "10"
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
