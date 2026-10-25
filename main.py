from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, Base, SessionLocal
from models import Application as ApplicationModel
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)
class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str


@app.get("/")
def home():
    db: Session = SessionLocal()
    applications = db.query(ApplicationModel).all()
    db.close()
    return applications


@app.post("/applications")
def create_application(application: ApplicationCreate):
    db: Session = SessionLocal()
    new_Application = ApplicationModel(
        company = application.company,
        role = application.role,
        status = application.status
    )
    db.add(new_Application)
    db.commit()
    db.refresh(new_Application)
    db.close
    return new_Application
