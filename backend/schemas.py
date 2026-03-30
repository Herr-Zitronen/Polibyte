from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional

# --- Activity Schemas ---
class ActivityBase(BaseModel):
    activity_type: str
    date: date
    cost: float
    description: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    crop_id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- Crop Schemas ---
class CropBase(BaseModel):
    name: str
    area: float
    planting_date: date
    status: str

class CropCreate(CropBase):
    pass

class CropUpdate(CropBase):
    pass

class CropResponse(CropBase):
    id: int
    activities: List[ActivityResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
