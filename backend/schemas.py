from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# User
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

# Organization
class OrganizationBase(BaseModel):
    name: str
    website: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
    class Config:
        from_attributes = True

# Certification
class CertificationBase(BaseModel):
    name: str
    organization_id: int

class CertificationCreate(CertificationBase):
    pass

class CertificationResponse(CertificationBase):
    id: int
    class Config:
        from_attributes = True

# User Certification
class UserCertificationBase(BaseModel):
    user_id: int
    certification_id: int
    issue_date: date
    expiry_date: date
    credential_url: Optional[str] = None

class UserCertificationCreate(UserCertificationBase):
    pass

class UserCertificationResponse(UserCertificationBase):
    id: int
    class Config:
        from_attributes = True

# Dashboard Stats
class DashboardStats(BaseModel):
    active_count: int
    expired_count: int
