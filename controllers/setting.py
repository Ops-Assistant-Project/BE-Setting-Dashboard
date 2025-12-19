from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from schemas.setting import SettingCreateSchema
from services.setting import SettingService


router = APIRouter(prefix="/settings", tags=["Settings"])


class OktaRequest(BaseModel):
    setting_ids: List[str]


class BulkUpdateRequest(BaseModel):
    updates: List[Dict[str, Any]]


@router.post("/", summary="Create setting")
def create_setting(payload: SettingCreateSchema):
    try:
        setting_id = SettingService.create(payload.dict())
        return {"id": setting_id}
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