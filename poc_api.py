"""
POC Agent API endpoints.

This module provides FastAPI endpoints for interacting with the POC Agent,
including document uploads, chat conversations, and POC generation.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
from datetime import datetime

from database import get_db, Document, POC, POCConversation, POCPhase
from agents.poc_agent import POCAgent
from auth import get_current_user, User

router = APIRouter(prefix="/api/poc", tags=["poc"])

# Pydantic models for requests/responses

class ChatRequest(BaseModel):
    prompt: str
    document_ids: Optional[List[int]] = None
    conversation_history: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent_state: dict
    next_action: str

class GenerateRequest(BaseModel):
    requirements: dict

class POCResponse(BaseModel):
    poc_id: str
    poc_name: str
    directory: str
    files: List[str]

# Initialize POC Agent (singleton)
poc_agent = POCAgent()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document (PDF, TXT, MD, PNG, JPG) for POC context.
    
    The document will be stored and processed for RAG.
    """
    # Validate file type
    allowed_types = ["pdf", "txt", "md", "png", "jpg", "jpeg"]
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Create upload directory
    upload_dir = f"uploads/{current_user.id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Load and process document
    try:
        docs = poc_agent.load_document(file_path, file_ext)
        poc_agent.create_vector_store(docs, str(current_user.id))
        
        # Extract content for database
        content_text = "\n".join([doc.page_content for doc in docs])
        
    except Exception as e:
        # Clean up file if processing fails
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")
    
    # Save to database
    db_document = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        content_text=content_text[:10000],  # Limit to 10k chars
        file_type=file_ext
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return {
        "id": db_document.id,
        "filename": db_document.filename,
        "file_type": db_document.file_type,
        "created_at": db_document.created_at
    }


@router.get("/documents")
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents uploaded by current user."""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "created_at": doc.created_at
        }
        for doc in documents
    ]


@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted"}


@router.post("/chat", response_model=ChatResponse)
def chat_with_agent(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Chat with POC Agent.
    
    Processes user message and returns agent response with conversation tracking.
    """
    try:
        result = poc_agent.process_request(
            prompt=request.prompt,
            user_id=str(current_user.id),
            document_ids=request.document_ids,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.post("/generate", response_model=POCResponse)
def generate_poc(
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate POC structure with all documentation files.
    
    Creates directory structure and markdown files for implementation.
    """
    try:
        result = poc_agent.generate_poc(
            requirements=request.requirements,
            user_id=str(current_user.id)
        )
        
        # Save to database
        db_poc = POC(
            user_id=current_user.id,
            poc_id=result["poc_id"],
            poc_name=result["poc_name"],
            description=request.requirements.get("goal", ""),
            requirements=request.requirements,
            directory=result["directory"]
        )
        db.add(db_poc)
        db.commit()
        db.refresh(db_poc)
        
        # Create phase records
        phases = [
            ("phase_1_frontend", "Frontend"),
            ("phase_2_backend", "Backend"),
            ("phase_3_database", "Database")
        ]
        
        for i, (file_key, name) in enumerate(phases, 1):
            db_phase = POCPhase(
                poc_id=db_poc.id,
                phase_number=i,
                phase_name=name,
                instructions_file=os.path.join(result["directory"], f"{file_key}.md"),
                status="pending"
            )
            db.add(db_phase)
        
        db.commit()
        
        return POCResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"POC generation failed: {str(e)}")


@router.get("/list")
def list_pocs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all POCs created by current user."""
    pocs = db.query(POC).filter(POC.user_id == current_user.id).all()
    
    return [
        {
            "id": poc.id,
            "poc_id": poc.poc_id,
            "poc_name": poc.poc_name,
            "description": poc.description,
            "created_at": poc.created_at
        }
        for poc in pocs
    ]


@router.get("/{poc_id}/files")
def get_poc_files(
    poc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get file tree for a POC."""
    poc = db.query(POC).filter(
        POC.poc_id == poc_id,
        POC.user_id == current_user.id
    ).first()
    
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    
    # Get all files in POC directory
    files = []
    poc_dir = poc.directory
    
    if os.path.exists(poc_dir):
        for root, dirs, filenames in os.walk(poc_dir):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, poc_dir)
                files.append(rel_path)
    
    return {
        "poc_id": poc.poc_id,
        "directory": poc.directory,
        "files": files
    }


@router.get("/{poc_id}/download")
def download_poc(
    poc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download POC as ZIP file."""
    poc = db.query(POC).filter(
        POC.poc_id == poc_id,
        POC.user_id == current_user.id
    ).first()
    
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    
    # Create ZIP file
    import zipfile
    zip_filename = f"{poc.poc_id}.zip"
    zip_path = f"/tmp/{zip_filename}"
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(poc.directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(poc.directory))
                zipf.write(file_path, arcname)
    
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=zip_filename
    )


@router.put("/{poc_id}/update")
def update_poc(
    poc_id: str,
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update POC requirements and regenerate phase files."""
    poc = db.query(POC).filter(
        POC.poc_id == poc_id,
        POC.user_id == current_user.id
    ).first()
    
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    
    # Update requirements
    poc.requirements = request.requirements
    poc.description = request.requirements.get("goal", poc.description)
    
    # Regenerate phase files
    try:
        result = poc_agent.generate_poc(
            requirements=request.requirements,
            user_id=str(current_user.id)
        )
        
        db.commit()
        
        return {"message": "POC updated", "directory": result["directory"]}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"POC update failed: {str(e)}")

