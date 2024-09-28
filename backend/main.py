import logging
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from config.database import create_db_and_tables
from config.settings import settings
from routes.user import lab_router
from routes.container import container_router
from core.handlers import register_all_errors


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
)
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

register_all_errors(app)
