from sqlalchemy import Column, Integer, String, Date, MetaData, Table
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship

# from .database import Base
from app.database import Base


# class Record(Base):
#     __tablename__ = "Records"

#     id = Column(Integer, primary_key=True, index=True)
#     date = Column(Date)
#     country = Column(String(255), index=True)
#     cases = Column(Integer)
#     deaths = Column(Integer)
#     recoveries = Column(Integer)


metadata = MetaData()

t_srpinpid = Table(
    "srpinpid",
    metadata,
    Column("pinpidid", Integer, primary_key=True),
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("pin", Integer),
    Column("pidno", Integer),
    Column("crown_lands_file_no", String),
    Column("legaldesc", String),
    Column("datenoted", DateTime),
)


class srpinpid(Base):
    __table__ = t_srpinpid
    sites = relationship("srsites", back_populates="pinpids", uselist=True)


t_srassocs = Table(
    "srassocs",
    metadata,
    Column("associd", Integer, primary_key=True),
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("associatedsiteid", Integer),
    Column("effectdate", DateTime),
    Column("notestring", String),
)


class srassocs(Base):
    __table__ = t_srassocs
    sites = relationship("srsites", back_populates="site_associations", uselist=True)


t_srlands = Table(
    "srlands",
    metadata,
    Column("landid", Integer, primary_key=True),
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("land_use", String),
    Column("notestring", String),
)


class srlands(Base):
    __table__ = t_srlands
    sites = relationship("srsites", back_populates="sus_land_use", uselist=True)


t_srprfuse = Table(
    "srprfuse",
    metadata,
    Column("landuseid", Integer, primary_key=True),
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("dateCompleted", DateTime),
    Column("land_use_cd", String),
    Column("land_use_description", String),
)


class srprfuse(Base):
    __table__ = t_srprfuse
    sites = relationship("srsites", back_populates="site_profile_use", uselist=True)

t_srprofil = Table(
    "srprofil",
    metadata,
    Column("profileid", Integer, primary_key=True),
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("datecompleted", DateTime),
    Column("ownerid", Integer),
    Column("contactid", Integer),
    Column("completorid", Integer),
    Column("dateReceived", DateTime),
    Column("dateLocalAuthority", DateTime),
    Column("dateRegistrar", DateTime),
    Column("dateDecision", DateTime),
    Column("dateEntered", DateTime),
    Column("decisionText", String),
    Column("commentString", String),
    Column("plannedActivityComment", String),
    Column("siteDisclosureComment", String),
    Column("govDocumentsComment", String),
    Column("localAuthEmail", String),
)


class srprofil(Base):
    __table__ = t_srprofil
    sites = relationship("srsites", back_populates="site_profile", uselist=True)



t_srsites = Table(
    "srsites",
    metadata,
    Column("siteid", Integer, primary_key=True),
    Column("region", String),
    Column("status", String),
    Column("common_name", String),
    Column("address_1", String),
    Column("address_2", String),
    Column("city", String),
    Column("prov_state", String),
    Column("postal_code", String),
    Column("lat", Integer),
    Column("latdeg", Integer),
    Column("latmin", Integer),
    Column("latsec", Integer),
    Column("lon", Integer),
    Column("londeg", Integer),
    Column("lonmin", Integer),
    Column("lonsec", Integer),
    Column("victoria_file_no", String),
    Column("regional_file_no", String),
    Column("classification", String),
    Column("gendescr", String),
    Column("regdate", DateTime),
    Column("moddate", DateTime),
    Column("tombdate", DateTime),
)


class srsites(Base):
    __table__ = t_srsites
    pinpids = relationship("srpinpid", back_populates="sites", uselist=True)
    events = relationship("srevents", back_populates="sites", uselist=True)
    site_participants = relationship("srsitpar", back_populates="sites", uselist=True)
    site_docs = relationship("srsitdoc", back_populates="sites", uselist=True)
    site_associations = relationship("srassocs", back_populates="sites", uselist=True)
    sus_land_use = relationship("srlands", back_populates="sites", uselist=True)
    site_profile_use = relationship("srprfuse", back_populates="sites", uselist=True)
    site_profile = relationship("srprofil", back_populates="sites", uselist=True)


t_srsitpar = Table(
    "srsitpar",
    metadata,
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("participantid", Integer, primary_key=True),
    Column("namestring", String),
    Column("effectivedate", DateTime),
    Column("enddate", DateTime),
    Column("notestring", String),
    Column("parttype", String),
)


