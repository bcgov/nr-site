from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel


class srevpart(BaseModel):
    srevpartid: int
    eventid: int
    namestring: str
    namerole: str

    class Config:
        orm_mode = True

class srevents(BaseModel):
    #sreventid: int
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

    class Config:
       orm_mode = True


class srpinpid(BaseModel):
    pinpidid: int
    siteid: int
    pin:  Optional[int]
    pidno: int
    crown_lands_file_no:  str
    legaldesc: str
    datenoted: datetime
    sites: List[srsites]

    class Config:
       orm_mode = True




# class sr_all_report(BaseModel):

#     @classmethod
#     def from_orm(cls, obj: Any) -> 'Order':
#         # `obj` is the orm model instance
#         if hasattr(obj, 'billing'):
#             obj.name = obj.billing.first_name
#         return super().from_orm(obj)

# https://stackoverflow.com/questions/64414030/how-to-use-nested-pydantic-models-for-sqlalchemy-in-a-flexible-way