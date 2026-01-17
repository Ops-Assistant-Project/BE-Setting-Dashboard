from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel


class CheckListItemSchema(BaseModel):
    label: str
    checked: bool = False


class SettingCreateSchema(BaseModel):
    # 사용자 정보
    user_name: str
    user_email: str
    role: Literal["team", "asst"]
    collaborators: Optional[str] = None

    # PC 정보
    os: str
    model: str
    serial: str
    device_type: Literal["EDP001", "EDP002", "EDP003"]
    network_type: Literal["team", "sec"]

    # 상태 정보
    urgency: bool
    onboarding_type: Literal["pending", "new", "replace", "rejoin", "switch"]
    status: Literal["pending", "shipped", "setting", "completed"]

    # 기타
    memo: Optional[str] = None
    checklist: Optional[List[CheckListItemSchema]] = None

    assignee_name: Optional[str] = None
    company: Literal["core", "bank", "insu"]

    # 일정
    requested_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

    is_computer: bool = False