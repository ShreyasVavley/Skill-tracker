from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text, and_
from datetime import date, timedelta
import models
import schemas
from database import engine, get_db
import os

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Skill & Certification Tracker")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/organizations/", response_model=schemas.OrganizationResponse)
def create_organization(org: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    db_org = models.Organization(**org.model_dump())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@app.get("/organizations/", response_model=list[schemas.OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    return db.query(models.Organization).all()

@app.post("/certifications/", response_model=schemas.CertificationResponse)
def create_certification(cert: schemas.CertificationCreate, db: Session = Depends(get_db)):
    db_cert = models.Certification(**cert.model_dump())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

@app.get("/certifications/", response_model=list[schemas.CertificationResponse])
def get_certifications(db: Session = Depends(get_db)):
    return db.query(models.Certification).all()

@app.post("/user-certifications/", response_model=schemas.UserCertificationResponse)
def create_user_certification(user_cert: schemas.UserCertificationCreate, db: Session = Depends(get_db)):
    db_user_cert = models.UserCertification(**user_cert.model_dump())
    db.add(db_user_cert)
    db.commit()
    db.refresh(db_user_cert)
    return db_user_cert

@app.get("/user-certifications/", response_model=list[schemas.UserCertificationResponse])
def get_user_certifications(db: Session = Depends(get_db)):
    return db.query(models.UserCertification).all()

# Renewal Alert Logic: A specialized API endpoint that returns all certifications expiring within the next 30 days using a SQL BETWEEN query.
@app.get("/alerts/expiring-soon")
def get_expiring_certifications(db: Session = Depends(get_db)):
    today = date.today()
    thirty_days_from_now = today + timedelta(days=30)
    
    # Using SQL BETWEEN equivalent in SQLAlchemy
    expiring_certs = db.query(models.UserCertification).filter(
        models.UserCertification.expiry_date.between(today, thirty_days_from_now)
    ).all()
    
    result = []
    for uc in expiring_certs:
        user = db.query(models.User).filter(models.User.id == uc.user_id).first()
        cert = db.query(models.Certification).filter(models.Certification.id == uc.certification_id).first()
        result.append({
            "user_name": user.name if user else "Unknown",
            "certification_name": cert.name if cert else "Unknown",
            "expiry_date": uc.expiry_date,
            "credential_url": uc.credential_url
        })
    return result

@app.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()
    active_count = db.query(models.UserCertification).filter(models.UserCertification.expiry_date >= today).count()
    expired_count = db.query(models.UserCertification).filter(models.UserCertification.expiry_date < today).count()
    
    return schemas.DashboardStats(
        active_count=active_count,
        expired_count=expired_count
    )

# Mount frontend static files last so it doesn't override API routes
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
