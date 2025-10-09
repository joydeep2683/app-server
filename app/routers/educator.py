"""
Educator router - API endpoints for Educator model
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.Educator])
def list_educators(db: Session = Depends(get_db)):
    """List all educators"""
    educators = db.query(models.Educator).all()
    return educators


@router.post("", response_model=schemas.Educator, status_code=status.HTTP_201_CREATED)
def create_educator(educator: schemas.EducatorCreate, db: Session = Depends(get_db)):
    """Create a new educator"""
    # Check if educator with same phone number exists
    existing_educator = db.query(models.Educator).filter(
        models.Educator.phone_number == educator.phone_number
    ).first()
    if existing_educator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Educator with this phone number already exists"
        )
    
    db_educator = models.Educator(**educator.model_dump())
    db.add(db_educator)
    db.commit()
    db.refresh(db_educator)
    return db_educator


@router.get("/{educator_id}", response_model=schemas.Educator)
def get_educator(educator_id: int, db: Session = Depends(get_db)):
    """Get a specific educator by ID"""
    educator = db.query(models.Educator).filter(models.Educator.id == educator_id).first()
    if not educator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Educator not found")
    return educator


@router.put("/{educator_id}", response_model=schemas.Educator)
def update_educator(educator_id: int, educator_update: schemas.EducatorUpdate, db: Session = Depends(get_db)):
    """Update an educator"""
    educator = db.query(models.Educator).filter(models.Educator.id == educator_id).first()
    if not educator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Educator not found")
    
    # Check if phone number conflicts with existing educator
    if educator_update.phone_number and educator_update.phone_number != educator.phone_number:
        existing_educator = db.query(models.Educator).filter(
            models.Educator.phone_number == educator_update.phone_number
        ).first()
        if existing_educator:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Educator with this phone number already exists"
            )
    
    for key, value in educator_update.model_dump(exclude_unset=True).items():
        setattr(educator, key, value)
    
    db.commit()
    db.refresh(educator)
    return educator


@router.patch("/{educator_id}", response_model=schemas.Educator)
def partial_update_educator(educator_id: int, educator_update: schemas.EducatorUpdate, db: Session = Depends(get_db)):
    """Partially update an educator"""
    return update_educator(educator_id, educator_update, db)


@router.delete("/{educator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_educator(educator_id: int, db: Session = Depends(get_db)):
    """Delete an educator"""
    educator = db.query(models.Educator).filter(models.Educator.id == educator_id).first()
    if not educator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Educator not found")
    
    db.delete(educator)
    db.commit()
    return None
