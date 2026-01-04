from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

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

@app.get("/api/systems")
async def systems():
    """Future endpoint for AI system registration and monitoring"""
    return {
        "message": "AI Systems endpoint - Coming soon",
        "description": "Register and monitor AI systems for compliance",
        "status": "under_development"
    }

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
