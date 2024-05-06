import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, models
from app.routers import results, sessions, settings, trajectories

logger = logging.getLogger("root")


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        logger.info(f"Request: {request.method} {request.url}")
        return await call_next(request)
    except Exception as e:
        logger.error(e)
        return Response("Internal server error", status_code=500)


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Trajectopy API", version="0.1.0", redoc_url=None, docs_url=None)


logger.info("Starting Trajectopy API")

allowed_origins = ["http://frontend", "http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
app.middleware("http")(catch_exceptions_middleware)


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
