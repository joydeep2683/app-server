"""
CallRequest router - API endpoints for CallRequest model
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.CallRequest])
def list_call_requests(db: Session = Depends(get_db)):
    """List all call requests"""
    call_requests = db.query(models.CallRequest).all()
    return call_requests


@router.post("", response_model=schemas.CallRequest, status_code=status.HTTP_201_CREATED)
def create_call_request(call_request: schemas.CallRequestCreate, db: Session = Depends(get_db)):
    """Create a new call request"""
    # Verify educator exists
    educator = db.query(models.Educator).filter(
        models.Educator.id == call_request.educator_id
    ).first()
    if not educator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Educator not found"
        )
    
    # Verify student exists
    student = db.query(models.Student).filter(
        models.Student.id == call_request.student_id
    ).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db_call_request = models.CallRequest(**call_request.model_dump())
    db.add(db_call_request)
    db.commit()
    db.refresh(db_call_request)
    return db_call_request


@router.get("/{call_request_id}", response_model=schemas.CallRequest)
def get_call_request(call_request_id: int, db: Session = Depends(get_db)):
    """Get a specific call request by ID"""
    call_request = db.query(models.CallRequest).filter(
        models.CallRequest.id == call_request_id
    ).first()
    if not call_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call request not found")
    return call_request


@router.put("/{call_request_id}", response_model=schemas.CallRequest)
def update_call_request(call_request_id: int, call_request_update: schemas.CallRequestCreate, db: Session = Depends(get_db)):
    """Update a call request"""
    call_request = db.query(models.CallRequest).filter(
        models.CallRequest.id == call_request_id
    ).first()
    if not call_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call request not found")
    
    # Verify educator exists
    educator = db.query(models.Educator).filter(
        models.Educator.id == call_request_update.educator_id
    ).first()
    if not educator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Educator not found"
        )
    
    # Verify student exists
    student = db.query(models.Student).filter(
        models.Student.id == call_request_update.student_id
    ).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    for key, value in call_request_update.model_dump().items():
        setattr(call_request, key, value)
    
    db.commit()
    db.refresh(call_request)
    return call_request


@router.patch("/{call_request_id}", response_model=schemas.CallRequest)
def partial_update_call_request(call_request_id: int, call_request_update: schemas.CallRequestCreate, db: Session = Depends(get_db)):
    """Partially update a call request"""
    return update_call_request(call_request_id, call_request_update, db)


@router.delete("/{call_request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_call_request(call_request_id: int, db: Session = Depends(get_db)):
    """Delete a call request"""
    call_request = db.query(models.CallRequest).filter(
        models.CallRequest.id == call_request_id
    ).first()
    if not call_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call request not found")
    
    db.delete(call_request)
    db.commit()
    return None
