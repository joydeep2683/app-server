"""
Degree router - API endpoints for Degree model
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.Degree])
def list_degrees(db: Session = Depends(get_db)):
    """List all degrees"""
    degrees = db.query(models.Degree).all()
    return degrees


@router.post("", response_model=schemas.Degree, status_code=status.HTTP_201_CREATED)
def create_degree(degree: schemas.DegreeCreate, db: Session = Depends(get_db)):
    """Create a new degree"""
    # Check if degree with same name exists
    existing_degree = db.query(models.Degree).filter(models.Degree.name == degree.name).first()
    if existing_degree:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Degree with this name already exists"
        )
    
    db_degree = models.Degree(**degree.model_dump())
    db.add(db_degree)
    db.commit()
    db.refresh(db_degree)
    return db_degree


@router.post("/bulk", response_model=List[schemas.Degree], status_code=status.HTTP_201_CREATED)
def bulk_create_degrees(degrees: List[schemas.DegreeCreate], db: Session = Depends(get_db)):
    """Create multiple degrees in bulk"""
    db_degrees = []
    for degree in degrees:
        # Check if degree with same name exists
        existing_degree = db.query(models.Degree).filter(models.Degree.name == degree.name).first()
        if existing_degree:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Degree with name '{degree.name}' already exists"
            )
        db_degrees.append(models.Degree(**degree.model_dump()))
    
    db.add_all(db_degrees)
    db.commit()
    for db_degree in db_degrees:
        db.refresh(db_degree)
    return db_degrees


@router.get("/{degree_id}", response_model=schemas.Degree)
def get_degree(degree_id: int, db: Session = Depends(get_db)):
    """Get a specific degree by ID"""
    degree = db.query(models.Degree).filter(models.Degree.id == degree_id).first()
    if not degree:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Degree not found")
    return degree


@router.put("/{degree_id}", response_model=schemas.Degree)
def update_degree(degree_id: int, degree_update: schemas.DegreeUpdate, db: Session = Depends(get_db)):
    """Update a degree"""
    degree = db.query(models.Degree).filter(models.Degree.id == degree_id).first()
    if not degree:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Degree not found")
    
    # Check if new name conflicts with existing degree
    if degree_update.name != degree.name:
        existing_degree = db.query(models.Degree).filter(models.Degree.name == degree_update.name).first()
        if existing_degree:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Degree with this name already exists"
            )
    
    for key, value in degree_update.model_dump().items():
        setattr(degree, key, value)
    
    db.commit()
    db.refresh(degree)
    return degree


@router.delete("/{degree_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_degree(degree_id: int, db: Session = Depends(get_db)):
    """Delete a degree"""
    degree = db.query(models.Degree).filter(models.Degree.id == degree_id).first()
    if not degree:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Degree not found")
    
    db.delete(degree)
    db.commit()
    return None
