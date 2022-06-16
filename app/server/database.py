import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.MachOP

feed_collection = database.get_collection("feeds_collection")


# helpers


def feed_helper(feed) -> dict:
    return {
        "id": str(feed["_id"]),
        "machinename": feed["machinename"],
        "email": feed["email"],
        "description": feed["description"],
        "isHeaterOn": feed["isHeaterOn"],
        "oxygenLevel": feed["oxygenLevel"],
        "humidityLevel": feed["humidityLevel"],
        "temperature": feed["temperature"],
        "moistureLevel": feed["moistureLevel"]
    }


# crud operations


# Retrieve all machine feeds present in the database
async def retrieve_sensor_feeds():
    sensor_feeds = []
    async for feed in feed_collection.find():
        sensor_feeds.append(feed_helper(feed))
    return sensor_feeds


# Add a new feeds into to the database
async def add_sensor_feed(feed_data: dict) -> dict:
    feed = await feed_collection.insert_one(feed_data)
    new_feed = await feed_collection.find_one({"_id": feed.inserted_id})
    return feed_helper(new_feed)


# Retrieve a feed with a matching ID
async def retrieve_sensor_feed(id: str) -> dict:
    feed = await feed_collection.find_one({"_id": ObjectId(id)})
    if feed:
        return feed_helper(feed)


# Update a feed with a matching ID
async def update_sensor_feed(id: str, data: dict):
    # Return false if an empty request body is sent.
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
