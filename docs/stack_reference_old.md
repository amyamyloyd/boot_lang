# Boot_Lang Platform - Stack Reference Document

**Last Updated:** December 19, 2024  
**Version:** 1.0.0

This document catalogs the entire Boot_Lang platform stack for AI agent consumption. It provides comprehensive technical details about endpoints, models, components, and patterns to enable automated POC implementation design.

---

## 1. STACK OVERVIEW

### Backend Framework
- **Framework:** FastAPI 0.100.0+
- **Language:** Python 3.11
- **Server:** Uvicorn with Gunicorn for production
- **Purpose:** RESTful API with real-time capabilities

### Frontend Framework
- **Framework:** React 19.2.0
- **Language:** TypeScript 4.9.5
- **Build Tool:** React Scripts 5.0.1
- **Styling:** Tailwind CSS 3.4.18
- **Purpose:** Single-page application with modern UI

### Database
- **Type:** SQLite
- **ORM:** SQLAlchemy 2.0.0+
- **File:** `boot_lang.db`
- **Purpose:** Local development and lightweight production

### AI/LLM Libraries
- **LangChain:** 0.1.0+ (conversation management, agents)
- **LangChain OpenAI:** 0.1.0+ (GPT integration)
- **LangChain Community:** 0.1.0+ (document loaders, vector stores)
- **FAISS:** 1.7.0+ (vector similarity search)
- **OpenAI API:** GPT-3.5-turbo, GPT-4o (with vision)

### Key Dependencies
```python
# Core Framework
fastapi>=0.100.0
uvicorn[standard]>=0.20.0
gunicorn>=20.1.0
python-multipart>=0.0.5

# AI/LLM
langchain>=0.1.0
langchain-openai>=0.1.0
langserve>=0.1.0
langchain-community>=0.1.0
faiss-cpu>=1.7.0
tiktoken>=0.5.0

# Database & Auth
sqlalchemy>=2.0.0
bcrypt>=4.0.0
python-jose[cryptography]>=3.3.0
passlib>=1.7.4

# Document Processing
pypdf>=3.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

### Deployment Platform
- **Development:** Local (localhost:8000 backend, localhost:3000 frontend)
- **Production:** Azure Static Web Apps + Azure App Service
- **CORS Origins:** 
  - `http://localhost:3000`
  - `http://localhost:5173`
  - `https://proud-smoke-02a8bab0f.1.azurestaticapps.net`
  - `https://boot-lang-gscvbveeg3dvgefh.eastus2-01.azurewebsites.net`

---

## 2. BACKEND ENDPOINTS CATALOG

### Authentication Endpoints (`/api/auth`)

#### POST /api/auth/register
**Purpose:** Register new user account  
**Auth Required:** No  
**Request Body:**
```json
{
  "username": "string (3-50 chars)",
  "password": "string (min 4 chars)",
  "email": "string (optional, max 100 chars)"
}
```
**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "token": "jwt_token_string",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "is_admin": false
  }
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123","email":"test@example.com"}'
```

#### POST /api/auth/login
**Purpose:** Authenticate user and return JWT token  
**Auth Required:** No  
**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "jwt_token_string",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "is_admin": false
  }
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}'
```

#### GET /api/auth/me
**Purpose:** Get current authenticated user information  
**Auth Required:** Yes (Bearer token)  
**Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_admin": false,
  "created_at": "2024-12-19T10:30:00"
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer jwt_token_string"
```

### User Management Endpoints (`/api/user`)

#### PUT /api/user/password
**Purpose:** Change user's password  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "current_password": "string",
  "new_password": "string (min 4 chars)"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```
**Example:**
```bash
curl -X PUT http://localhost:8000/api/user/password \
  -H "Authorization: Bearer jwt_token_string" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"oldpass","new_password":"newpass123"}'
```

#### PUT /api/user/profile
**Purpose:** Update user profile (username, email)  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "username": "string (optional, 3-50 chars)",
  "email": "string (optional, max 100 chars)"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "newusername",
    "email": "newemail@example.com",
    "is_admin": false
  }
}
```
**Example:**
```bash
curl -X PUT http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer jwt_token_string" \
  -H "Content-Type: application/json" \
  -d '{"username":"newusername","email":"newemail@example.com"}'
