from fastapi import FastAPI, HTTPException
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

@app.get("/applications")
def get_applications(status:str = None):
    db: Session = SessionLocal()

    query = db.query(ApplicationModel)
    if status:
        query = query.filter(ApplicationModel.status == status)
    applications = query.all()

    db.close()

    return applications

@app.get("/applications/{application_id}")
def get_application(application_id: int):
    db: Session = SessionLocal()
    application = db.query(ApplicationModel).filter(
        ApplicationModel.id == application_id
    ).first()
    if application is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


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



@app.put("/applications/{application_id}")
def update_application(application_id: int,application: ApplicationCreate):
    db: Session = SessionLocal()
    existing_application = db.query(ApplicationModel).filter(
        ApplicationModel.id == application_id
    ).first()
    if existing_application is None:
        db.close()
        return{"Application not found"}
    existing_application.company = application.company
    existing_application.role = application.role
    existing_application.status = application.status

    db.commit()
    db.refresh(existing_application)
    if existing_application is None:
        db.close()
    raise HTTPException(
        status_code=404,
        detail="Application not found"
    )
    return existing_application\

@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    db: Session = SessionLocal()

    application = db.query(ApplicationModel).filter(
        ApplicationModel.id == application_id
    ).first()

    if application is None:
        db.close()
        raise HTTPException(status_code =404, detail = "Application not found")

    db.delete(application)
    db.commit()

    db.close()

    return {"message": "Application deleted successfully"}

    
    
