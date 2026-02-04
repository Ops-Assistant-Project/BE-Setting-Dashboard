from datetime import datetime
from typing import List, Dict, Any, Optional
from models.setting import Setting, QuickActionStatus, QuickAction
from models.computer import Computer, ComputerStatus
from models.employee import Employee
from modules.slack import BoltApp
from modules.okta import OktaClient
from modules.password import generate_password_for_week
from blocks.setting import password_notice_message_block, pickup_notice_message_block, pickup_notice_button_block, password_reset_message_block
from common.okta import OktaGroups
from common.slack import SlackBotName
from common.exceptions import NotFoundError
from schemas.setting import SettingCreateSchema
from services.crud_base import CrudBase


class SettingService(CrudBase):
    model = Setting

    def __init__(self):
        self.okta_client = OktaClient()
        self.slack_bot = BoltApp(SlackBotName.SETTING_BOT).client
        self.SINGLE_EXECUTABLE_STATUS = {
            QuickActionStatus.PENDING,
            QuickActionStatus.ERROR,
            QuickActionStatus.PROGRESS,
            QuickActionStatus.DONE
        }
        self.BULK_EXECUTABLE_STATUS = {
            QuickActionStatus.PENDING,
            QuickActionStatus.PROGRESS,
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
                due_date = data.due_date,
                is_manual = True
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
                due_date = data.due_date,
                is_manual = True
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
            status_changed = "status" in data and data["status"] != setting.status

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

            if not setting.is_manual and status_changed and data["status"] == "completed":
                computer = Computer.objects(serial=setting.serial).first()
                computer.status = ComputerStatus.USE
                computer.save()

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

    def password_notice(self, setting_ids: List[str], requested_by: str = None):
        fail_user_name = []
        is_single = len(setting_ids) == 1

        for setting_id in setting_ids:
            setting = Setting.objects(id=setting_id).first()
            if not setting:
                continue

            quick_action = self._get_quick_action(setting, 'password-notice')
            status = quick_action.status

            # 실행 가능 여부 확인
            if not self._is_executable(status=status, is_single=is_single):
                # n/a일 경우: 상태 유지 + 에러 메시지만 기록
                if status == QuickActionStatus.NA:
                    quick_action.error_message = "Action not applicable for this setting"
                    setting.save()
                fail_user_name.append(setting.user_name)
                continue

            # 실행 시작 - progress
            self._mark_quick_action_progress(
                action=quick_action,
                requested_by=requested_by,
            )
            setting.save()

            try:
                user = Employee.objects(email=setting.user_email).first()
                if not user:
                    raise Exception("User not found")

                # 슬랙 안내 DM 전송
                self.slack_bot.chat_postMessage(
                    channel=user.slack_id,
                    text="Okta 비밀번호 초기화 예정",
                    blocks=password_notice_message_block(user_name=user.name)
                )

                # 성공 시
                self._mark_quick_action_done(action=quick_action)
            except Exception as e:
                self._mark_quick_action_error(action=quick_action, error_message=str(e))
                fail_user_name.append(setting.user_name)
            finally:
                setting.save()

        return {"failed_users": fail_user_name, "failed_count": len(fail_user_name), "success_count": len(setting_ids) - len(fail_user_name)}

    def pickup_notice(self, setting_ids: List[str], requested_by: str = None):
        fail_user_name = []
        is_single = len(setting_ids) == 1

        for setting_id in setting_ids:
            setting = Setting.objects(id=setting_id).first()
            if not setting:
                continue

            quick_action = self._get_quick_action(setting, 'pickup-notice')
            status = quick_action.status

            # 실행 가능 여부 확인
            if not self._is_executable(status=status, is_single=is_single):
                # n/a일 경우: 상태 유지 + 에러 메시지만 기록
                if status == QuickActionStatus.NA:
                    quick_action.error_message = "Action not applicable for this setting"
                    setting.save()
                fail_user_name.append(setting.user_name)
                continue

            # 실행 시작 - progress
            self._mark_quick_action_progress(
                action=quick_action,
                requested_by=requested_by,
            )
            setting.save()

            try:
                user = Employee.objects(email=setting.user_email).first()
                if not user:
                    raise Exception("User not found")

                # 슬랙 안내 DM 전송
                self.slack_bot.chat_postMessage(
                    channel=user.slack_id,
                    text="장비 수령 안내",
                    blocks=pickup_notice_message_block()
                )

                self.slack_bot.chat_postMessage(
                    channel=user.slack_id,
                    text="수령 날짜 및 시간 선택",
                    blocks=pickup_notice_button_block()
                )

                # 성공 시
                self._mark_quick_action_done(action=quick_action)
            except Exception as e:
                self._mark_quick_action_error(action=quick_action, error_message=str(e))
                fail_user_name.append(setting.user_name)
            finally:
                setting.save()

        return {"failed_users": fail_user_name, "failed_count": len(fail_user_name), "success_count": len(setting_ids) - len(fail_user_name)}

    def okta_setting(self, setting_ids: List[str], requested_by: str = None):
        """
        Okta Setting 그룹에 추가 및 비밀번호 재설정
        """
        fail_user_name = []
        is_single = len(setting_ids) == 1

        for setting_id in setting_ids:
            setting = Setting.objects(id=setting_id).first()
            if not setting:
                continue

            quick_action = self._get_quick_action(setting, 'okta-setting')
            status = quick_action.status

            # 실행 가능 여부 확인
            if not self._is_executable(status=status, is_single=is_single):
                # n/a일 경우: 상태 유지 + 에러 메시지만 기록
                if status == QuickActionStatus.NA:
                    quick_action.error_message = "Action not applicable for this setting"
                    setting.save()
                fail_user_name.append(setting.user_name)
                continue

            # 실행 시작 - progress
            self._mark_quick_action_progress(
                action=quick_action,
                requested_by=requested_by,
            )
            setting.save()

            try:
                user = Employee.objects(email=setting.user_email).first()
                if not user:
                    raise Exception("User not found")

                # okta-setting 그룹에 유저 추가
                # res = self.okta_client.add_user_to_group(group_id=OktaGroups.ALL_SETTING, user_id=user.okta_user_id)
                # if not res.ok:
                #     raise Exception(res.error or "Okta Setting group assignment failed")

                # OKTA 계정 비밀번호 초기화
                new_password = generate_password_for_week()
                # res = self.okta_client.admin_set_password(user_id=user.okta_user_id, new_password=new_password)
                # if not res.ok:
                #     raise Exception(res.error or "Okta password reset failed")

                # 초기화 비밀번호 DM으로 전송
                self.slack_bot.chat_postMessage(
                    channel=user.slack_id,
                    text="Okta 비밀번호 초기화 안내",
                    blocks=password_reset_message_block(new_password)
                )

                # 성공 시
                self._mark_quick_action_done(action=quick_action)
            except Exception as e:
                self._mark_quick_action_error(action=quick_action, error_message=str(e))
                fail_user_name.append(setting.user_name)
            finally:
                setting.save()

        return {"failed_users": fail_user_name, "failed_count": len(fail_user_name), "success_count": len(setting_ids) - len(fail_user_name)}

    def win_setting(self, setting_ids: List[str], requested_by: str = None):
        """
        Okta Win Setting 그룹에 추가
        """
        fail_user_name = []
        is_single = len(setting_ids) == 1

        for setting_id in setting_ids:
            setting = Setting.objects(id=setting_id).first()
            if not setting:
                continue

            quick_action = self._get_quick_action(setting, 'win-setting')
            status = quick_action.status

            # 실행 가능 여부 확인
            if not self._is_executable(status=status, is_single=is_single):
                # n/a일 경우: 상태 유지 + 에러 메시지만 기록
                if status == QuickActionStatus.NA:
                    quick_action.error_message = "Action not applicable for this setting"
                    setting.save()
                fail_user_name.append(setting.user_name)
                continue

            # 실행 시작 - progress
            self._mark_quick_action_progress(
                action=quick_action,
                requested_by=requested_by,
            )
            setting.save()

            try:
                user = Employee.objects(email=setting.user_email).first()
                if not user:
                    raise Exception("User not found")

                # # win-setting 그룹에 유저 추가
                # res = self.okta_client.add_user_to_group(group_id=OktaGroups.WIN_SETTING, user_id=user.okta_user_id)
                # if not res.ok:
                #     raise Exception(res.error or "Windows group assignment failed")

                # 성공 시
                self._mark_quick_action_done(action=quick_action)
            except Exception as e:
                self._mark_quick_action_error(action=quick_action, error_message=str(e))
                fail_user_name.append(setting.user_name)
            finally:
                setting.save()

        return {"failed_users": fail_user_name, "failed_count": len(fail_user_name), "success_count": len(setting_ids) - len(fail_user_name)}

    def o365_setting(self, setting_ids: List[str], requested_by: str = None):
        """
        Okta o365 Intune 그룹에 추가
        """
        fail_user_name = []
        is_single = len(setting_ids) == 1

        for setting_id in setting_ids:
            setting = Setting.objects(id=setting_id).first()
            if not setting:
                continue

            quick_action = self._get_quick_action(setting, 'o365-intune')
            status = quick_action.status

            # 실행 가능 여부 확인
            if not self._is_executable(status=status, is_single=is_single):
                # n/a일 경우: 상태 유지 + 에러 메시지만 기록
                if status == QuickActionStatus.NA:
                    quick_action.error_message = "Action not applicable for this setting"
                    setting.save()
                fail_user_name.append(setting.user_name)
                continue

            # 실행 시작 - progress
            self._mark_quick_action_progress(
                action=quick_action,
                requested_by=requested_by,
            )
            setting.save()

            try:
                user = Employee.objects(email=setting.user_email).first()
                if not user:
                    raise Exception("User not found")

                # # 계정 활성화
                # res = self.okta_client.add_user_to_group(group_id=OktaGroups.O365_INTUNE, user_id=user.okta_user_id)
                # if not res.ok:
                #     raise Exception(res.error or "Intune group assignment failed")

                # 성공 시
                self._mark_quick_action_done(action=quick_action)
            except Exception as e:
                self._mark_quick_action_error(action=quick_action, error_message=str(e))
                fail_user_name.append(setting.user_name)
            finally:
                setting.save()

        return {"failed_users": fail_user_name, "failed_count": len(fail_user_name), "success_count": len(setting_ids) - len(fail_user_name)}

    def okta_activate(self, setting_ids: List[str], requested_by: str = None):
        """
        사용자 Okta 계정 활성화
        """
        fail_user_name = []
        is_single = len(setting_ids) == 1

        for setting_id in setting_ids:
            setting = Setting.objects(id=setting_id).first()
            if not setting:
                continue

            quick_action = self._get_quick_action(setting, 'okta-activate')
            status = quick_action.status

            # 실행 가능 여부 확인
            if not self._is_executable(status=status, is_single=is_single):
                # n/a일 경우: 상태 유지 + 에러 메시지만 기록
                if status == QuickActionStatus.NA:
                    quick_action.error_message = "Action not applicable for this setting"
                    setting.save()
                fail_user_name.append(setting.user_name)
                continue

            # 실행 시작 - progress
            self._mark_quick_action_progress(
                action=quick_action,
                requested_by=requested_by,
            )
            setting.save()

            try:
                user = Employee.objects(email=setting.user_email).first()
                if not user:
                    raise Exception("User not found")

                # 계정 활성화
                # res = self.okta_client.activate_user(user_id=user.okta_user_id)
                # if not res.ok:
                #     raise Exception(res.error or "Okta activation failed")

                # 성공 시
                self._mark_quick_action_done(action=quick_action)
            except Exception as e:
                self._mark_quick_action_error(action=quick_action, error_message=str(e))
                fail_user_name.append(setting.user_name)
            finally:
                setting.save()

        return {"failed_users": fail_user_name, "failed_count": len(fail_user_name), "success_count": len(setting_ids) - len(fail_user_name)}

    def _is_executable(self, status: QuickActionStatus, is_single: bool) -> bool:
        """
        실행 가능 여부 판단 함수
        """
        if is_single:
            return status in self.SINGLE_EXECUTABLE_STATUS
        return status in self.BULK_EXECUTABLE_STATUS

    def _get_quick_action(self, setting, action_name: str) -> QuickAction | None:
        """
        setting.quick_actions에서 actions 리스트에 해당하는 객체만 반환
        :param setting: Setting 객체
        :param action_name: 예. 'o365-intune'
        :return: 조건에 맞는 quick_action 객체
        """
        for action in setting.quick_actions:
            if action.action == action_name:
                return action
        return None

    def _mark_quick_action_progress(self, action: QuickAction, requested_by: str):
        action.requested_by = requested_by
        action.requested_at = datetime.utcnow()
        action.status = QuickActionStatus.PROGRESS
        action.error_message = None

    def _mark_quick_action_done(self, action: QuickAction):
        action.status = QuickActionStatus.DONE
        action.error_message = None

    def _mark_quick_action_error(self, action: QuickAction, error_message: str):
        action.status = QuickActionStatus.ERROR
        action.error_message = error_message

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