```

### Admin Endpoints (`/api/admin`)

#### GET /api/admin/users
**Purpose:** List all users (admin only)  
**Auth Required:** Yes (admin token)  
**Response:**
```json
{
  "success": true,
  "message": "Found 3 users",
  "users": [
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "is_admin": false,
      "created_at": "2024-12-19T10:30:00",
      "updated_at": "2024-12-19T10:30:00"
    }
  ]
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer admin_jwt_token"
```

#### POST /api/admin/users
**Purpose:** Create new user (admin only)  
**Auth Required:** Yes (admin token)  
**Request Body:**
```json
{
  "username": "string (3-50 chars)",
  "password": "string (min 4 chars)",
  "email": "string (optional)",
  "is_admin": false
}
```
**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "id": 2,
    "username": "newuser",
    "email": "newuser@example.com",
    "is_admin": false
  }
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer admin_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"pass123","email":"newuser@example.com","is_admin":false}'
```

#### DELETE /api/admin/users/{user_id}
**Purpose:** Delete user (admin only, cannot delete self)  
**Auth Required:** Yes (admin token)  
**Response:**
```json
{
  "success": true,
  "message": "User 'username' deleted successfully"
}
```
**Example:**
```bash
curl -X DELETE http://localhost:8000/api/admin/users/2 \
  -H "Authorization: Bearer admin_jwt_token"
```

#### PUT /api/admin/users/{user_id}/reset-password
**Purpose:** Reset user's password (admin only)  
**Auth Required:** Yes (admin token)  
**Request Body:**
```json
{
  "new_password": "string (min 4 chars)"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Password reset successfully for user 'username'"
}
```
**Example:**
```bash
curl -X PUT http://localhost:8000/api/admin/users/2/reset-password \
  -H "Authorization: Bearer admin_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{"new_password":"newpass123"}'
```

### POC Agent Endpoints (`/api/poc`)

#### POST /api/poc/upload
**Purpose:** Upload document for POC context (PDF, TXT, MD, PNG, JPG)  
**Auth Required:** Yes (Bearer token)  
**Request:** Multipart form data with file  
**Response:**
```json
{
  "id": 1,
  "filename": "requirements.pdf",
  "file_type": "pdf",
  "created_at": "2024-12-19T10:30:00"
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/poc/upload \
  -H "Authorization: Bearer jwt_token_string" \
  -F "file=@requirements.pdf"
```

#### GET /api/poc/documents
**Purpose:** List user's uploaded documents  
**Auth Required:** Yes (Bearer token)  
**Response:**
```json
[
  {
    "id": 1,
    "filename": "requirements.pdf",
    "file_type": "pdf",
    "created_at": "2024-12-19T10:30:00"
  }
]
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/documents \
  -H "Authorization: Bearer jwt_token_string"
```

#### DELETE /api/poc/documents/{doc_id}
**Purpose:** Delete uploaded document  
**Auth Required:** Yes (Bearer token)  
**Response:**
```json
{
  "message": "Document deleted"
}
```
**Example:**
```bash
curl -X DELETE http://localhost:8000/api/poc/documents/1 \
  -H "Authorization: Bearer jwt_token_string"
```

#### POST /api/poc/chat
**Purpose:** Chat with POC Agent  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "prompt": "string",
  "document_ids": [1, 2],
  "conversation_history": {
    "conversation_id": "conv_user123_20241219_103000"
  }
}
```
**Response:**
```json
{
  "response": "Agent response text",
  "conversation_id": "conv_user123_20241219_103000",
  "agent_state": {
    "stage": "requirements_gathering",
    "requirements": {}
  },
  "next_action": "continue_chat"
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/poc/chat \
  -H "Authorization: Bearer jwt_token_string" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"I want to build a task management app"}'
```

#### POST /api/poc/generate
**Purpose:** Generate POC structure with documentation  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "requirements": {
    "goal": "Task management app",
    "users": "Small teams",
    "frontend": {"pages": ["dashboard", "task_list"]},
    "backend": {"endpoints": ["POST /tasks", "GET /tasks"]},
    "database": {"tables": ["tasks"]}
  }
}
```
**Response:**
```json
{
  "poc_id": "task_management_app",
  "poc_name": "Task Management App",
  "directory": "/path/to/pocs/user123/task_management_app",
  "files": ["poc_desc.md", "requirements.md", "phase_1_frontend.md", "phase_2_backend.md", "phase_3_database.md"]
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/poc/generate \
  -H "Authorization: Bearer jwt_token_string" \
  -H "Content-Type: application/json" \
  -d '{"requirements":{"goal":"Task management app","users":"Small teams"}}'
```

