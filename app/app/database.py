import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

LOGGER  = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN")
if 'POSTGRESQL_USER' in os.environ:
    usr = os.environ['POSTGRESQL_USER']
    pss = os.environ['POSTGRESQL_PASSWORD']
    db = os.environ['POSTGRESQL_DATABASE']
    host = '0.0.0.0'
    if 'POSTGRESQL_HOST' in os.environ:
        host = os.environ['POSTGRESQL_HOST']
    dbport = 5432
    if 'POSTGRES_PORT' in  os.environ:
        dbport = os.environ['POSTGRES_PORT']
    #SQLALCHEMY_DATABASE_URL = f'postgresql+pg8000://{usr}:{pss}@127.0.0.1:5432/{db}'
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{usr}:{pss}@127.0.0.1:{dbport}/{db}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
