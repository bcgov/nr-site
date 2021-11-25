from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
#import models.models as models
from ..models import models
from .. import dependencies
#
from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
import logging

LOGGER = logging.getLogger(__name__)

router = APIRouter()

#@router.get("/sites/default", response_model=Page[schemas.srsites])
@router.get("/sites", response_model=LimitOffsetPage[schemas.srsites])
def show_records(db: Session = Depends(dependencies.get_db)):
    #records =
    #LOGGER.debug(records[0])
    #LOGGER.debug(f'record length: {len(records)}')
    return paginate(db.query(models.srsites))



add_pagination(router)