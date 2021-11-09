from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel


# class sr_all_report(BaseModel):

#     @classmethod
#     def from_orm(cls, obj: Any) -> 'Order':
#         # `obj` is the orm model instance
#         if hasattr(obj, 'billing'):
#             obj.name = obj.billing.first_name
#         return super().from_orm(obj)

# https://stackoverflow.com/questions/64414030/how-to-use-nested-pydantic-models-for-sqlalchemy-in-a-flexible-way



class srevpart(BaseModel):
    srevpartid: int
    eventid: int
    namestring: str
    namerole: str

    class Config:
        orm_mode = True


class srevents(BaseModel):
    # sreventid: int
    siteid: int
    eventid: int
    event_type: str
    event_class: str
    eventdate: Optional[datetime]
    approval_date: Optional[datetime]
    ministry_contact: str
    note: str
    required_action: str
    eventparts: Optional[List[srevpart]]

    class Config:
        orm_mode = True


class srassocs(BaseModel):
    associd: int
    siteid: int
    associatedsiteid: int
    effectdate: datetime
    notestring: str

    class Config:
        orm_mode = True

class srparrol(BaseModel):
    class Config:
        orm_mode = True
    partroleid: int
    participantid: int
    rolestring: str


class srsitpar(BaseModel):
    siteid: int
    participantid: int
    namestring: str
    effectivedate: datetime
    enddate: Optional[datetime]
    notestring: str
    parttype: str
    participantroles: Optional[List[srparrol]]


    class Config:
        orm_mode = True

class srdocpar(BaseModel):
    docparid: int
    docid: int
    namestring: str
    role: str
    class Config:
        orm_mode = True


class srsitdoc(BaseModel):
    siteid: int
    docid: int
    titlestring: str
    submissiondate: datetime
    documentdate: datetime
    notestring: str
    document_participant: List[srdocpar]
    class Config:
        orm_mode = True

class srlands(BaseModel):
    landid: int
    siteid: int
    land_use: str
    notestring: str
    class Config:
        orm_mode = True

class srprfuse(BaseModel):
    landuseid: int
    siteid: int
    dateCompleted: datetime
    land_use_cd: str
    class Config:
        orm_mode = True


class srsites(BaseModel):
    siteid: int
    region: str
    status: str
    common_name: str
    address_1: str
    address_2: str
    city: str
    prov_state: str
    postal_code: str
    lat: int
    latdeg: int
    latmin: int
    latsec: int
    lon: int
    londeg: int
    lonmin: int
    lonsec: int
    victoria_file_no: str
    regional_file_no: str
    classification: str
    gendescr: str
    regdate: datetime
    moddate: datetime
    tombdate: datetime
    events: List[srevents]
    site_participants: List[srsitpar]
    site_docs: List[srsitdoc]
    site_associations: List[srassocs]
    sus_land_use: List[srlands]
    site_profile_use: List[srprfuse]

    class Config:
        orm_mode = True

class srpinpid(BaseModel):
    pinpidid: int
    siteid: int
    pin: Optional[int]
    pidno: int
    crown_lands_file_no: str
    legaldesc: str
    datenoted: datetime
    sites: List[srsites]

    class Config:
        orm_mode = True



