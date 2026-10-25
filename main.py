from fastapi import FastAPI, HTTPException, Depends
from typing import Literal
from pydantic import BaseModel,HttpUrl, Field
from database import engine, Base, SessionLocal
from models import Application as ApplicationModel
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1)
    role: str = Field(min_length=1)
    status: Literal["Applied", "Interview", "Rejected", "Selected"]
    application_date: str = Field(min_length=1)
    job_link: HttpUrl
    notes: str = Field(min_length=1)

@app.get("/applications")
def get_applications(status:str = None, db: Session = Depends(get_db)):
   

    query = db.query(ApplicationModel)
    if status:
        query = query.filter(ApplicationModel.status == status)
    applications = query.all()

    

    return applications

@app.get("/applications/{application_id}")
@app.get("/applications/{application_id}")
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.query(ApplicationModel).filter(
        ApplicationModel.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application



@app.post("/applications")
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    
    new_application = ApplicationModel(
    company=application.company,
    role=application.role,
    status=application.status,
    application_date=application.application_date,
    job_link=str(application.job_link),
    notes=application.notes
)
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    
    return new_application



@app.put("/applications/{application_id}")
def update_application(application_id: int, application: ApplicationCreate, db: Session = Depends(get_db)):
    

    existing_application = db.query(ApplicationModel).filter(
        ApplicationModel.id == application_id
    ).first()

    if existing_application is None:
        
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    existing_application.company = application.company
    existing_application.role = application.role
    existing_application.status = application.status
    existing_application.application_date = application.application_date
    existing_application.job_link = str(application.job_link)
    existing_application.notes = application.notes

    db.commit()
    db.refresh(existing_application)
    

    return existing_application

@app.delete("/applications/{application_id}")
def delete_application(application_id: int,  db: Session = Depends(get_db)):
   

    application = db.query(ApplicationModel).filter(
        ApplicationModel.id == application_id
    ).first()

    if application is None:
        
        raise HTTPException(status_code =404, detail = "Application not found")

    db.delete(application)
    db.commit()



    return {"message": "Application deleted successfully"}

    
    
