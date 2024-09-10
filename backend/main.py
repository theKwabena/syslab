from fastapi import FastAPI
from config.database import create_db_and_tables
from routes.user import lab_router
from routes.container import container_router

app = FastAPI()
app.include_router(lab_router)
app.include_router(container_router)


@app.on_event("startup")
def on_startup():
    print("Creating DB Tables")
    create_db_and_tables()