class srsitpar(Base):
    __table__ = t_srsitpar
    sites = relationship("srsites", back_populates="site_participants", uselist=True)
    participantroles = relationship(
        "srparrol", back_populates="site_participants", uselist=True
    )


t_srparrol = Table(
    "srparrol",
    metadata,
    Column("partroleid", Integer, primary_key=True),
    Column("participantid", Integer, ForeignKey("srsitpar.participantid")),
    Column("rolestring", String),
)


class srparrol(Base):
    __table__ = t_srparrol
    site_participants = relationship(
        "srsitpar", back_populates="participantroles", uselist=True
    )


t_srevents = Table(
    "srevents",
    metadata,
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("eventid", Integer, primary_key=True),
    Column("event_type", String),
    Column("event_class", String),
    Column("eventdate", DateTime),
    Column("approval_date", DateTime),
    Column("ministry_contact", String),
    Column("note", String),
    Column("required_action", String),
)
# ,UniqueConstraint('eventid', name='eventid_unique')


class srevents(Base):
    __table__ = t_srevents
    sites = relationship("srsites", back_populates="events", uselist=True)
    eventparts = relationship("srevpart", back_populates="events", uselist=True)


t_srevpart = Table(
    "srevpart",
    metadata,
    Column("srevpartid", Integer, primary_key=True),
    Column("eventid", Integer, ForeignKey("srevents.eventid")),
    Column("namestring", String),
    Column("namerole", String),
)


class srevpart(Base):
    __table__ = t_srevpart
    events = relationship("srevents", back_populates="eventparts", uselist=True)


# class srassocs(Base):
#     __tablename__ = "srassocs"
#     associd = Column(Integer, primary_key=True)
#     siteid = Column(Integer)
#     associatedsiteid = Column(Integer)
#     effectdate = Column(String)
#     notestring = Column(String)


t_srdate = Table(
    "srdate",
    metadata,
    Column("downloaddate", String),
    Column("dateid", Integer, primary_key=True),
)

# create declarative base obj from table
# more info:
# https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#mapping-declaratively-with-reflected-tables


class srdate(Base):
    __table__ = t_srdate


t_srsitdoc = Table(
    "srsitdoc",
    metadata,
    Column("siteid", Integer, ForeignKey("srsites.siteid")),
    Column("docid", Integer, primary_key=True),
    Column("titlestring", String),
    Column("submissiondate", DateTime),
    Column("documentdate", DateTime),
    Column("notestring", String),
)


class srsitdoc(Base):
    __table__ = t_srsitdoc
    sites = relationship("srsites", back_populates="site_docs", uselist=True)
    document_participant = relationship(
        "srdocpar", back_populates="documents", uselist=True
    )


t_srdocpar = Table(
    "srdocpar",
    metadata,
    Column("docparid", Integer, primary_key=True),
    Column("docid", Integer, ForeignKey("srsitdoc.docid")),
    Column("namestring", String),
    Column("role", String),
)


class srdocpar(Base):
    __table__ = t_srdocpar
    documents = relationship(
        srsitdoc, back_populates="document_participant", uselist=True
    )


t_srprfans = Table(
    "srprfans",
    metadata,
    Column("srprfanid", Integer, primary_key=True),
    Column("siteid", Integer),
    Column("questionid", Integer),
    Column("date_completed", DateTime),
    Column("answer", String),
)


class srprfans(Base):
    __table__ = t_srprfans


t_srprfcat = Table(
    "srprfcat",
    metadata,
    Column("catid", Integer, primary_key=True),
    Column("sequenceno", Integer),
    Column("effectivedate", DateTime),
    Column("expirydate", DateTime),
    Column("question_type", String),
    Column("descr", String),
    Column("category_precursor", String),
)


class srprfcat(Base):
    __table__ = t_srprfcat


t_srprfque = Table(
    "srprfque",
    metadata,
    Column("questionid", Integer, primary_key=True),
    Column("sequenceno", Integer),
    Column("catid", Integer),
    Column("parentid", Integer),
    Column("effectivedate", DateTime),
    Column("expirydate", DateTime),
    Column("descr", String),
)


class srprfque(Base):
    __table__ = t_srprfque






# t_srprfuse = Table(
#     "srprfuse",
#     metadata,
#     Column("landuseid", Integer, primary_key=True),
#     Column("siteid", Integer),
#     Column("dateCompleted", DateTime),
#     Column("land_use_cd", String),
# )


# class srprfuse(Base):
#     __table__ = t_srprfuse
