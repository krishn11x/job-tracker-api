from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Application(BaseModel):
    company: str
    role: str
    status: str


@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}


@app.post("/applications")
def create_application(application: Application):
    return application