#### GET /api/poc/list
**Purpose:** List user's generated POCs  
**Auth Required:** Yes (Bearer token)  
**Response:**
```json
[
  {
    "id": 1,
    "poc_id": "task_management_app",
    "poc_name": "Task Management App",
    "description": "Simple task tracker for teams",
    "created_at": "2024-12-19T10:30:00"
  }
]
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/list \
  -H "Authorization: Bearer jwt_token_string"
```

#### GET /api/poc/{poc_id}/files
**Purpose:** Get file tree for a POC  
**Auth Required:** Yes (Bearer token)  
**Response:**
```json
{
  "poc_id": "task_management_app",
  "directory": "/path/to/pocs/user123/task_management_app",
  "files": ["poc_desc.md", "requirements.md", "phase_1_frontend.md", "phase_2_backend.md", "phase_3_database.md", "wireframes/", "generated/"]
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/task_management_app/files \
  -H "Authorization: Bearer jwt_token_string"
```

#### GET /api/poc/{poc_id}/download
**Purpose:** Download POC as ZIP file  
**Auth Required:** Yes (Bearer token)  
**Response:** ZIP file download  
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/task_management_app/download \
  -H "Authorization: Bearer jwt_token_string" \
  -o task_management_app.zip
```

#### PUT /api/poc/{poc_id}/update
**Purpose:** Update POC requirements and regenerate files  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "requirements": {
    "goal": "Updated task management app",
    "users": "Large teams",
    "frontend": {"pages": ["dashboard", "task_list", "analytics"]},
    "backend": {"endpoints": ["POST /tasks", "GET /tasks", "GET /analytics"]},
    "database": {"tables": ["tasks", "analytics"]}
  }
}
```
**Response:**
```json
{
  "message": "POC updated",
  "directory": "/path/to/pocs/user123/task_management_app"
}
```
**Example:**
```bash
curl -X PUT http://localhost:8000/api/poc/task_management_app/update \
  -H "Authorization: Bearer jwt_token_string" \
  -H "Content-Type: application/json" \
  -d '{"requirements":{"goal":"Updated task management app"}}'
```

### Root Endpoints

#### GET /
**Purpose:** Health check and platform info  
**Auth Required:** No  
**Response:**
```json
{
  "message": "Boot_Lang Platform",
  "status": "running",
  "version": "1.0.0"
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/
```

---

## 3. DATABASE MODELS CATALOG

### User Model
**Table:** users  
**Purpose:** Stores user authentication and profile data  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `username`: String(50), Unique, Not Null, Indexed
- `email`: String(100), Nullable
- `password_hash`: String(255), Not Null (bcrypt hashed)
- `is_admin`: Boolean, Default=False, Not Null
- `created_at`: DateTime, Default=now(), Not Null
- `updated_at`: DateTime, Default=now(), OnUpdate=now(), Not Null

**Relationships:** None  
**Indexes:** 
- Primary key on `id`
- Unique index on `username`

### Document Model
**Table:** documents  
**Purpose:** Stores uploaded files for POC context  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: Integer, Not Null, Indexed (foreign key to users)
- `filename`: String(255), Not Null (original filename)
- `file_path`: String(500), Not Null (path to stored file)
- `content_text`: Text, Nullable (extracted text content)
- `file_type`: String(10), Not Null (pdf, txt, md, png, jpg)
- `created_at`: DateTime, Default=now(), Not Null

**Relationships:** Belongs to User via `user_id`  
**Indexes:**
- Primary key on `id`
- Index on `user_id`

### POC Model
**Table:** pocs  
**Purpose:** Stores generated proof-of-concept projects  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: Integer, Not Null, Indexed (foreign key to users)
- `poc_id`: String(100), Not Null, Indexed (friendly name)
- `poc_name`: String(255), Not Null (display name)
- `description`: Text, Nullable (POC description/goal)
- `requirements`: JSON, Nullable (captured requirements)
- `directory`: String(500), Not Null (path to POC directory)
- `created_at`: DateTime, Default=now(), Not Null

**Relationships:** Belongs to User via `user_id`  
**Indexes:**
- Primary key on `id`
- Index on `user_id`
- Index on `poc_id`
- Composite index on `user_id`, `poc_id`

