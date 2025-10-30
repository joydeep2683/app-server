"""
SQLAlchemy models
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Institute(Base):
    __tablename__ = "institute"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)

    # Relationship
    educator_institute = relationship("EducatorDegree", back_populates="institute")

class Area(Base):
    __tablename__ = "area"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationship
    educator_areas = relationship("EducatorArea", back_populates="area")


class Degree(Base):
    __tablename__ = "degree"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)

    # Relationship
    educator_degrees = relationship("EducatorDegree", back_populates="degree")


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    call_requests = relationship("CallRequest", back_populates="student")


class Educator(Base):
    __tablename__ = "educator"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_licensed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    licenses = relationship("EducatorLicense", back_populates="educator", cascade="all, delete-orphan")
    degrees = relationship("EducatorDegree", back_populates="educator", cascade="all, delete-orphan")
    areas = relationship("EducatorArea", back_populates="educator", cascade="all, delete-orphan")
    call_requests = relationship("CallRequest", back_populates="educator")


class EducatorLicense(Base):
    __tablename__ = "educator_license"

    id = Column(Integer, primary_key=True, index=True)
    educator_id = Column(Integer, ForeignKey("educator.id"), nullable=False)
    registration_number = Column(String(255), nullable=True)
    issuing_authority = Column(String(255), nullable=True)

    # Relationship
    educator = relationship("Educator", back_populates="licenses")


class EducatorDegree(Base):
    __tablename__ = "educator_degree"

    id = Column(Integer, primary_key=True, index=True)
    educator_id = Column(Integer, ForeignKey("educator.id"), nullable=False)
    degree_id = Column(Integer, ForeignKey("degree.id"), nullable=False)
    institute_id = Column(Integer, ForeignKey("institute.id"), nullable=True)

    # Relationships
    educator = relationship("Educator", back_populates="degrees")
    degree = relationship("Degree", back_populates="educator_degrees")
    institute = relationship("Institute", back_populates="educator_institute")


class EducatorArea(Base):
    __tablename__ = "educator_area"

    id = Column(Integer, primary_key=True, index=True)
    educator_id = Column(Integer, ForeignKey("educator.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)

    # Relationships
    educator = relationship("Educator", back_populates="areas")
    area = relationship("Area", back_populates="educator_areas")


class CallRequest(Base):
    __tablename__ = "call_requests"

    id = Column(Integer, primary_key=True, index=True)
    educator_id = Column(Integer, ForeignKey("educator.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    educator = relationship("Educator", back_populates="call_requests")
    student = relationship("Student", back_populates="call_requests")
