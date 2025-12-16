from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class Computer(BaseModel):
    # 사용자 정보
    user_name: str
    user_email: str
    user_slack_key: str
    user_ldap_name: str

    # 장비 정보
    os: str
    model: str
    serial: str
    device_id: str
    ip_address: str
    mac_address: str
    os_version: str
    device_type: Literal["EDP001", "EDP002", "EDP003"]  # 단말 종류(인터넷PC, ...)
    network_type: Literal["team", "sec"]    # 망 종류(인터넷망, 분리망)

    status: Literal["KEEP", "SETTING", "USE", "LOST"]   # 보관, 세팅중, 사용중, 분실
    notes: Optional[str]

    updated_at: datetime