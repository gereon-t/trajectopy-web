import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, models
from app.routers import results, sessions, settings, trajectories

logger = logging.getLogger("root")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trajectopy API", version="0.1.0")

logger.info("Starting Trajectopy API")

# Define allowed origins explicitly
allowed_origins = [
    "http://frontend",
    "https://trajectopy.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


app.include_router(trajectories.router)
app.include_router(results.router)
app.include_router(sessions.router)
app.include_router(settings.router)


load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "8000")),
    )
