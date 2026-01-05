from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import AISystem, ComplianceRequirement, RiskCategory, ComplianceStatus
from pydantic import BaseModel, Field
from typing import List, Optional

# Pydantic schemas for request/response validation
class AISystemCreate(BaseModel):
    """Schema for creating a new AI system"""
    name: str = Field(..., min_length=1, max_length=255, description="Name of the AI system")
    description: Optional[str] = Field(None, description="Detailed description")
    risk_category: RiskCategory = Field(..., description="EU AI Act risk category")
    organization: Optional[str] = Field(None, max_length=255)
    department: Optional[str] = Field(None, max_length=255)
    owner_email: Optional[str] = Field(None, max_length=255)
    
    class Config:
        use_enum_values = True

class AISystemResponse(BaseModel):
    """Schema for AI system responses"""
    id: str
    name: str
    description: Optional[str]
    risk_category: str
    organization: Optional[str]
    department: Optional[str]
    owner_email: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

app = FastAPI(
    title="WatchGraph API",
    description="Continuous AI Compliance Monitoring Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("🚀 WatchGraph API started successfully!")

@app.get("/")
async def home():
    """Main endpoint for WatchGraph continuous AI compliance monitoring"""
    return {
        "message": "Hello from WatchGraph - Continuous AI Compliance Monitoring Platform",
        "company": "Hexidus",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "description": "Real-time monitoring and compliance checking for AI systems"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WatchGraph API",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "operational"
    }

@app.get("/version")
async def version():
    """Version information endpoint"""
    return {
        "service": "WatchGraph",
        "version": "1.0.0",
        "platform": "Continuous AI Compliance Monitoring",
        "company": "Hexidus",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# AI Systems Endpoints
@app.post("/api/systems", response_model=AISystemResponse, status_code=201)
async def create_ai_system(
    system: AISystemCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new AI system for compliance monitoring
    
    - **name**: Name of the AI system (required)
    - **risk_category**: EU AI Act risk category (required)
        - unacceptable: Prohibited AI systems
        - high: High-risk AI systems
        - limited: Limited risk (transparency obligations)
        - minimal: Minimal/no risk
    - **description**: Detailed description of the system
    - **organization**: Organization name
    - **department**: Department or team
    - **owner_email**: Contact email for the system owner
    """
    # Create new AI system
    db_system = AISystem(
        name=system.name,
        description=system.description,
        risk_category=system.risk_category,
        organization=system.organization,
        department=system.department,
        owner_email=system.owner_email
    )
    
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    
    # Convert to response format
    return AISystemResponse(
        id=db_system.id,
        name=db_system.name,
        description=db_system.description,
        risk_category=db_system.risk_category.value,
        organization=db_system.organization,
        department=db_system.department,
        owner_email=db_system.owner_email,
        created_at=db_system.created_at.isoformat(),
        updated_at=db_system.updated_at.isoformat()
    )

@app.get("/api/systems", response_model=List[AISystemResponse])
async def list_ai_systems(db: Session = Depends(get_db)):
    """
    List all registered AI systems
    
    Returns a list of all AI systems being monitored for compliance.
    """
    systems = db.query(AISystem).all()
    
    return [
        AISystemResponse(
            id=s.id,
            name=s.name,
            description=s.description,
            risk_category=s.risk_category.value,
            organization=s.organization,
            department=s.department,
            owner_email=s.owner_email,
            created_at=s.created_at.isoformat(),
            updated_at=s.updated_at.isoformat()
        )
        for s in systems
    ]

@app.get("/api/systems/{system_id}", response_model=AISystemResponse)
async def get_ai_system(system_id: str, db: Session = Depends(get_db)):
    """
    Get details of a specific AI system
    
    - **system_id**: UUID of the AI system
    """
    system = db.query(AISystem).filter(AISystem.id == system_id).first()
    
    if not system:
        raise HTTPException(status_code=404, detail="AI system not found")
    
    return AISystemResponse(
        id=system.id,
        name=system.name,
        description=system.description,
        risk_category=system.risk_category.value,
        organization=system.organization,
        department=system.department,
        owner_email=system.owner_email,
        created_at=system.created_at.isoformat(),
        updated_at=system.updated_at.isoformat()
    )

@app.get("/api/compliance")
async def compliance():
    """Future endpoint for compliance rule management"""
    return {
        "message": "Compliance Rules endpoint - Coming soon",
        "description": "Define and manage compliance rules for AI systems",
        "status": "under_development"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
