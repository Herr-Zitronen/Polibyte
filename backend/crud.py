from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas

# --- CROPS ---
def get_crop(db: Session, crop_id: int):
    return db.query(models.Crop).filter(models.Crop.id == crop_id).first()

def get_crops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Crop).offset(skip).limit(limit).all()

def create_crop(db: Session, crop: schemas.CropCreate):
    db_crop = models.Crop(**crop.model_dump())
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop

def update_crop(db: Session, crop_id: int, crop_update: schemas.CropUpdate):
    db_crop = db.query(models.Crop).filter(models.Crop.id == crop_id).first()
    if db_crop:
        for key, value in crop_update.model_dump().items():
            setattr(db_crop, key, value)
        db.commit()
        db.refresh(db_crop)
    return db_crop

def delete_crop(db: Session, crop_id: int):
    db_crop = db.query(models.Crop).filter(models.Crop.id == crop_id).first()
    if db_crop:
        db.delete(db_crop)
        db.commit()
        return True
    return False


# --- ACTIVITIES ---
def get_activities(db: Session, crop_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Activity)
    if crop_id:
        query = query.filter(models.Activity.crop_id == crop_id)
    return query.offset(skip).limit(limit).all()

def create_activity(db: Session, activity: schemas.ActivityCreate, crop_id: int):
    db_activity = models.Activity(**activity.model_dump(), crop_id=crop_id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
        return True
    return False

# --- PROCESAMIENTO BÁSICO (KPIs y Dashboard) ---
def get_dashboard_stats(db: Session):
    total_crops = db.query(func.count(models.Crop.id)).scalar()
    active_crops = db.query(func.count(models.Crop.id)).filter(models.Crop.status == "Activo").scalar()
    total_area = db.query(func.sum(models.Crop.area)).scalar() or 0.0
    total_cost = db.query(func.sum(models.Activity.cost)).scalar() or 0.0
    
    # Costos agrupados por tipo de actividad
    cost_by_activity = db.query(
        models.Activity.activity_type, func.sum(models.Activity.cost).label('total_cost')
    ).group_by(models.Activity.activity_type).all()
    
    # Costos asociados por cultivo
    cost_by_crop = db.query(
        models.Crop.name, func.sum(models.Activity.cost).label('total_cost')
    ).join(models.Activity, models.Crop.id == models.Activity.crop_id).group_by(models.Crop.name).all()

    return {
        "total_crops": total_crops,
        "active_crops": active_crops,
        "total_area": round(total_area, 2),
        "total_cost": round(total_cost, 2),
        "cost_by_activity": [{"type": a[0], "cost": a[1]} for a in cost_by_activity if a[1] > 0],
        "cost_by_crop": [{"crop": c[0], "cost": c[1]} for c in cost_by_crop if c[1] > 0]
    }
