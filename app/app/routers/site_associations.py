from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Page, add_pagination, LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate

from .. import schemas
#import models.models as models
from ..models import models as models
from .. import dependencies
import logging

LOGGER = logging.getLogger(__name__)

router = APIRouter()
# useful link on pagination: https://github.com/uriyyo/fastapi-pagination/blob/main/examples/pagination_sqlalchemy.py

@router.get("/srassocs", response_model=LimitOffsetPage[schemas.srassocs])
def show_records(db: Session=Depends(dependencies.get_db)):
    return paginate(db.query(models.srassocs))

add_pagination(router)

