from datetime import datetime
from models.computer import Computer, ComputerStatus
from models.setting import Setting
from models.employee import Employee
from services.setting import SettingService


def sync_setting_computers():
    """
    computer.status == SETTING -> setting에 자동 추가
    computer.status == USE -> setting에서 자동 삭제
    :return:
    """
    existing_serials = set(
        Setting.objects.only("serial").scalar("serial")
    )

    target_computers = Computer.objects(status=ComputerStatus.SETTING)
    created_count = 0
    deleted_count = 0

    service = SettingService()

    # SETTING 추가
    for computer in target_computers:
        if computer.serial in existing_serials:
            continue

        user = Employee.objects(email=computer.user_email).first()

        Setting(
            user_name=computer.user_name,
            user_email=computer.user_email,
            role=user.role,
            os=computer.os,
            model=computer.model,
            serial=computer.serial,
            device_type=computer.device_type,
            network_type=computer.network_type,
            onboarding_type="pending",
            status="setting",
            company=user.company,
            requested_date=datetime.utcnow(),
            quick_actions=service.generate_quick_actions(os=computer.os, onboarding_type="pending")
        ).save()

        created_count += 1

    # USE 삭제
    use_computers = Computer.objects(status=ComputerStatus.USE)
    use_serial = {computer.serial for computer in use_computers}

    delete_targets = existing_serials & use_serial

    if delete_targets:
        deleted_count = Setting.objects(serial__in=list(delete_targets)).delete()

    return {
        "created": created_count,
        "deleted": deleted_count,
    }