### POCConversation Model
**Table:** poc_conversations  
**Purpose:** Stores conversation history with POC Agent  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `poc_id`: Integer, Nullable, Indexed (foreign key to pocs)
- `user_id`: Integer, Not Null, Indexed (foreign key to users)
- `conversation_history`: JSON, Nullable (message history)
- `langchain_memory`: JSON, Nullable (LangChain memory state)
- `created_at`: DateTime, Default=now(), Not Null

**Relationships:** 
- Belongs to User via `user_id`
- Optional belongs to POC via `poc_id`

**Indexes:**
- Primary key on `id`
- Index on `poc_id`
- Index on `user_id`

### POCPhase Model
**Table:** poc_phases  
**Purpose:** Tracks implementation phases for POCs  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `poc_id`: Integer, Not Null, Indexed (foreign key to pocs)
- `phase_number`: Integer, Not Null (1, 2, 3)
- `phase_name`: String(50), Not Null (Frontend, Backend, Database)
- `instructions_file`: String(500), Not Null (path to phase instructions)
- `status`: String(20), Default="pending", Not Null (pending, in_progress, completed)
- `created_at`: DateTime, Default=now(), Not Null

**Relationships:** Belongs to POC via `poc_id`  
**Indexes:**
- Primary key on `id`
- Index on `poc_id`

---

## 4. FRONTEND COMPONENTS CATALOG

### AdminPanel Component
**File:** `src/components/AdminPanel.tsx`  
**Purpose:** Admin interface for user management  
**Props:** None (standalone page component)  
**Features:**
- Create new users with admin privileges
- List existing users in table format
- Reset user passwords
- Delete users (cannot delete self)
- Form validation and error handling
- 40/60 layout: Left panel for actions, right panel for user list

**Usage:**
```tsx
import AdminPanel from './components/AdminPanel';
<AdminPanel />
```

### Login Component
**File:** `src/components/Login.tsx`  
**Purpose:** User authentication login form  
**Props:** None (standalone page component)  
**Features:**
- Username/password form
- Form validation
- Error message display
- Loading states
- Link to registration page
- Redirects to home on successful login

**Usage:**
```tsx
import Login from './components/Login';
<Login />
```

### Register Component
**File:** `src/components/Register.tsx`  
**Purpose:** User registration form  
**Props:** None (standalone page component)  
**Features:**
- Username, password, email form
- Password strength validation
- Form validation
- Error message display
- Loading states
- Link to login page
- Redirects to home on successful registration

**Usage:**
```tsx
import Register from './components/Register';
<Register />
```

### POCBuilder Component
**File:** `src/components/POCBuilder.tsx`  
**Purpose:** Main POC creation interface with chat and document management  
**Props:** None (standalone page component)  
**Features:**
- 40/60 layout: Left panel for documents/POCs, right panel for chat
- Document upload (PDF, TXT, MD, PNG, JPG)
- Document list with delete functionality
- POC list with selection
- Real-time chat with POC Agent
- Message history with timestamps
- Typing indicators
- POC generation button
- File upload with drag-and-drop styling

**Usage:**
```tsx
import POCBuilder from './components/POCBuilder';
<POCBuilder />
```

### UserSettings Component
**File:** `src/components/UserSettings.tsx`  
**Purpose:** User profile management  
**Props:** None (standalone page component)  
**Features:**
- Update username and email
- Change password with current password verification
- Form validation
- Error and success message display
- Loading states

**Usage:**
```tsx
import UserSettings from './components/UserSettings';
<UserSettings />
```

### AuthContext Context
**File:** `src/contexts/AuthContext.tsx`  
**Purpose:** Global authentication state management  
**Interface:**
```tsx
interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  updateUser: (user: User) => void;
}
```
**Features:**
- JWT token management
- User state persistence in localStorage
- Admin role checking
- Login/logout functionality
- User profile updates

**Usage:**
```tsx
import { useAuth } from './contexts/AuthContext';
const { user, isAuthenticated, login, logout } = useAuth();
```

---

## 5. AUTHENTICATION & MIDDLEWARE

### Authentication Mechanism
- **Type:** JWT (JSON Web Tokens)
- **Algorithm:** HS256
- **Expiration:** 24 hours (configurable via `JWT_EXPIRATION_HOURS`)
- **Secret Key:** Configurable via `JWT_SECRET_KEY` environment variable
- **Password Hashing:** bcrypt with salt

