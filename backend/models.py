from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    area = Column(Float) # Hectáreas
    planting_date = Column(Date)
    status = Column(String, default="Activo") # Activo, Cosechado

    activities = relationship("Activity", back_populates="crop", cascade="all, delete-orphan")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    activity_type = Column(String) # Riego, Fumigación, Poda, etc.
    date = Column(Date)
    cost = Column(Float)
    description = Column(String, nullable=True)

    crop = relationship("Crop", back_populates="activities")
