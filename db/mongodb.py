from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

class MongoDB:
    client: Optional[MongoClient] = None
    db = None


mongodb = MongoDB()


def connect_to_mongo():
    """앱 시작 시 한 번만 실행 — MongoDB 클라이언트 초기화"""
    mongodb.client = MongoClient(MONGODB_URL)
    mongodb.db = mongodb.client[MONGODB_DB_NAME]
    print("✔️ MongoDB connected")


def close_mongo_connection():
    """앱 종료 시 호출 — 커넥션 종료"""
    if mongodb.client:
        mongodb.client.close()
        print("👋 MongoDB connection closed")


@lru_cache
def get_collection(collection_name: str) -> Collection:
    """서비스 레이어에서 호출 — 특정 컬렉션 핸들 반환"""
    if not mongodb.db:
        raise RuntimeError("MongoDB is not connected yet")
    return mongodb.db[collection_name]
