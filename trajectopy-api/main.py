import logging
import os

import uvicorn
from app.middlewares import catch_exceptions_middleware
from app.repository import engine, models
from app.router import results, sessions, settings, trajectories
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(
    format="%(levelname)-8s %(asctime)s.%(msecs)03d - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Trajectopy API", version="0.1.0", redoc_url=None)

app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

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


@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_file = os.path.join("frontend", "build", "index.html")
    return FileResponse(index_file)


def main():
    load_dotenv()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "8000")),
    )


if __name__ == "__main__":
    main()
