from datetime import datetime
from enum import Enum
from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    BooleanField,
    DateTimeField,
    EmbeddedDocumentListField,
)
from mongoengine.fields import EnumField


class Role(str, Enum):
    TEAM = "team"   # 팀원
    ASST = "asst"   # 어시


class DeviceType(str, Enum):
    EDP001 = "EDP001"   # 인터넷 PC
    EDP002 = "EDP002"
    EDP003 = "EDP003"


class NetworkType(str, Enum):
    TEAM = "team"   # 인터넷망
    SEC = "sec" # 분리망


class OnboardingType(str, Enum):
    PENDING = "pending" # 미정
    NEW = "new" # 신규 입사
    REPLACE = "replace" # 교체
    REJOIN = "rejoin"   # 복직
    SWITCH = "switch"   # 전환


class SettingStatus(str, Enum):
    PENDING = "pending" # 출고 전
    SHIPPED = "shipped" # 출고 완료
    SETTING = "setting" # 세팅 중
    COMPLETED = "completed" # 세팅 완료


class Company(str, Enum):
    CORE = "core"
    BANK = "bank"
    INSU = "insu"


class QuickActionStatus(str, Enum):
    NA = "n/a"  # 관련 없음
    PENDING = "pending"
    PROGRESS = "progress"
    DONE = "done"
    ERROR = "error"


class QuickAction(EmbeddedDocument):
    """
    빠른 실행 액션 기록
    """
    action = StringField(required=True) # 액션 이름 (win-setting, okta-setting 등)
    requested_by = StringField(required=True)   # 실행한 사람
    requested_at = DateTimeField(required=True) # 실행 시각
    status = EnumField(QuickActionStatus, required=True)
    error_message = StringField(null=True)


class CheckListItem(EmbeddedDocument):
    """
    체크리스트 아이템
    """
    label = StringField(required=True)  # 체크 항목 이름
    checked = BooleanField(default=False)   # 완료 여부


class Setting(Document):
    """
    PC 세팅 요청 메인 모델
    """

    # 사용자 정보
    user_name = StringField(required=True)
    user_email = StringField(required=True)
    role = EnumField(Role, required=True)
    collaborators = StringField(null=True)

    # PC 정보
    os = StringField(required=True)
    model = StringField(required=True)
    serial = StringField(required=True)
    device_type = EnumField(DeviceType, required=True)
    network_type = EnumField(NetworkType, required=True)

    # 상태 정보
    urgency = BooleanField(required=True)   # True: 급건 / False: 일반
    onboarding_type = EnumField(OnboardingType, required=True)
    status = EnumField(SettingStatus, required=True)

    # 기타
    memo = StringField(null=True)
    checklist = EmbeddedDocumentListField(CheckListItem)
    quick_actions = EmbeddedDocumentListField(QuickAction)

    assignee_name = StringField(null=True)
    company = EnumField(Company, required=True)

    # 일정
    requested_date = DateTimeField(null=True)
    due_date = DateTimeField(null=True)
    completed_date = DateTimeField(null=True)

    meta = {
        "collection": "setting",
        "indexes": [
            "user_email",
            "serial",
        ]
    }
