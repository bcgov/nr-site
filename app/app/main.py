from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse


from . import schemas
from .models import models
from .routers import site_associations, sites, pin_pid, healthz

from .database import SessionLocal, engine
import logging

# engine = sqlalchemy.create_engine(
#    DATABASE_URL, connect_args={"check_same_thread": False}
# )

# metadata.create_all(engine)

# TODO: move to a config log file
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
hndlr = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s"
)
hndlr.setFormatter(formatter)
LOGGER.addHandler(hndlr)
LOGGER.debug("first test message")


LOGGER = logging.getLogger(__name__)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


app.include_router(site_associations.router)
app.include_router(sites.router)
app.include_router(pin_pid.router)
app.include_router(healthz.router)
