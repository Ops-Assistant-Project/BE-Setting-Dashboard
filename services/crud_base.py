from typing import Type, Optional, Dict, Any, List
from mongoengine import Document
from common.serializers import serialize_mongo


class CrudBase:
    model: Type[Document]

    @classmethod
    def create(cls, data: Dict[str, Any]) -> str:
        obj = cls.model(**data)
        obj.save()
        return str(obj.id)

    @classmethod
    def get(cls, doc_id: str):
        obj = cls.model.objects(id=doc_id).first()
        if not obj:
            return None

        data = obj.to_mongo().to_dict()
        data["id"] = str(obj.id)
        data.pop("_id", None)

        return serialize_mongo(data)

    @classmethod
    def list(cls, filters: Optional[Dict[str, Any]] = None, order_by: Optional[str] = None):
        filters = filters or {}
        results = []

        qs = cls.model.objects(**filters)

        if order_by:
            qs = qs.order_by(order_by)

        for obj in qs:
            data = obj.to_mongo().to_dict()
            data["id"] = str(obj.id)
            data.pop("_id", None)

            results.append(serialize_mongo(data))

        return results

    @classmethod
    def update(cls, doc_id: str, data: Dict[str, Any]) -> bool:
        result = cls.model.objects(id=doc_id).update_one(**{
            f"set__{k}": v for k, v in data.items()
        })
        return result > 0

    @classmethod
    def delete(cls, doc_id: str) -> bool:
        return cls.model.objects(id=doc_id).delete() > 0
