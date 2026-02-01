from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Text, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, date
import enum
import uuid

Base = declarative_base()

class RiskCategory(str, enum.Enum):
    """EU AI Act Risk Categories (Article 6)"""
    UNACCEPTABLE = "unacceptable"  # Prohibited AI systems
    HIGH = "high"                   # High-risk AI systems
    LIMITED = "limited"             # Limited risk (transparency obligations)
    MINIMAL = "minimal"             # Minimal/no risk

class ComplianceStatus(str, enum.Enum):
    """Compliance status for requirements"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NON_COMPLIANT = "non_compliant"

class EvidenceStatus(str, enum.Enum):
    """Status for evidence lifecycle"""
    CURRENT = "current"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"
    ARCHIVED = "archived"

class AISystem(Base):
    """AI System being monitored for compliance"""
    __tablename__ = "ai_systems"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    risk_category = Column(Enum(RiskCategory), nullable=False)
    
    # Metadata
    organization = Column(String(255))
    department = Column(String(255))
    owner_email = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requirements = relationship("RequirementMapping", back_populates="ai_system", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="ai_system", cascade="all, delete-orphan")

class ComplianceRequirement(Base):
    """EU AI Act Compliance Requirements"""
    __tablename__ = "compliance_requirements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    article = Column(String(50), nullable=False)  # e.g., "Article 9"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Applicable risk categories
    applies_to = Column(JSON)  # List of risk categories this requirement applies to
    
    # Relationships
    mappings = relationship("RequirementMapping", back_populates="requirement")

class RequirementMapping(Base):
    """Maps requirements to AI systems with compliance status"""
    __tablename__ = "requirement_mappings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ai_system_id = Column(String(36), ForeignKey("ai_systems.id"), nullable=False)
    requirement_id = Column(String(36), ForeignKey("compliance_requirements.id"), nullable=False)
    
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.NOT_STARTED)
    notes = Column(Text)
    updated_by = Column(String(255), nullable=True)  # Email of who updated it
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ai_system = relationship("AISystem", back_populates="requirements")
    requirement = relationship("ComplianceRequirement", back_populates="mappings")
    evidence = relationship("Evidence", back_populates="requirement_mapping")

class Evidence(Base):
    """Evidence/documentation supporting compliance - stored in S3"""
    __tablename__ = "evidence"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ai_system_id = Column(String(36), ForeignKey("ai_systems.id"), nullable=False)
    requirement_mapping_id = Column(String(36), ForeignKey("requirement_mappings.id"), nullable=True)
    
    # File metadata (S3 storage)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, png, jpg, xlsx, docx, csv
    file_size = Column(Integer, nullable=False)      # bytes
    s3_key = Column(String(500), nullable=False)     # Full S3 object path
    
    # Legacy fields (for backward compatibility)
    title = Column(String(255), nullable=True)
    file_url = Column(String(500), nullable=True)
    
    # Description
    description = Column(Text, nullable=True)
    
    # Evidence lifecycle
    status = Column(Enum(EvidenceStatus), default=EvidenceStatus.CURRENT)
    expiration_date = Column(Date, nullable=True)  # When evidence expires
    
    # Tracking
    uploaded_by = Column(String(255), nullable=True)  # Email of uploader
    
    # Soft delete
    deleted_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ai_system = relationship("AISystem", back_populates="evidence")
    requirement_mapping = relationship("RequirementMapping", back_populates="evidence")