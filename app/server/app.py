from fastapi import FastAPI

from app.server.routes.feed import router as FeedRouter
from app.server.routes.authentication import router as AuthRouter
from app.server.routes.machine import router as MachineRouter

app = FastAPI()

app.include_router(FeedRouter, tags=["Sensor"], prefix="/feed")
app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")
app.include_router(MachineRouter, tags=["Machine"], prefix="/machine")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to MachOP app!"}
