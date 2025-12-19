from typing import List, Dict, Any
from models.setting import Setting
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

            updated = cls.model.objects(id=setting_id).update_one(**{
                f"set__{k}": v for k, v in data.items()
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

        # for setting_id in setting_ids:
        #     setting = Setting.objects(id=setting_id).first()
        #
        #     if len(setting_ids) == 1:
        #         res = self.okta_client.activate_user(user_id=setting.)
        #     res = self.okta_client.activate_user(user_id=)
        #     if not res.ok:
        #         fail_ids.append(user_id)
        #
        # return fail_ids