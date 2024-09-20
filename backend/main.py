from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.database import create_db_and_tables
from config.settings import settings
from routes.user import lab_router
from routes.container import container_router

app = FastAPI()
app.include_router(lab_router)
app.include_router(container_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def on_startup():
    print("Creating DB Tables")
    create_db_and_tables()
