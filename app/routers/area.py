"""
Area router - API endpoints for Area model
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.Area])
def list_areas(db: Session = Depends(get_db)):
    """List all areas"""
    areas = db.query(models.Area).all()
    return areas


@router.post("", response_model=schemas.Area, status_code=status.HTTP_201_CREATED)
def create_area(area: schemas.AreaCreate, db: Session = Depends(get_db)):
    """Create a new area"""
    # Check if area with same name exists
    existing_area = db.query(models.Area).filter(models.Area.name == area.name).first()
    if existing_area:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Area with this name already exists"
        )
    
    db_area = models.Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


@router.post("/bulk", response_model=List[schemas.Area], status_code=status.HTTP_201_CREATED)
def bulk_create_areas(areas: List[schemas.AreaCreate], db: Session = Depends(get_db)):
    """Create multiple areas in bulk"""
    db_areas = []
    for area in areas:
        # Check if area with same name exists
        existing_area = db.query(models.Area).filter(models.Area.name == area.name).first()
        if existing_area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Area with name '{area.name}' already exists"
            )
        db_areas.append(models.Area(**area.model_dump()))
    
    db.add_all(db_areas)
    db.commit()
    for db_area in db_areas:
        db.refresh(db_area)
    return db_areas


@router.get("/{area_id}", response_model=schemas.Area)
def get_area(area_id: int, db: Session = Depends(get_db)):
    """Get a specific area by ID"""
    area = db.query(models.Area).filter(models.Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return area


@router.put("/{area_id}", response_model=schemas.Area)
def update_area(area_id: int, area_update: schemas.AreaUpdate, db: Session = Depends(get_db)):
    """Update an area"""
    area = db.query(models.Area).filter(models.Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    
    # Check if new name conflicts with existing area
    if area_update.name != area.name:
        existing_area = db.query(models.Area).filter(models.Area.name == area_update.name).first()
        if existing_area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Area with this name already exists"
            )
    
    for key, value in area_update.model_dump().items():
        setattr(area, key, value)
    
    db.commit()
    db.refresh(area)
    return area


@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area(area_id: int, db: Session = Depends(get_db)):
    """Delete an area"""
    area = db.query(models.Area).filter(models.Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    
    db.delete(area)
    db.commit()
    return None
