from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, get_db

# Crear tablas en SQLite en el primer arranque
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgroTech API",
    description="Backend MVP para registro de cultivos y actividades agrícolas.",
    version="1.0.0"
)

# CORS parameters para Streamlit (permitir peticiones de cualquier frontend por simplicidad)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambiar esto por dominios reales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "¡AgroTech API funcionando correctamente! Ir a /docs para ver los endpoints."}

# --- CROPS ---
@app.post("/crops/", response_model=schemas.CropResponse, tags=["Crops"])
def create_crop(crop: schemas.CropCreate, db: Session = Depends(get_db)):
    return crud.create_crop(db=db, crop=crop)

@app.get("/crops/", response_model=List[schemas.CropResponse], tags=["Crops"])
def read_crops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_crops(db=db, skip=skip, limit=limit)

@app.put("/crops/{crop_id}", response_model=schemas.CropResponse, tags=["Crops"])
def update_crop(crop_id: int, crop: schemas.CropUpdate, db: Session = Depends(get_db)):
    db_crop = crud.update_crop(db=db, crop_id=crop_id, crop_update=crop)
    if not db_crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return db_crop

@app.delete("/crops/{crop_id}", tags=["Crops"])
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    if not crud.delete_crop(db, crop_id):
        raise HTTPException(status_code=404, detail="Crop not found")
    return {"message": "Crop deleted successfully"}

# --- ACTIVITIES ---
@app.post("/crops/{crop_id}/activities/", response_model=schemas.ActivityResponse, tags=["Activities"])
def create_activity_for_crop(crop_id: int, activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    db_crop = crud.get_crop(db, crop_id=crop_id)
    if not db_crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crud.create_activity(db=db, activity=activity, crop_id=crop_id)

@app.get("/crops/{crop_id}/activities/", response_model=List[schemas.ActivityResponse], tags=["Activities"])
def get_activities_for_crop(crop_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_activities(db, crop_id=crop_id, skip=skip, limit=limit)

@app.delete("/activities/{activity_id}", tags=["Activities"])
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    if not crud.delete_activity(db, activity_id):
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}

# --- DASHBOARD & KPIs ---
@app.get("/dashboard/stats", tags=["Dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db=db)