### Token Management
```python
# Creating tokens
from auth_utils import create_access_token
token = create_access_token(data={
    "sub": str(user.id),
    "username": user.username,
    "is_admin": user.is_admin
})

# Validating tokens
from auth_utils import decode_access_token
payload = decode_access_token(token)
if payload:
    user_id = payload.get("sub")
```

### Protecting Endpoints
```python
from auth import get_current_user
from fastapi import Depends

@app.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id}
```

### Admin-Only Endpoints
```python
from admin import get_admin_user

@app.get("/admin-only")
async def admin_endpoint(admin_user: User = Depends(get_admin_user)):
    return {"admin": admin_user.username}
```

### Frontend Token Handling
```typescript
// Setting token
import { setToken } from '../utils/auth';
setToken(token);

// Getting auth header
import { getAuthHeader } from '../utils/auth';
const headers = getAuthHeader(); // Returns { Authorization: `Bearer ${token}` }
```

### Password Security
- **Hashing:** bcrypt with automatic salt generation
- **Validation:** Minimum 4 characters
- **Verification:** Secure comparison using bcrypt.checkpw()

---

## 6. FILE UPLOAD PATTERNS

### Upload Endpoint
- **Route:** `POST /api/poc/upload`
- **Content-Type:** `multipart/form-data`
- **Supported Types:** PDF, TXT, MD, PNG, JPG, JPEG
- **Size Limits:** Not explicitly set (handled by FastAPI/Uvicorn defaults)
- **Storage Location:** `uploads/{user_id}/{timestamp}_{filename}`

### File Processing
```python
# Document loading and processing
agent = POCAgent()
docs = agent.load_document(file_path, file_ext)
agent.create_vector_store(docs, str(user_id))

# Image analysis (PNG, JPG)
analysis = agent.analyze_wireframe(image_path)
```

### Adding File Upload to New Endpoints
```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["pdf", "txt", "md", "png", "jpg"]
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
```

### Access Patterns
- **List:** `GET /api/poc/documents`
- **Delete:** `DELETE /api/poc/documents/{doc_id}`
- **Download:** Files stored in `uploads/{user_id}/` directory

---

## 7. DATABASE PATTERNS

### Creating New Tables
```python
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class NewModel(Base):
    __tablename__ = "new_table"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

### Database Initialization
```python
from database import init_db
init_db()  # Creates all tables defined in Base.metadata
```

### Session Management
```python
from database import get_db
from sqlalchemy.orm import Session

@app.get("/endpoint")
async def endpoint(db: Session = Depends(get_db)):
    # Use db session
    users = db.query(User).all()
    return users
```

### Query Examples
```python
# Create
new_user = User(username="test", password_hash="hash")
db.add(new_user)
db.commit()
db.refresh(new_user)

# Read
user = db.query(User).filter(User.username == "test").first()
users = db.query(User).all()

# Update
user.email = "new@email.com"
db.commit()

# Delete
db.delete(user)
db.commit()
```

### Transaction Handling
```python
try:
    # Database operations
    db.add(new_record)
    db.commit()
except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

---

## 8. DIRECTORY STRUCTURE CONVENTIONS

```
/root
  /frontend
    /src
      /components          # React components
      /contexts           # React contexts (AuthContext)
      /utils              # Utility functions
      App.tsx             # Main app component
      config.ts           # API configuration
    package.json
    tailwind.config.js
  /backend (root)
    app.py                # Main FastAPI app
    database.py           # SQLAlchemy models and DB setup
    auth.py              # Authentication endpoints
    auth_utils.py         # Auth utilities (JWT, bcrypt)
    admin.py              # Admin endpoints
    user_management.py    # User profile endpoints
    poc_api.py           # POC Agent endpoints
    /agents
      poc_agent.py        # Main POC Agent implementation
      poc_agent_prompts.json # Agent prompt configuration
    /pocs
      /{user_id}
        /{poc_name}       # Generated POC directories
          poc_desc.md
          requirements.md
          phase_1_frontend.md
          phase_2_backend.md
          phase_3_database.md
          /wireframes
          /generated
    /uploads
      /{user_id}          # User uploaded files
    /vector_stores
      /{user_id}          # FAISS vector stores per user
        faiss_index/
    requirements.txt
    .env
    boot_lang.db          # SQLite database
```

### Naming Conventions
- **POC Directories:** `pocs/{user_id}/{friendly_name}`
- **Upload Directories:** `uploads/{user_id}/`
- **Vector Stores:** `vector_stores/{user_id}/faiss_index/`
- **Friendly Names:** Generated from user description (e.g., "customer_feedback_tracker")

