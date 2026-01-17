from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from common.exceptions import NotFoundError
from schemas.setting import SettingCreateSchema
from services.setting import SettingService


router = APIRouter(prefix="/settings", tags=["Settings"])


class OktaRequest(BaseModel):
    setting_ids: List[str]
    requested_by: str


class BulkUpdateRequest(BaseModel):
    updates: List[Dict[str, Any]]


@router.post("/", summary="Create setting")
def create_setting(payload: SettingCreateSchema):
    try:
        setting_id = SettingService.create(payload)
        return {"id": setting_id}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{setting_id}", summary="Get setting by id")
def get_setting(setting_id: str):
    setting = SettingService.get(setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    return setting


@router.get("/", summary="List settings")
def list_settings():
    return SettingService.list()


@router.patch("/", summary="Bulk update settings")
def update_settings(payload: BulkUpdateRequest):
    return SettingService.bulk_update(payload.updates)


@router.delete("/{setting_id}", summary="Delete setting")
def delete_setting(setting_id: str):
    success = SettingService.delete(setting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"message": "deleted"}


@router.patch("/action/win-setting", summary="빠른 실행 - Okta win setting 그룹에 추가")
def win_setting(request: OktaRequest):
    return SettingService().win_setting(request.setting_ids, request.requested_by)


@router.patch("/action/okta-setting", summary="빠른 실행 - 비밀번호 초기화 및 Okta setting 그룹에 추가")
def okta_setting(request: OktaRequest):
    return SettingService().okta_setting(request.setting_ids, request.requested_by)


@router.patch("/action/o365-intune", summary="빠른 실행 - Okta o365 intune 그룹에 추가")
def o365_setting(request: OktaRequest):
    return SettingService().o365_setting(request.setting_ids, request.requested_by)


@router.patch("/action/password-notice", summary="빠른 실행 - 비밀번호 초기화 안내 전송")
def password_notice(request: OktaRequest):
    return SettingService().password_notice(request.setting_ids, request.requested_by)


@router.patch("/action/pickup-notice", summary="빠른 실행 - 장비 수령 안내 전송")
def pickup_notice(request: OktaRequest):
    return SettingService().pickup_notice(request.setting_ids, request.requested_by)


@router.patch("/action/okta-activate", summary="빠른 실행 - Okta 계정 활성화")
def okta_activate(request: OktaRequest):
    return SettingService().okta_activate(request.setting_ids, request.requested_by)
