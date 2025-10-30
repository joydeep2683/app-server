# Migration Guide: Django to FastAPI

## Overview
This document outlines the migration from Django REST Framework to FastAPI with SQLAlchemy.

## Technology Stack Changes

### Before (Django)
- **Framework**: Django 5.2.7
- **API Framework**: Django REST Framework
- **ORM**: Django ORM
- **Validation**: DRF Serializers
- **Server**: Django development server / Gunicorn

### After (FastAPI)
- **Framework**: FastAPI 0.104.1
- **API Framework**: FastAPI (native)
- **ORM**: SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn 0.24.0

## File Structure Comparison

### Before
```
app-server/
├── manage.py
├── appserver/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── area/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── migrations/
├── degree/
├── students/
├── educators/
├── calls/
└── core/
```

### After
```
app-server/
├── main.py
├── init_db.py
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    └── routers/
        ├── __init__.py
        ├── area.py
        ├── degree.py
        ├── student.py
        ├── educator.py
        └── call_request.py
```

## Code Examples

### Model Definition

#### Django (Before)
```python
# area/models.py
from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'area'
```

#### FastAPI + SQLAlchemy (After)
```python
# app/models.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Area(Base):
    __tablename__ = "area"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
```

### View/Router Definition

#### Django (Before)
```python
# area/views.py
from rest_framework import generics
from .models import Area
from .serializers import AreaSerializer

class AreaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
```

#### FastAPI (After)
```python
# app/routers/area.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("", response_model=List[schemas.Area])
def list_areas(db: Session = Depends(get_db)):
    areas = db.query(models.Area).all()
    return areas

@router.post("", response_model=schemas.Area)
def create_area(area: schemas.AreaCreate, db: Session = Depends(get_db)):
    db_area = models.Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area
```

### Schema/Serializer Definition

#### Django (Before)
```python
# area/serializers.py
from rest_framework import serializers
from .models import Area

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']
```

#### Pydantic (After)
```python
# app/schemas.py
from pydantic import BaseModel

class AreaBase(BaseModel):
    name: str

class AreaCreate(AreaBase):
    pass

class Area(AreaBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
```

## Key Improvements

### 1. Performance
- FastAPI is significantly faster than Django
- Async/await support for better concurrency
- Automatic request/response validation

### 2. Developer Experience
- Automatic interactive API documentation (Swagger UI)
- Type hints throughout the codebase
- Better IDE support and autocomplete

### 3. Code Quality
- More explicit and readable code
- Dependency injection pattern
- Cleaner separation of concerns

### 4. API Documentation
- Auto-generated OpenAPI 3.0 schema
- Interactive documentation at /docs
- Alternative documentation at /redoc

## Running the Application

### Before (Django)
```bash
python manage.py runserver
```

### After (FastAPI)
```bash
uvicorn main:app --reload
```

## Database Operations

### Before (Django)
```bash
python manage.py makemigrations
python manage.py migrate
```

### After (FastAPI)
```bash
python init_db.py  # Creates all tables
# Or tables are auto-created on first run
```

## Preserved Functionality

All original functionality has been preserved:
- ✅ CRUD operations for all models
- ✅ Bulk create for Area and Degree
- ✅ Relationships between models
- ✅ Database table names and structure
- ✅ PostgreSQL database support
- ✅ Environment variable configuration

## Migration Benefits

1. **Better Performance**: FastAPI is one of the fastest Python frameworks
2. **Modern Stack**: Built on modern Python features (type hints, async)
3. **Auto Documentation**: OpenAPI documentation generated automatically
4. **Type Safety**: Pydantic provides runtime type validation
5. **Smaller Footprint**: Fewer dependencies and simpler structure
6. **Developer Productivity**: Better IDE support and faster development
