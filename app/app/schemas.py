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
    note: Optional[str]
    required_action: Optional[str]
    eventparts: Optional[List[srevpart]]

    class Config:
        orm_mode = True


class srassocs(BaseModel):
    associd: int
    siteid: int
    associatedsiteid: int
    effectdate: datetime
    notestring: Optional[str]

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
    notestring: Optional[str]
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
    notestring: Optional[str]
    document_participant: List[srdocpar]
    class Config:
        orm_mode = True

class srlands(BaseModel):
    landid: int
    siteid: int
    land_use: str
    notestring: Optional[str]
    class Config:
        orm_mode = True

class srprfuse(BaseModel):
    landuseid: int
    siteid: int
    dateCompleted: datetime
    land_use_cd: str
    land_use_description: str
    class Config:
        orm_mode = True

class srprfcat(BaseModel):
    class Config:
        orm_mode = True
    catid: int
    sequenceno: int
    effectivedate: Optional[datetime]
    expirydate: Optional[datetime]
    question_type: str
    descr: str
    category_precursor: str

class srprfque(BaseModel):
    class Config:
        orm_mode = True

    questionid: int
    sequenceno: int
    catid: int
    parentid: Optional[int]
    effectivedate: Optional[datetime]
    expirydate: Optional[datetime]
    descr: str
    question_category: List[srprfcat]

class srprfans(BaseModel):
    class Config:
        orm_mode = True
    srprfanid: int
    siteid: int
    questionid: int
    date_completed: datetime
    answer: str
    questions: Optional[List[srprfque]]




class srprofil(BaseModel):
    profileid: int
    siteid: int
    datecompleted: datetime
    ownerid: int
    contactid: int
    completorid: int
    dateReceived: datetime
    dateLocalAuthority: datetime
    dateRegistrar: Optional[datetime]
    dateDecision: datetime
    dateEntered: Optional[datetime]
    decisionText: str
    commentString: str
    plannedActivityComment: Optional[str]
    siteDisclosureComment: Optional[str]
    govDocumentsComment: Optional[str]
    localAuthEmail: Optional[str]

    class Config:
        orm_mode = True

class srsites(BaseModel):
    siteid: int
    region: str
    status: str
    common_name: str
    address_1: str
    address_2: Optional[str]
    city: str
    prov_state: str
    postal_code: Optional[str]
    lat: int
    latdeg: int
    latmin: int
    latsec: int
    lon: int
    londeg: int
    lonmin: int
    lonsec: int
    victoria_file_no: Optional[str]
    regional_file_no: Optional[str]
    classification: str
    gendescr: Optional[str]
    regdate: datetime
    moddate: datetime
    tombdate: datetime
    events: List[srevents]
    site_participants: List[srsitpar]
    site_docs: List[srsitdoc]
    site_associations: List[srassocs]
    sus_land_use: List[srlands]
    site_profile_use: List[srprfuse]
    site_profile: List[srprofil]
    site_answers: List[srprfans]

    class Config:
        orm_mode = True

class srpinpid(BaseModel):
    pinpidid: int
    siteid: int
    pin: Optional[int]
    pidno: int
    crown_lands_file_no: Optional[str]
    legaldesc: str
    datenoted: datetime
    sites: List[srsites]

    class Config:
        orm_mode = True

class srpinpid_nr(BaseModel):
    pinpidid: int
    siteid: int
    pin: Optional[int]
    pidno: int
    crown_lands_file_no: Optional[str]
    legaldesc: str
    datenoted: datetime

    class Config:
        orm_mode = True


class healthz(BaseModel):
    class Config:
        orm_mode = True
    healthz_pk: int
    healthz: str