---

## 9. DEPLOYMENT CONFIGURATION

### Environment Variables Required
```bash
# Backend Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Database Configuration
SQLite (no additional config needed)

# LLM Keys
PERPLEXITY_API_KEY
OPENAI_API_KEY

# LangSmith Configuration (Optional)
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=boot_lang

# Development Settings
DEBUG=True
LOG_LEVEL=INFO

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Build Commands
```bash
# Frontend
cd frontend
npm install
npm run build

# Backend (no build needed, Python)
pip install -r requirements.txt
```

### Start Commands
```bash
# Development
# Frontend
cd frontend && npm start

# Backend
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Production
# Frontend (served by Azure Static Web Apps)
# Backend
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Azure Deployment
- **Frontend:** Azure Static Web Apps
- **Backend:** Azure App Service
- **Database:** SQLite file (persistent storage)
- **CORS:** Pre-configured for Azure domains

---

## 10. LANGCHAIN INTEGRATION PATTERNS

### Available LangChain Components
- **ChatOpenAI:** GPT-3.5-turbo, GPT-4o (with vision)
- **OpenAIEmbeddings:** For document vectorization
- **ConversationChain:** For conversational AI
- **ConversationBufferMemory:** For conversation persistence
- **FAISS:** Vector store for RAG
- **PyPDFLoader, TextLoader:** Document loaders
- **RecursiveCharacterTextSplitter:** Text chunking
- **PydanticOutputParser:** Structured output parsing

### Agent Structure
```python
class POCAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation_chain = ConversationChain(llm=self.llm, memory=self.memory)
        self.embeddings = OpenAIEmbeddings()
        self.vector_stores = {}  # Per-user vector stores
```

### Memory Management
```python
# Save conversation state
def save_conversation(self):
    messages = []
    for msg in self.memory.chat_memory.messages:
        messages.append({
            "type": msg.type,
            "content": msg.content
        })
    return {
        "conversation_id": self.conversation_id,
        "memory": {"messages": messages}
    }

# Load conversation state
def load_conversation(self, saved_state):
    for msg in saved_state["memory"]["messages"]:
        if msg["type"] == "human":
            self.memory.chat_memory.add_user_message(msg["content"])
        elif msg["type"] == "ai":
            self.memory.chat_memory.add_ai_message(msg["content"])
```

### Prompt Template Patterns
```python
# System prompt injection
system_prompt = self.get_system_prompt()
self.memory.chat_memory.add_ai_message(
    f"[SYSTEM CONTEXT: {system_prompt}] Hello! I'm here to help..."
)

# Structured output parsing
parser = PydanticOutputParser(pydantic_object=RequirementsSchema)
prompt = PromptTemplate(
    input_variables=["conversation", "format_instructions"],
    template="Extract requirements: {conversation}\n{format_instructions}"
)
chain = prompt | self.llm | parser
```

### RAG Implementation
```python
# Document loading and chunking
docs = self.load_document(file_path, file_type)
chunks = self.text_splitter.split_documents(docs)

# Vector store creation
vector_store = FAISS.from_documents(chunks, self.embeddings)
vector_store.save_local(vector_store_path)

# Context retrieval
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.get_relevant_documents(query)
```

---

## 11. AVAILABLE TOOLS & UTILITIES

### Authentication Utilities (`auth_utils.py`)
```python
# Password hashing
hash_password(password: str) -> str
verify_password(plain_password: str, hashed_password: str) -> bool

# JWT token management
create_access_token(data: Dict[str, Any]) -> str
decode_access_token(token: str) -> Optional[Dict[str, Any]]

# Password validation
validate_password_strength(password: str) -> tuple[bool, Optional[str]]
```

### Database Utilities (`database.py`)
```python
# Session management
get_db() -> Generator[SessionLocal, None, None]

# Database initialization
init_db() -> None
```

### Frontend Utilities (`src/utils/auth.ts`)
```typescript
// Token management
setToken(token: string): void
getToken(): string | null
clearAuth(): void

// User management
setUser(user: User): void
getUser(): User | null

// Auth headers
getAuthHeader(): { Authorization: string }
```

