# app.py
import os
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables FIRST before any other imports
load_dotenv()

# Import database initialization
from database import init_db

# Import routers
from auth import router as auth_router
from user_management import router as user_router
from admin import router as admin_router
from poc_api import router as poc_router
from tenant.tenant_1.poc_idea_1.backend.routes import router as t1_poc1_router

app = FastAPI(title="Boot_Lang Platform")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup."""
    init_db()
    print("✓ Application started, database initialized")

# CORS - pre-configured for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://proud-smoke-02a8bab0f.1.azurestaticapps.net",  # Azure Static Web App
        "https://boot-lang-gscvbveeg3dvgefh.eastus2-01.azurewebsites.net",  # Azure App Service
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(poc_router)
app.include_router(t1_poc1_router, prefix="/api/tenant_1/poc_idea_1", tags=["tenant_1"])

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    error: Optional[str] = None

class POCRequest(BaseModel):
    description: str
    user_id: str

class POCResponse(BaseModel):
    success: bool
    poc_id: Optional[str] = None
    poc_structure: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Boot_Lang Platform",
        "status": "running",
        "version": "1.0.0"
    }

# Login endpoint
@app.post("/api/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Simple auth endpoint - expand with real JWT/bcrypt later
    """
    # TODO: Replace with real auth
    if request.username and request.password:
        return LoginResponse(
            success=True,
            token="dummy_token_for_now"
        )
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# POC Agent endpoint
@app.post("/api/poc/create", response_model=POCResponse)
async def create_poc(request: POCRequest):
    """
    POC Agent: Takes user description, generates POC structure
    """
    try:
        from agents.poc_agent import POCAgent
        
        agent = POCAgent()
        result = agent.create_poc(request.description, request.user_id)
        
        return POCResponse(
            success=True,
            poc_id=result["poc_id"],
            poc_structure=result["structure"]
        )
    
    except Exception as e:
        return POCResponse(
            success=False,
            error=str(e)
        )

# List POCs
@app.get("/api/poc/list")
async def list_pocs(user_id: str):
    """
    List all POCs for a user
    """
    # TODO: Implement with database
    return {"pocs": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)