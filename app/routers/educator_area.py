"""
EducatorArea router - API endpoints for EducatorArea model
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.EducatorArea])
def list_educator_areas(db: Session = Depends(get_db)):
    """List all educator-area relations"""
    educator_areas = db.query(models.EducatorArea).all()
    return educator_areas


@router.post("", response_model=schemas.EducatorArea, status_code=status.HTTP_201_CREATED)
def create_educator_area(educator_area: schemas.EducatorAreaCreate, db: Session = Depends(get_db)):
    """Create a new educator-area relation"""
    # Verify educator exists
    educator = db.query(models.Educator).filter(models.Educator.id == educator_area.educator_id).first()
    if not educator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Educator not found")

    # Verify area exists
    area = db.query(models.Area).filter(models.Area.id == educator_area.area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")

    # Prevent duplicate mapping
    existing = db.query(models.EducatorArea).filter(
        models.EducatorArea.educator_id == educator_area.educator_id,
        models.EducatorArea.area_id == educator_area.area_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EducatorArea already exists")

    db_ea = models.EducatorArea(**educator_area.model_dump())
    db.add(db_ea)
    db.commit()
    db.refresh(db_ea)
    return db_ea


@router.get("/{educator_area_id}", response_model=schemas.EducatorArea)
def get_educator_area(educator_area_id: int, db: Session = Depends(get_db)):
    """Get a specific educator-area relation by ID"""
    ea = db.query(models.EducatorArea).filter(models.EducatorArea.id == educator_area_id).first()
    if not ea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EducatorArea not found")
    return ea


@router.put("/{educator_area_id}", response_model=schemas.EducatorArea)
def update_educator_area(educator_area_id: int, ea_update: schemas.EducatorAreaCreate, db: Session = Depends(get_db)):
    """Update an educator-area relation"""
    ea = db.query(models.EducatorArea).filter(models.EducatorArea.id == educator_area_id).first()
    if not ea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EducatorArea not found")

    # Verify educator exists
    educator = db.query(models.Educator).filter(models.Educator.id == ea_update.educator_id).first()
    if not educator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Educator not found")

    # Verify area exists
    area = db.query(models.Area).filter(models.Area.id == ea_update.area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")

    # Prevent duplicate mapping (except self)
    existing = db.query(models.EducatorArea).filter(
        models.EducatorArea.educator_id == ea_update.educator_id,
        models.EducatorArea.area_id == ea_update.area_id,
        models.EducatorArea.id != educator_area_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Another EducatorArea with same educator and area exists")

    for key, value in ea_update.model_dump().items():
        setattr(ea, key, value)

    db.commit()
    db.refresh(ea)
    return ea


@router.patch("/{educator_area_id}", response_model=schemas.EducatorArea)
def partial_update_educator_area(educator_area_id: int, ea_update: schemas.EducatorAreaCreate, db: Session = Depends(get_db)):
    """Partially update an educator-area relation"""
    return update_educator_area(educator_area_id, ea_update, db)


@router.delete("/{educator_area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_educator_area(educator_area_id: int, db: Session = Depends(get_db)):
    """Delete an educator-area relation"""
    ea = db.query(models.EducatorArea).filter(models.EducatorArea.id == educator_area_id).first()
    if not ea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EducatorArea not found")

    db.delete(ea)
    db.commit()
    return None
