from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from .. import schemas
#import models.models as models
from ..models import models as models
from .. import dependencies
import logging

LOGGER = logging.getLogger(__name__)

router = APIRouter()

@router.get("/healthz/", response_model=schemas.healthz)
def show_records(db: Session = Depends(dependencies.get_db)):
    records = db.query(models.healthz).all()
    LOGGER.debug(records[0])
    LOGGER.debug(f'record length: {len(records)}')
    return records[0]
