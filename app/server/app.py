from fastapi import FastAPI

from app.server.routes.feed import router as FeedRouter

app = FastAPI()

app.include_router(FeedRouter, tags=["Sensor"], prefix="/feed")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to MachOP app!"}
