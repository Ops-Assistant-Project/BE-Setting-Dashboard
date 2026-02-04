from datetime import datetime
from models.computer import Computer
from models.setting import Setting
from models.employee import Employee
from services.setting import SettingService


def sync_setting_computers():
    existing_serials = set(
        Setting.objects.only("serial").scalar("serial")
    )

    target_computers = Computer.objects(status="setting")
    created_count = 0
    service = SettingService()

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

    return created_count
