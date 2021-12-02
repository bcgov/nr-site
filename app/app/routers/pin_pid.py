from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
#import models.models as models
from ..models import models
from .. import dependencies
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from .. import crud
import logging

LOGGER = logging.getLogger(__name__)

router = APIRouter()
# doesn't inlcude related tables
@router.get("/pinpid", response_model=LimitOffsetPage[schemas.srpinpid_nr])
def show_records(db: Session = Depends(dependencies.get_db)):
    return paginate(db.query(models.srpinpid_nr))

# currently includes relationships... possibly want to only include pinpid table data.
@router.get("/pinpid/{pidno}", response_model=schemas.srpinpid)
def read_pinpid(pidno: int, db: Session = Depends(dependencies.get_db)):
    pidrec = crud.get_pinpid(db, pidno=pidno)
    if pidrec is None:
        raise HTTPException(status_code=404, detail="User not found")
    return pidrec

@router.get("/pinpid/{pidno}/site", response_model=List[schemas.srsites])
def read_pinpidsite(pidno: int, db: Session = Depends(dependencies.get_db)):
    pidrec = crud.get_site(db, pidno=pidno)
    if pidrec is None:
        raise HTTPException(status_code=404, detail="User not found")
    return pidrec

#response_model=List[schemas.sr-all-report]  ,,
@router.get("/pinpid/{pidno}/all_report",  response_model=List[schemas.srpinpid])
def read_pinpidsite(pidno: int, db: Session = Depends(dependencies.get_db)):
    pidrec = crud.get_allReportData(db, pidno=pidno)
    if pidrec is None:
        raise HTTPException(status_code=404, detail="User not found")
    LOGGER.debug(f"pidrec: {pidrec}")

    return pidrec




add_pagination(router)