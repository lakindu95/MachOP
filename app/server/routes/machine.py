from fastapi.security import OAuth2PasswordBearer

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from app.server.models.machine import (
    MachineModel,
    MachineInDB
)

from app.server.auth.auth import (
    get_current_active_user
)

from app.server.database import (
    add_machine_user
)

from app.server.models.common import (
    ResponseModel
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Get current machine details
@router.get("/current/", response_model=MachineModel,)
async def read_users_me(token: str = Depends(oauth2_scheme), current_user: MachineModel = Depends(get_current_active_user)):
    return current_user


# Register a new machine user
@router.post("/register", response_description="Machine user added into the database")
async def add_machine_user_data(token: str = Depends(oauth2_scheme), feed: MachineInDB = Body(...)):
    feed = jsonable_encoder(feed)
    new_feed = await add_machine_user(feed)
    return ResponseModel(new_feed, "Machine user added successfully.")
