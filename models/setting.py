from pydantic import BaseModel, Field
from typing import List, Optional, Literal, ClassVar, Dict
from datetime import datetime

class QuickAction(BaseModel):
    action: str # 액션 이름
    requested_by: str   # 마지막으로 실행한 사람 이름
    requested_at: datetime  # 마지막으로 실행한 날짜
    status: Literal["n/a", "pending", "progress", "done", "error"]  # 관련 없음, 진행 전, 진행 중, 진행 완료, 오류 발생
    error_message: Optional[str] = None

class CheckListItem(BaseModel):
    label: str  # 체크리스트 아이템
    checked: bool = False   # True: 완료 / False: 미완료

class Setting(BaseModel):
    # 사용자 정보
    user_name: str
    user_email: str
    role: Literal["team", "asst"]   # 팀원, 어시
    collaborators: Optional[str] = None    # 협업 팀원(어시일 경우)

    # pc 정보
    os: str
    model: str
    serial: str
    device_type: Literal["EDP001", "EDP002", "EDP003"]  # 단말 종류(인터넷PC, ...)
    network_type: Literal["team", "sec"]    # 망 종류(인터넷망, 분리망)

    urgency: bool # 긴급도(True: 급건/False: 일반)
    onboarding_type: Literal["pending", "new", "replace", "rejoin", "switch"]   # 미정, 신규입사, 교체, 복직, 전환
    status: Literal["pending", "shipped", "setting", "completed"]  # 출고 전, 출고완료, 세팅중, 세팅완료
    memo: Optional[str] = None # 메모
    checklist: Optional[List[CheckListItem]] = None
    quick_actions: List[QuickAction] = Field(default_factory=list)
    assignee_name: Optional[str] = None
    company: Literal["core", "bank", "insu"]

    requested_date: Optional[datetime] = None    # 요청일
    due_date: Optional[datetime] = None  # 마감일
    completed_date: Optional[datetime] = None    # 완료일

    meta: ClassVar[Dict[str, str]] = {
        "collection": "setting"
    }

    @classmethod
    def get_collection(cls):
        from db.mongodb import mongodb
        return mongodb.db[cls.meta["collection"]]