"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


# Area schemas
class AreaBase(BaseModel):
    name: str


class AreaCreate(AreaBase):
    pass


class AreaUpdate(AreaBase):
    pass


class Area(AreaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Degree schemas
class DegreeBase(BaseModel):
    name: str


class DegreeCreate(DegreeBase):
    pass


class DegreeUpdate(DegreeBase):
    pass


class Degree(DegreeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Student schemas
class StudentBase(BaseModel):
    phone_number: str
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    phone_number: Optional[str] = None
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# EducatorLicense schemas
class EducatorLicenseBase(BaseModel):
    registration_number: Optional[str] = None
    issuing_authority: Optional[str] = None


class EducatorLicenseCreate(EducatorLicenseBase):
    pass


class EducatorLicense(EducatorLicenseBase):
    id: int
    educator_id: int
    model_config = ConfigDict(from_attributes=True)


# EducatorDegree schemas
class EducatorDegreeBase(BaseModel):
    degree_id: int


class EducatorDegreeCreate(EducatorDegreeBase):
    pass


class EducatorDegree(EducatorDegreeBase):
    id: int
    educator_id: int
    model_config = ConfigDict(from_attributes=True)


# EducatorArea schemas
class EducatorAreaBase(BaseModel):
    area_id: int


class EducatorAreaCreate(EducatorAreaBase):
    pass


class EducatorArea(EducatorAreaBase):
    id: int
    educator_id: int
    model_config = ConfigDict(from_attributes=True)


# Educator schemas
class EducatorBase(BaseModel):
    phone_number: str
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_licensed: bool = False


class EducatorCreate(EducatorBase):
    pass


class EducatorUpdate(BaseModel):
    phone_number: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_licensed: Optional[bool] = None


class Educator(EducatorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# CallRequest schemas
class CallRequestBase(BaseModel):
    educator_id: int
    student_id: int


class CallRequestCreate(CallRequestBase):
    pass


class CallRequest(CallRequestBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
