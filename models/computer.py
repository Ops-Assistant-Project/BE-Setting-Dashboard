from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
)
from mongoengine.fields import EnumField
from enum import Enum


class DeviceType(str, Enum):
    EDP001 = "EDP001"
    EDP002 = "EDP002"
    EDP003 = "EDP003"


class NetworkType(str, Enum):
    TEAM = "team"
    SEC = "sec"


class ComputerStatus(str, Enum):
    KEEP = "KEEP"
    SETTING = "SETTING"
    USE = "USE"
    LOST = "LOST"

class Computer(Document):
    # 사용자 정보
    user_name = StringField(required=True)
    user_email = StringField(required=True)
    user_slack_key = StringField(required=True)
    user_ldap_name = StringField(required=True)

    # 장비 정보
    os = StringField(required=True)
    model = StringField(required=True)
    serial = StringField(required=True, unique=True)
    device_id = StringField(required=True, unique=True)
    ip_address = StringField(required=True)
    mac_address = StringField(required=True)
    os_version = StringField(required=True)

    device_type = EnumField(DeviceType, required=True)
    network_type = EnumField(NetworkType, required=True)

    status = EnumField(ComputerStatus, required=True, default=ComputerStatus.KEEP)
    notes = StringField(null=True)

    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "computers",
        "indexes": [
            "serial",
            "device_id",
            "user_email",
        ]
    }
