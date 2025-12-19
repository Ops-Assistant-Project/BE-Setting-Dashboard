from bson import ObjectId


def serialize_mongo(data):
    """
    MongoEngine / PyMongo 결과를 JSON-safe dict로 변환
    """
    if isinstance(data, dict):
        return {
            k: serialize_mongo(str(v) if isinstance(v, ObjectId) else v)
            for k, v in data.items()
        }

    if isinstance(data, list):
        return [serialize_mongo(item) for item in data]

    return data
