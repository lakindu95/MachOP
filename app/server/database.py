import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
from datetime import datetime
import logging

MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
logger = logging.getLogger("uvicorn.error")

database = client.MachOP

feed_collection = database.get_collection("feeds_collection")
user_machine_collection = database.get_collection("user_machine_collection")

# helpers
def feed_helper(feed) -> dict:
    return {
        "id": str(feed["_id"]),
        "machine_name": feed["machine_name"],
        "machine_id": feed["machine_id"],
        "sensor_id": feed["sensor_id"],
        "is_heater_on": feed["is_heater_on"],
        "oxygen_level": feed["oxygen_level"],
        "humidity_level": feed["humidity_level"],
        "temperature": feed["temperature"],
        "moisture_level": feed["moisture_level"],
        "start_date": feed["start_date"]
    }

def machine_user_helper(machine_user) -> dict:
    return {
        "id": str(machine_user["_id"]),
        "username": machine_user["username"],
        "machine_name": machine_user["machine_name"],
        "machine_id": machine_user["machine_id"],
        "disabled": machine_user["disabled"]
    }

def machine_user_helper_db(machine_user) -> dict:
    return {
        "id": str(machine_user["_id"]),
        "username": machine_user["username"],
        "machine_name": machine_user["machine_name"],
        "machine_id": machine_user["machine_id"],
        "disabled": machine_user["disabled"],
       "hashed_password": machine_user["hashed_password"]
    }

# crud operations


# Retrieve all machine feeds present in the database
async def retrieve_sensor_feeds():
    sensor_feeds = []
    async for feed in feed_collection.find():
        sensor_feeds.append(feed_helper(feed))
    return sensor_feeds


# Retrieve all machine feeds by start date
async def retrieve_sensor_feeds_by_start_date(start_date: datetime) :
    sensor_feeds_by_start_date = []
    async for feed in feed_collection.find({"start_date": start_date}):
        sensor_feeds_by_start_date.append(feed_helper(feed))
    return sensor_feeds_by_start_date


# Retreive all machine feeds by sensor ID
async def retrieve_sensor_feed_by_sensor_id(sensor_id: int) :
    logger.error(sensor_id)
    sensor_feeds_by_sensor_id = []
    async for feed in feed_collection.find({"sensor_id": int(sensor_id)}):
        logger.error(feed)
        sensor_feeds_by_sensor_id.append(feed_helper(feed))
    return sensor_feeds_by_sensor_id


# Add a new feeds into to the database
async def add_sensor_feed(feed_data: dict) -> dict:
    feed = await feed_collection.insert_one(feed_data)
    new_feed = await feed_collection.find_one({"_id": feed.inserted_id})
    return feed_helper(new_feed)


# Update a feed with a matching ID
async def update_sensor_feed(id: str, data: dict):
    if len(data) < 1:
        return False
    feed = await feed_collection.find_one({"_id": ObjectId(id)})
    if feed:
        updated_feed = await feed_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_feed:
            return True
        return False


# Delete a feed from the database
async def delete_sensor_feed(id: str):
    feed = await feed_collection.find_one({"_id": ObjectId(id)})
    if feed:
        await feed_collection.delete_one({"_id": ObjectId(id)})
        return True


# Add Machine user data
async def add_machine_user(user_data: dict) -> dict:
    machine_user = await user_machine_collection.insert_one(user_data)
    new_machine_user = await user_machine_collection.find_one({"_id": machine_user.inserted_id})
    return machine_user_helper(new_machine_user)


# Retrieve a machine user with a matching ID
async def retrieve_machine_user(username: str) -> dict:
    machine_user = await user_machine_collection.find_one({"username": username})
    if machine_user:
        return machine_user_helper_db(machine_user)
