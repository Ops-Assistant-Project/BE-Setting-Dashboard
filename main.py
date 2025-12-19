from fastapi import FastAPI
from controllers.setting import router as SettingController
from db.mongodb import connect_to_mongo

app = FastAPI(title="PC Setting Dashboard API")


@app.on_event("startup")
def startup():
    connect_to_mongo()


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(SettingController)