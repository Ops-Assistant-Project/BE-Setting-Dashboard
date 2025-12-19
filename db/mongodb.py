from mongoengine import connect
import os

def connect_to_mongo():
    connect(
        db=os.getenv("MONGODB_DB_NAME"),
        host=os.getenv("MONGODB_URL"),
        alias="default"
    )
    print("✔️ MongoDB connected")

def close_mongo_connection():
    pass
