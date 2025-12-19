from typing import List, Dict, Any
from models.setting import Setting
from services.crud_base import CrudBase
from modules.okta import OktaClient
from common.constants import OktaGroups


class SettingService(CrudBase):
    model = Setting

    def __init__(self):
        self.okta_client = OktaClient()

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
