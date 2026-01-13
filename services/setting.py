from typing import List, Dict, Any, Optional
from models.setting import Setting, QuickActionStatus
from models.computer import Computer
from models.employee import Employee
from modules.okta import OktaClient
from common.constants import OktaGroups
from common.exceptions import NotFoundError
from schemas.setting import SettingCreateSchema
from services.crud_base import CrudBase


class SettingService(CrudBase):
    model = Setting

    def __init__(self):
        self.okta_client = OktaClient()
        self.SINGLE_EXECUTABLE_STATUS = {
            QuickActionStatus.PENDING,
            QuickActionStatus.ERROR,
            QuickActionStatus.DONE
        }
        self.BULK_EXECUTABLE_STATUS = {
            QuickActionStatus.PENDING,
            QuickActionStatus.ERROR
        }


    @classmethod
    def create(cls, data: SettingCreateSchema):
        if data.is_computer:
            computer = Computer.objects(serial=data.serial).first()

            if not computer:
                raise NotFoundError("Computer not found")

            user = Employee.objects(email=computer.user_email).first()
            setting = Setting(
                user_name = computer.user_name,
                user_email = computer.user_email,
                role = user.role,
                os = computer.os,
                model = computer.model,
                serial = computer.serial,
                device_type = computer.device_type,
                network_type = computer.network_type,
                urgency = data.urgency,
                onboarding_type = data.onboarding_type,
                status = data.status,
                memo = data.memo,
                quick_actions = cls.generate_quick_actions(os=computer.os, onboarding_type=data.onboarding_type),
                company = data.company,
                requested_date = data.requested_date,
                due_date = data.due_date
            )
        else:
            user = Employee.objects(email=data.user_email).first()
            setting = Setting(
                user_name = data.user_name,
                user_email = data.user_email,
                role = user.role,
                os = data.os,
                model = data.model,
                serial = data.serial,
                device_type = data.device_type,
                network_type = data.network_type,
                urgency = data.urgency,
                onboarding_type = data.onboarding_type,
                status = data.status,
                memo = data.memo,
                quick_actions = cls.generate_quick_actions(os=data.os, onboarding_type=data.onboarding_type),
                company = data.company,
                requested_date = data.requested_date,
                due_date = data.due_date
            )

        setting.save()
        return str(setting.id)

    @classmethod
    def bulk_update(cls, updates: List[Dict[str, Any]]):
        """
        여러 Setting 문서를 개별 업데이트

        Body 예시:
        {
            "updates": [
                {
                    "id": "<setting_id>",
                    "data": {
                        "status": "setting"
                    }
                }
            ]
        }
        """
        results = []

        for item in updates:
            setting_id = item.get("id")
            data = item.get("data")

            if not setting_id or not data:
                continue

            setting = cls.model.objects(id=setting_id).first()
            if not setting:
                results.append({
                    "id": setting_id,
                    "updated": False,
                    "reason": "not_found"
                })
                continue

            update_data = data.copy()

            os_changed = "os" in data and data["os"] != setting.os
            onboarding_changed = (
                    "onboarding_type" in data
                    and data["onboarding_type"] != setting.onboarding_type
            )

            if os_changed or onboarding_changed:
                new_os = data.get("os", setting.os)
                new_onboarding_type = data.get(
                    "onboarding_type",
                    setting.onboarding_type
                )

                update_data["quick_actions"] = cls.generate_quick_actions(
                    os=new_os,
                    onboarding_type=new_onboarding_type,
                    prev_actions=setting.quick_actions
                )

            updated = cls.model.objects(id=setting_id).update_one(**{
                f"set__{k}": v for k, v in update_data.items()
            })

            results.append({
                "id": setting_id,
                "updated": updated > 0
            })

        return {
            "requested_count": len(updates),
            "updated_count": sum(1 for r in results if r["updated"]),
            "results": results
        }


    def add_okta_setting(self, user_ids: List[str]):
        """
        Okta Setting 그룹에 추가 및 비밀번호 재설정
        """
        fail_ids = []

        for user_id in user_ids:
            res = self.okta_client.add_user_to_group(group_id=OktaGroups.ALL_SETTING, user_id=user_id)
            if not res.ok:
                fail_ids.append(user_id)

        return fail_ids


    def add_win_setting(self, user_ids: List[str]):
        """
        Okta Win Setting 그룹에 추가
        """
        fail_ids = []

        for user_id in user_ids:
            res = self.okta_client.add_user_to_group(group_id=OktaGroups.WIN_SETTING, user_id=user_id)
            if not res.ok:
                fail_ids.append(user_id)

        return fail_ids


    def add_o365_intune(self, user_ids: List[str]):
        """
        Okta o365 Intune 그룹에 추가
        """
        fail_ids = []

        for user_id in user_ids:
            res = self.okta_client.add_user_to_group(group_id=OktaGroups.O365_INTUNE, user_id=user_id)
            if not res.ok:
                fail_ids.append(user_id)

        return fail_ids


    def okta_activate(self, setting_ids: List[str]):
        """
        사용자 Okta 계정 활성화
        """
        fail_user_name = []
        continue_user_name = []
        is_single = len(setting_ids) == 1

        for setting_id in setting_ids:
            setting = Setting.objects(id=setting_id).first()
            actions = self.get_quick_actions(setting, ['okta-activate'])
            status = actions[0]["status"].value

            # 실행 가능 여부 확인
            if not self._is_executable(status=status, is_single=is_single):
                continue

            user = Employee.objects(email=setting.user_email).first()
            if not user:
                fail_user_name.append(setting.user_name)
                continue

            # res = self.okta_client.activate_user(user_id=user.okta_user_id)
            # if not res.ok:
            #     fail_user_name.append(setting.user_name)
            #     setting.save()

            # TODO: quick_actions 수정


        return fail_user_name

    def _is_executable(self, status: QuickActionStatus, is_single: bool) -> bool:
        """
        실행 가능 여부 판단 함수
        """
        if is_single:
            return status in self.SINGLE_EXECUTABLE_STATUS
        return status in self.BULK_EXECUTABLE_STATUS

    @staticmethod
    def get_quick_actions(setting: Setting, actions: List[str]) -> List[dict]:
        """
        setting.quick_actions에서 actions 리스트에 해당하는 객체만 반환
        :param setting: Setting 객체
        :param actions: 예. ['win-setting', 'o365-intune']
        :return: 조건에 맞는 quick_actions 객체 리스트
        """
        return [
            {
                "action": qa.action,
                "status": qa.status,
                "requested_by": qa.requested_by,
                "requested_at": qa.requested_at,
                "error_message": qa.error_message,
            }
            for qa in setting.quick_actions
            if qa.action in actions
        ]

    @staticmethod
    def generate_quick_actions(
            os: str,
            onboarding_type: str,
            prev_actions: Optional[List[Any]] = None
    ) -> List[Dict]:
        """
        onboarding_type과 OS에 따라 quick_actions 리스트 생성
        - status는 조건에 따라 재계산
        - requested_by, requested_at, error_message는 기존 값 유지

        :param os: 'Windows', 'Mac'
        :param onboarding_type: 'pending', 'new', 'rejoin', 'replace', 'switch'
        :param prev_actions:
        :return:
        """

        all_actions = [
            "okta-setting",
            "win-setting",
            "o365-intune",
            "password-notice",
            "pickup-notice",
            "okta-activate"
        ]

        actions_map = {
            "new": ["okta-setting"],
            "replace": ["okta-setting", "password-notice", "pickup-notice"],
            "rejoin": ["okta-activate"],
            "switch": ["okta-setting"],
            "pending": []
        }

        active_actions = actions_map.get(onboarding_type, [])

        if os.lower() == "windows" and onboarding_type in ["new", "replace", "switch"]:
            active_actions.extend(["win-setting", "o365-intune"])

        active_actions = set(active_actions)

        prev_map = {
            qa.action: qa
            for qa in (prev_actions or [])
        }

        quick_actions = []

        for action in all_actions:
            prev = prev_map.get(action)

            requested_by = getattr(prev, "requested_by", None)
            requested_at = getattr(prev, "requested_at", None)
            error_message = getattr(prev, "error_message", None)

            if action in active_actions:
                if requested_by and requested_at and error_message:
                    status = "error"
                elif requested_by and requested_at:
                    status = "done"
                else:
                    status = "pending"
            else:
                status = "n/a"

            quick_actions.append({
                "action": action,
                "status": status,
                "requested_by": requested_by,
                "requested_at": requested_at,
                "error_message": error_message,
            })

        return quick_actions
