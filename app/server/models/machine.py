from typing import Union
from pydantic import BaseModel

class MachineModel(BaseModel):
    username: str
    machine_name: Union[str, None] = None
    machine_id: Union[str, None] = None
    disabled: Union[bool, None] = None

class Config:
    schema_extra = {
        "example": {
            "username": "machine1",
            "machine_name": "Biowaste_Process_1",
            "machine_id": 13223,
            "disabled": 'true',
            }
    }

class MachineInDB(MachineModel):
    hashed_password: str
