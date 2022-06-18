from datetime import datetime, timedelta
from typing import Union
import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from decouple import config

from app.server.models.machine import MachineModel

ACCESS_TOKEN_EXPIRE_MINUTES = 30

logger = logging.getLogger("uvicorn.error")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from app.server.database import (
    add_sensor_feed,
    delete_sensor_feed,
    retrieve_sensor_feed_by_sensor_id,
    retrieve_sensor_feeds,
    retrieve_sensor_feeds_by_start_date,
    update_sensor_feed
)
from app.server.models.feed import (
    FeedModel,
    UpdateFeedModel
)
from app.server.models.common import (
    ErrorResponseModel,
    ResponseModel
)
router = APIRouter()


# Add machine feed
@router.post("/", response_description="Machine feed data added into the database")
async def add_sensor_feed_data(token: str = Depends(oauth2_scheme), feed: FeedModel = Body(...)):
    feed = jsonable_encoder(feed)
    new_feed = await add_sensor_feed(feed)
    return ResponseModel(new_feed, "Machine feed added successfully.")


# Get all feeds
@router.get("/", response_description="Machine feeds retrieved")
async def get_feeds(token: str = Depends(oauth2_scheme)):
    feeds = await retrieve_sensor_feeds()
    if feeds:
        return ResponseModel(feeds, "Machine feeds retrieved successfully")
    return ResponseModel(feeds, "No feeds available")


# Get feeds by start date time
@router.get("/startdate/{start_date}", response_description="Feeds retrieved on start date")
async def get_feeds_by_start_date(start_date, token: str = Depends(oauth2_scheme)):
    feeds = await retrieve_sensor_feeds_by_start_date(start_date)
    if feeds:
        return ResponseModel(feeds, "Machine feed retrieved successfully")
    return ResponseModel(feeds, "No feeds available")


# Get feeds by sensor ID
@router.get("/sensorid/{sensor_id}", response_description="Machine feed by Sensor ID retrieved")
async def get_feed_data(sensor_id, token: str = Depends(oauth2_scheme)):
    feed = await retrieve_sensor_feed_by_sensor_id(sensor_id)
    if feed:
        return ResponseModel(feed, "Machine feed by ID retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Machine feed doesn't exist.")


# Update machine feed data by ID
@router.put("/{id}")
async def update_feed_data(id: str, req: UpdateFeedModel = Body(...), token: str = Depends(oauth2_scheme)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_feed = await update_sensor_feed(id, req)
    if updated_feed:
        return ResponseModel(
            "Machine with ID: {} name update is successful".format(id),
            "Machine feed updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the machine feed.",
    )


# Delete machine feed data by ID 
@router.delete("/{id}", response_description="feed data deleted from the database")
async def delete_sensor_feed_data(id: str, token: str = Depends(oauth2_scheme),):
    deleted_feed = await delete_sensor_feed(id)
    if deleted_feed:
        return ResponseModel(
            "feed with ID: {} removed".format(id), "feed deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "feed with id {0} doesn't exist".format(id)
    )
