"""
FastAPI main application file
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine
from app.models import Base
from app.routers import area, degree, student, educator, call_request


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="App Server API",
    description="FastAPI application with SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(area.router, prefix="/api/v1/area", tags=["area"])
app.include_router(degree.router, prefix="/api/v1/degree", tags=["degree"])
app.include_router(student.router, prefix="/api/v1/students", tags=["students"])
app.include_router(educator.router, prefix="/api/v1/educators", tags=["educators"])
app.include_router(call_request.router, prefix="/api/v1/calls", tags=["calls"])

@app.get("/")
async def root():
    return {"message": "Welcome to App Server API"}
