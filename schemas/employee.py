from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmployeeCreateSchema(BaseModel):
    name: str
    email: str
    role: str

    okta_user_id: str
    ldap_id: str
    slack_id: str

    joined_at: Optional[datetime]

    class Config:
        from_attributes = True


class EmployeeUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

    okta_user_id: Optional[str] = None
    ldap_id: Optional[str] = None
    slack_id: Optional[str] = None

    status: Optional[str] = None  # ACTIVE / INACTIVE / SUSPENDED

    joined_at: Optional[datetime] = None
    resigned_at: Optional[datetime] = None

    class Config:
        extra = "forbid"  # 정의 안 된 필드 막기