### POC Agent Utilities
```python
# Document processing
load_document(file_path: str, file_type: str) -> List[Document]
create_vector_store(documents: List[Document], user_id: str) -> FAISS
retrieve_context(query: str, user_id: str) -> str

# Requirements management
gather_requirements(conversation: str) -> Dict[str, Any]
validate_requirements_completeness(requirements: Dict[str, Any]) -> Dict[str, Any]

# POC generation
generate_poc(requirements: Dict[str, Any], user_id: str) -> Dict[str, Any]
generate_friendly_name(description: str) -> str
```

---

## 12. STYLING CONVENTIONS

### CSS Framework
- **Primary:** Tailwind CSS 3.4.18
- **Configuration:** `tailwind.config.js` (minimal configuration)
- **Build:** PostCSS with Autoprefixer

### Color Scheme
- **Primary:** Blue (`blue-600`, `blue-700`, `blue-800`)
- **Success:** Green (`green-600`, `green-700`)
- **Error:** Red (`red-600`, `red-700`)
- **Background:** Gray (`gray-50`, `gray-100`, `gray-200`)
- **Text:** Gray (`gray-700`, `gray-800`, `gray-900`)

### Common Utility Classes
```css
/* Layout */
.min-h-screen { min-height: 100vh; }
.max-w-7xl { max-width: 80rem; }
.mx-auto { margin-left: auto; margin-right: auto; }

/* Spacing */
.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-8 { margin-bottom: 2rem; }

/* Colors */
.bg-blue-600 { background-color: #2563eb; }
.text-white { color: #ffffff; }
.text-gray-700 { color: #374151; }

/* Forms */
.border { border-width: 1px; }
.border-gray-300 { border-color: #d1d5db; }
.rounded-md { border-radius: 0.375rem; }
.focus\:ring-blue-500:focus { --tw-ring-color: #3b82f6; }
```

### Layout Patterns
- **40/60 Split:** `grid-cols-1 md:grid-cols-5` with `md:col-span-2` and `md:col-span-3`
- **Full Width:** `w-full`
- **Flex Layout:** `flex`, `flex-col`, `justify-between`, `items-center`
- **Responsive:** `md:` prefix for medium screens and up

### Responsive Breakpoints
- **Mobile:** Default (no prefix)
- **Medium:** `md:` (768px+)
- **Large:** `lg:` (1024px+)

---

## 13. ERROR HANDLING PATTERNS

### Backend Error Response Format
```python
# Standard HTTPException
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already exists"
)

# Custom error response
return {
    "success": False,
    "error": "Detailed error message",
    "code": "ERROR_CODE"
}
```

### Frontend Error Display
```tsx
// Error message component
{error && (
  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
)}

// Success message component
{success && (
  <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
    {success}
  </div>
)}
```

### Logging Configuration
- **Level:** INFO (configurable via `LOG_LEVEL`)
- **Format:** Standard Python logging
- **Location:** Console output (development)

### Common Error Scenarios
1. **Authentication Errors:** 401 Unauthorized
2. **Validation Errors:** 400 Bad Request
3. **Not Found Errors:** 404 Not Found
4. **Permission Errors:** 403 Forbidden
5. **Server Errors:** 500 Internal Server Error

---

## 14. TESTING PATTERNS

### Testing Framework
- **Backend:** pytest (not yet implemented)
- **Frontend:** Jest + React Testing Library (configured but not implemented)

### Test File Locations
- **Backend:** `test_*.py` files in root directory
- **Frontend:** `*.test.tsx` files alongside components

### Running Tests
```bash
# Backend (when implemented)
python -m pytest

# Frontend (when implemented)
cd frontend && npm test
```

### Coverage Expectations
- **Target:** 30% comment coverage (as per project rules)
- **Focus:** Public functions with docstrings
- **Documentation:** All public functions must include purpose, args, returns, exceptions, examples

---

## Summary

This stack reference documents a comprehensive POC generation platform with:

- **FastAPI backend** with JWT authentication, admin management, and POC Agent integration
- **React frontend** with TypeScript, Tailwind CSS, and modern component architecture
- **SQLite database** with SQLAlchemy ORM and structured models
- **LangChain integration** for conversational AI, RAG, and document processing
- **File upload system** supporting multiple document types including image analysis
- **Azure deployment** configuration for production hosting

The platform enables users to upload documents, have conversations with an AI agent, and generate structured POC implementations with phased documentation ready for development.

**Key Gaps Identified:**
- Testing implementation (framework configured but tests not written)
- Production environment configuration details
- CI/CD pipeline documentation
- Performance monitoring and logging setup
