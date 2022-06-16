from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_sensor_feed,
    delete_sensor_feed,
    retrieve_sensor_feed,
    retrieve_sensor_feeds,
    update_sensor_feed,
)
from app.server.models.feed import (
    ErrorResponseModel,
    ResponseModel,
    MachOPSchema,
    UpdateMachOPModel,
)

router = APIRouter()

@router.post("/", response_description="Machine data added into the database")
async def add_sensor_feed_data(feed: MachOPSchema = Body(...)):
    feed = jsonable_encoder(feed)
    new_feed = await add_sensor_feed(feed)
    return ResponseModel(new_feed, "Machine feed added successfully.")

@router.get("/", response_description="Machine retrieved")
async def get_feeds():
    feeds = await retrieve_sensor_feeds()
    if feeds:
        return ResponseModel(feeds, "Machine feed retrieved successfully")
    return ResponseModel(feeds, "Empty list returned")

@router.get("/{id}", response_description="Machine feed retrieved")
async def get_feed_data(id):
    feed = await retrieve_sensor_feed(id)
    if feed:
        return ResponseModel(feed, "Machine feed retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Machine doesn't exist.")

@router.put("/{id}")
async def update_feed_data(id: str, req: UpdateMachOPModel = Body(...)):
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

@router.delete("/{id}", response_description="feed data deleted from the database")
async def delete_sensor_feed_data(id: str):
    deleted_feed = await delete_sensor_feed(id)
    if deleted_feed:
        return ResponseModel(
            "feed with ID: {} removed".format(id), "feed deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "feed with id {0} doesn't exist".format(id)
    )
