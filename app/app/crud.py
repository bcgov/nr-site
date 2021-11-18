from sqlalchemy.orm import Session, Load


# from app import models

from . import schemas
import models.models as models
import logging
LOGGER = logging.getLogger(__name__)


def get_pinpid(db: Session, pidno: int):
    results = db.query(models.srpinpid).filter(models.srpinpid.pidno == pidno).first()
    LOGGER.debug(f'pinpid results: {results}')
    return results

def get_site(db: Session, pidno: int):
    # models.srpinpid
    srsites = models.srsites
    columns = srsites.__table__.c
    LOGGER.debug(f"columns : {columns}")
    query = db.query(models.srsites).filter(
        models.srpinpid.siteid == models.srsites.siteid
    ).filter(
        models.srpinpid.pidno == pidno
    )

    results = query.all()
    LOGGER.debug(f"records: {len(results)}")
    LOGGER.debug(f"records: {results}")

    return query.all()

def get_allReportData(db: Session, pidno: int):
    # query = db.query(models.srpinpid).filter(
    #     models.srpinpid.siteid == models.srsites.siteid
    # ).filter(
    #     models.srevents.siteid == models.srpinpid.siteid
    # ).filter(
    #     models.srpinpid.pidno == pidno
    # )
    query = db.query(models.srpinpid).filter(
        models.srpinpid.pidno == pidno
    ).all()
    LOGGER.debug(f'query: {query}')
    return query


#def get_user_by_email(db: Session, email: str):
#    return db.query(models.User).filter(models.User.email == email).first()


def get_pinpids(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.srpinpid).offset(skip).limit(limit).all()



# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item