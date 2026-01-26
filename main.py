from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.mongodb import connect_to_mongo
from controllers.slack import router as SlackRouter
from controllers.setting import router as SettingController
from controllers.employee import router as EmployeeController

app = FastAPI(title="PC Setting Dashboard API")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    connect_to_mongo()


@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(SlackRouter)
app.include_router(SettingController)
app.include_router(EmployeeController)