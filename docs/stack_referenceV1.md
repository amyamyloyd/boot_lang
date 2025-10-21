# Boot_Lang Platform - Stack Reference Document

**Last Updated:** October 9, 2025  
**Purpose:** Comprehensive stack documentation for AI agents and developers

---

## 1. STACK OVERVIEW

### Core Technologies
- **Backend Framework:** FastAPI 0.100.0+ (Python 3.11)
- **Frontend Framework:** React 18 with TypeScript
- **Database:** SQLite 3 with SQLAlchemy 2.0+ ORM
- **Styling:** Tailwind CSS
- **AI/LLM:** LangChain 0.1.0+, OpenAI GPT-3.5-turbo/GPT-4
- **Authentication:** JWT tokens (python-jose) + bcrypt password hashing
- **Deployment:** Azure Static Web Apps (frontend) + Azure App Service (backend)

### Key Dependencies
```
fastapi>=0.100.0
uvicorn[standard]>=0.20.0
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-community>=0.1.0
faiss-cpu>=1.7.0
sqlalchemy>=2.0.0
bcrypt>=4.0.0
python-jose[cryptography]>=3.3.0
pypdf>=3.0.0
tiktoken>=0.5.0
```

### Application Architecture
- **Backend Port:** 8000
- **Frontend Port:** 3000
- **Database File:** `boot_lang.db` (SQLite)
- **Virtual Environment:** `/venv` (Python 3.11)

---

## 2. BACKEND ENDPOINTS CATALOG

### Authentication Endpoints (`/api/auth`)

#### POST /api/auth/register
**Purpose:** Register a new user account  
**Auth Required:** No  
**Request Body:**
```json
{
  "username": "string (3-50 chars)",
  "password": "string (min 4 chars)",
  "email": "string (optional)"
}
```
**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "token": "eyJhbGci...",
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
**Purpose:** Authenticate user and receive JWT token  
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
  "token": "eyJhbGci...",
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
**Purpose:** Get current authenticated user's information  
**Auth Required:** Yes (Bearer token)  
**Request:** None  
**Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_admin": false,
  "created_at": "2025-10-09T12:00:00"
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer eyJhbGci..."
```

---

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
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"current_password":"oldpass","new_password":"newpass123"}'
```

#### PUT /api/user/profile
**Purpose:** Update user profile (username/email)  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "username": "string (optional, 3-50 chars)",
  "email": "string (optional)"
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
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"username":"newname","email":"new@example.com"}'
```

---

### Admin Endpoints (`/api/admin`)

#### GET /api/admin/users
**Purpose:** List all users (admin only)  
**Auth Required:** Yes (admin token)  
**Request:** None  
**Response:**
```json
{
  "success": true,
  "message": "Found 5 users",
  "users": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "is_admin": true,
      "created_at": "2025-10-01T10:00:00",
      "updated_at": "2025-10-01T10:00:00"
    }
  ]
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer eyJhbGci..."
```

#### POST /api/admin/users
**Purpose:** Create new user as admin  
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
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"pass123","is_admin":false}'
```

#### DELETE /api/admin/users/{user_id}
**Purpose:** Delete a user (admin only, cannot delete self)  
**Auth Required:** Yes (admin token)  
**Request:** Path parameter `user_id`  
**Response:**
```json
{
  "success": true,
  "message": "User 'username' deleted successfully"
}
```
**Example:**
```bash
curl -X DELETE http://localhost:8000/api/admin/users/5 \
  -H "Authorization: Bearer eyJhbGci..."
```

#### PUT /api/admin/users/{user_id}/reset-password
**Purpose:** Reset user's password as admin  
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
curl -X PUT http://localhost:8000/api/admin/users/5/reset-password \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"new_password":"newpass123"}'
```

---

### POC Agent Endpoints (`/api/poc`)

#### POST /api/poc/upload
**Purpose:** Upload document (PDF, TXT, MD, PNG, JPG) for POC context  
**Auth Required:** Yes (Bearer token)  
**Request:** multipart/form-data with `file` field  
**Accepted Types:** .pdf, .txt, .md, .png, .jpg, .jpeg  
**Response:**
```json
{
  "id": 1,
  "filename": "requirements.pdf",
  "file_type": "pdf",
  "created_at": "2025-10-09T12:00:00"
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/poc/upload \
  -H "Authorization: Bearer eyJhbGci..." \
  -F "file=@requirements.pdf"
```

#### GET /api/poc/documents
**Purpose:** List all documents uploaded by current user  
**Auth Required:** Yes (Bearer token)  
**Request:** None  
**Response:**
```json
[
  {
    "id": 1,
    "filename": "requirements.pdf",
    "file_type": "pdf",
    "created_at": "2025-10-09T12:00:00"
  }
]
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/documents \
  -H "Authorization: Bearer eyJhbGci..."
```

#### DELETE /api/poc/documents/{doc_id}
**Purpose:** Delete a document  
**Auth Required:** Yes (Bearer token)  
**Request:** Path parameter `doc_id`  
**Response:**
```json
{
  "message": "Document deleted"
}
```
**Example:**
```bash
curl -X DELETE http://localhost:8000/api/poc/documents/1 \
  -H "Authorization: Bearer eyJhbGci..."
```

#### POST /api/poc/chat
**Purpose:** Chat with POC Agent (conversational requirements gathering)  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "prompt": "I want to build a task management app",
  "document_ids": [1, 2],
  "conversation_history": {
    "conversation_id": "conv_123_20251009_120000"
  }
}
```
**Response:**
```json
{
  "response": "Great! Let me ask you some questions...",
  "conversation_id": "conv_123_20251009_120000",
  "agent_state": {
    "stage": "initial_requirements",
    "requirements": {
      "goal": "Task management app"
    }
  },
  "next_action": "continue_chat"
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/poc/chat \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"prompt":"I want to build a customer feedback tool"}'
```

#### POST /api/poc/generate
**Purpose:** Generate complete POC structure with documentation  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "requirements": {
    "goal": "Build a task tracker",
    "users": "Teams",
    "frontend": {"pages": ["dashboard", "tasks"]},
    "backend": {"endpoints": ["POST /tasks", "GET /tasks"]},
    "database": {"tables": ["tasks"]}
  }
}
```
**Response:**
```json
{
  "poc_id": "task_tracker",
  "poc_name": "Build a task tracker",
  "directory": "pocs/user_1/task_tracker",
  "files": [
    "poc_desc.md",
    "requirements.md",
    "phase_1_frontend.md",
    "phase_2_backend.md",
    "phase_3_database.md"
  ]
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/poc/generate \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"requirements":{"goal":"Task tracker"}}'
```

#### GET /api/poc/list
**Purpose:** List all POCs created by current user  
**Auth Required:** Yes (Bearer token)  
**Request:** None  
**Response:**
```json
[
  {
    "id": 1,
    "poc_id": "task_tracker",
    "poc_name": "Task Tracker",
    "description": "Simple task management",
    "created_at": "2025-10-09T12:00:00"
  }
]
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/list \
  -H "Authorization: Bearer eyJhbGci..."
```

#### GET /api/poc/{poc_id}/files
**Purpose:** Get file tree for a POC  
**Auth Required:** Yes (Bearer token)  
**Request:** Path parameter `poc_id`  
**Response:**
```json
{
  "poc_id": "task_tracker",
  "directory": "pocs/user_1/task_tracker",
  "files": [
    "poc_desc.md",
    "requirements.md",
    "phase_1_frontend.md"
  ]
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/task_tracker/files \
  -H "Authorization: Bearer eyJhbGci..."
```

#### GET /api/poc/{poc_id}/download
**Purpose:** Download POC as ZIP file  
**Auth Required:** Yes (Bearer token)  
**Request:** Path parameter `poc_id`  
**Response:** Binary ZIP file  
**Example:**
```bash
curl -X GET http://localhost:8000/api/poc/task_tracker/download \
  -H "Authorization: Bearer eyJhbGci..." \
  -o poc.zip
```

#### PUT /api/poc/{poc_id}/update
**Purpose:** Update POC requirements and regenerate files  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "requirements": {
    "goal": "Updated goal"
  }
}
```
**Response:**
```json
{
  "message": "POC updated",
  "directory": "pocs/user_1/task_tracker"
}
```
**Example:**
```bash
curl -X PUT http://localhost:8000/api/poc/task_tracker/update \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"requirements":{"goal":"Updated task tracker"}}'
```

---

### Tenant POC Endpoints (`/api/tenant_1/poc_idea_1`)

#### GET /api/tenant_1/poc_idea_1/tasks
**Purpose:** Get all tasks for current user (tenant-specific)  
**Auth Required:** Yes (Bearer token)  
**Request:** None  
**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Task title",
      "description": "Task description",
      "status": "pending",
      "created_at": "2025-10-09T12:00:00",
      "updated_at": "2025-10-09T12:00:00"
    }
  ]
}
```
**Example:**
```bash
curl -X GET http://localhost:8000/api/tenant_1/poc_idea_1/tasks \
  -H "Authorization: Bearer eyJhbGci..."
```

#### POST /api/tenant_1/poc_idea_1/tasks
**Purpose:** Create new task for current user  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "title": "New task",
  "description": "Task details",
  "status": "pending"
}
```
**Response:**
```json
{
  "task": {
    "id": 1,
    "user_id": 1,
    "title": "New task",
    "description": "Task details",
    "status": "pending",
    "created_at": "2025-10-09T12:00:00",
    "updated_at": "2025-10-09T12:00:00"
  }
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/tenant_1/poc_idea_1/tasks \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"title":"New task","description":"Details","status":"pending"}'
```

#### PUT /api/tenant_1/poc_idea_1/tasks/{task_id}
**Purpose:** Update existing task  
**Auth Required:** Yes (Bearer token)  
**Request Body:**
```json
{
  "title": "Updated title",
  "status": "completed"
}
```
**Response:**
```json
{
  "task": {
    "id": 1,
    "title": "Updated title",
    "status": "completed"
  }
}
```
**Example:**
```bash
curl -X PUT http://localhost:8000/api/tenant_1/poc_idea_1/tasks/1 \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'
```

#### DELETE /api/tenant_1/poc_idea_1/tasks/{task_id}
**Purpose:** Delete a task  
**Auth Required:** Yes (Bearer token)  
**Request:** Path parameter `task_id`  
**Response:**
```json
{
  "message": "Task deleted successfully"
}
```
**Example:**
```bash
curl -X DELETE http://localhost:8000/api/tenant_1/poc_idea_1/tasks/1 \
  -H "Authorization: Bearer eyJhbGci..."
```

---

### Root Endpoint

#### GET /
**Purpose:** Health check and API information  
**Auth Required:** No  
**Request:** None  
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
**Table:** `users`  
**Purpose:** Stores user authentication and profile data  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment, Indexed
- `username`: String(50), Unique, Not Null, Indexed
- `email`: String(100), Nullable
- `password_hash`: String(255), Not Null (bcrypt hashed)
- `is_admin`: Boolean, Default=False, Not Null
- `created_at`: DateTime, Default=UTC now, Not Null
- `updated_at`: DateTime, Default=UTC now, On Update=UTC now, Not Null

**Relationships:** None  
**Indexes:** 
- Primary key on `id`
- Unique index on `username`

**Usage Example:**
```python
from database import User, get_db

# Create user
new_user = User(
    username="testuser",
    email="test@example.com",
    password_hash=hashed_password,
    is_admin=False
)
db.add(new_user)
db.commit()
```

---

### Document Model
**Table:** `documents`  
**Purpose:** Stores uploaded documents (PDFs, TXT, MD, images) for POC context  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment, Indexed
- `user_id`: Integer, Not Null, Indexed (foreign key to users.id)
- `filename`: String(255), Not Null
- `file_path`: String(500), Not Null
- `content_text`: Text, Nullable (extracted text, limited to 10k chars)
- `file_type`: String(10), Not Null (pdf, txt, md, png, jpg)
- `created_at`: DateTime, Default=UTC now, Not Null

**Relationships:** Foreign key to User via `user_id`  
**Indexes:**
- Primary key on `id`
- Index on `user_id`

**Usage Example:**
```python
from database import Document, get_db

doc = Document(
    user_id=1,
    filename="requirements.pdf",
    file_path="uploads/1/requirements.pdf",
    content_text="Extracted text...",
    file_type="pdf"
)
db.add(doc)
db.commit()
```

---

### POC Model
**Table:** `pocs`  
**Purpose:** Stores generated proof-of-concept projects  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment, Indexed
- `user_id`: Integer, Not Null, Indexed (foreign key to users.id)
- `poc_id`: String(100), Not Null, Indexed (friendly name like "task_tracker")
- `poc_name`: String(255), Not Null (display name)
- `description`: Text, Nullable
- `requirements`: JSON, Nullable (structured requirements)
- `directory`: String(500), Not Null (path to POC directory)
- `created_at`: DateTime, Default=UTC now, Not Null

**Relationships:** Foreign key to User via `user_id`  
**Indexes:**
- Primary key on `id`
- Index on `user_id`
- Index on `poc_id`
- Composite index on `(user_id, poc_id)`

**Usage Example:**
```python
from database import POC, get_db

poc = POC(
    user_id=1,
    poc_id="task_tracker",
    poc_name="Task Tracker",
    description="Simple task management",
    requirements={"goal": "Track tasks"},
    directory="pocs/user_1/task_tracker"
)
db.add(poc)
db.commit()
```

---

### POCConversation Model
**Table:** `poc_conversations`  
**Purpose:** Stores conversation history with POC Agent  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment, Indexed
- `poc_id`: Integer, Nullable, Indexed (foreign key to pocs.id, null before POC generated)
- `user_id`: Integer, Not Null, Indexed (foreign key to users.id)
- `conversation_history`: JSON, Nullable (message history)
- `langchain_memory`: JSON, Nullable (LangChain memory state)
- `created_at`: DateTime, Default=UTC now, Not Null

**Relationships:** 
- Foreign key to User via `user_id`
- Foreign key to POC via `poc_id`

**Indexes:**
- Primary key on `id`
- Index on `poc_id`
- Index on `user_id`

**Usage Example:**
```python
from database import POCConversation, get_db

conversation = POCConversation(
    user_id=1,
    poc_id=None,  # Before POC generation
    conversation_history={"messages": [...]},
    langchain_memory={"buffer": [...]}
)
db.add(conversation)
db.commit()
```

---

### POCPhase Model
**Table:** `poc_phases`  
**Purpose:** Tracks implementation phases of a POC  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment, Indexed
- `poc_id`: Integer, Not Null, Indexed (foreign key to pocs.id)
- `phase_number`: Integer, Not Null (1, 2, or 3)
- `phase_name`: String(50), Not Null (frontend, backend, database)
- `instructions_file`: String(500), Not Null (path to phase instructions)
- `status`: String(20), Default="pending", Not Null (pending, in_progress, completed)
- `created_at`: DateTime, Default=UTC now, Not Null

**Relationships:** Foreign key to POC via `poc_id`  
**Indexes:**
- Primary key on `id`
- Index on `poc_id`

**Usage Example:**
```python
from database import POCPhase, get_db

phase = POCPhase(
    poc_id=1,
    phase_number=1,
    phase_name="Frontend",
    instructions_file="pocs/user_1/task_tracker/phase_1_frontend.md",
    status="pending"
)
db.add(phase)
db.commit()
```

---

### TaskModel (Tenant-Specific)
**Table:** `tenant_1_poc1_tasks`  
**Purpose:** Stores tasks for tenant_1's poc_idea_1  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment, Indexed
- `user_id`: Integer, Not Null, Indexed (foreign key to users.id)
- `title`: String(200), Not Null
- `description`: Text, Nullable
- `status`: String(20), Default="pending", Not Null
- `created_at`: DateTime, Default=UTC now, Not Null
- `updated_at`: DateTime, Default=UTC now, On Update=UTC now, Not Null

**Relationships:** Foreign key to User via `user_id`  
**Indexes:**
- Primary key on `id`
- Index on `user_id`

**Usage Example:**
```python
from tenant.tenant_1.poc_idea_1.backend.models import TaskModel
from database import get_db

task = TaskModel(
    user_id=1,
    title="Complete documentation",
    description="Write comprehensive docs",
    status="pending"
)
db.add(task)
db.commit()
```

---

## 4. FRONTEND COMPONENTS CATALOG

### POCBuilder Component
**File:** `frontend/src/components/POCBuilder.tsx`  
**Purpose:** Main POC building interface with document upload, chat, and POC management  
**Props:** None (standalone page component)  
**Features:**
- 40/60 split layout (left: documents/POCs, right: chat)
- Document upload with drag-and-drop (PDF, TXT, MD, PNG, JPG)
- Conversational chat interface with POC Agent
- Document list with delete functionality
- POC list and selection
- Generate POC button when conversation ready
- Real-time typing indicators
- Message history with timestamps
- Tab switching between documents and POCs

**State Management:**
- `activeTab`: 'documents' | 'pocs'
- `documents`: Document[]
- `pocs`: POC[]
- `messages`: Message[] (role: 'user' | 'agent', content, timestamp)
- `conversationId`: string | null
- `isTyping`: boolean

**Usage:**
```tsx
import POCBuilder from './components/POCBuilder';

function App() {
  return <POCBuilder />;
}
```

---

### AdminPanel Component
**File:** `frontend/src/components/AdminPanel.tsx`  
**Purpose:** Admin interface for user management  
**Props:** None (standalone page component)  
**Features:**
- 40/60 split layout (left: actions, right: user list)
- Add new users with admin privilege option
- Reset user passwords
- Delete users (except self)
- User list table with role badges
- Real-time user list refresh
- Form validation
- Success/error message display

**State Management:**
- `users`: User[]
- `newUsername`, `newPassword`, `newEmail`, `newIsAdmin`: form state
- `resetUserId`, `resetPassword`: reset password state
- `error`, `success`: message state
- `loading`, `addLoading`, `resetLoading`: loading states

**Usage:**
```tsx
import AdminPanel from './components/AdminPanel';

// Only accessible by admin users
function App() {
  return isAdmin ? <AdminPanel /> : <Navigate to="/" />;
}
```

---

### Login Component
**File:** `frontend/src/components/Login.tsx`  
**Purpose:** User login form  
**Props:** None (standalone page component)  
**Features:**
- Username and password input
- Form validation
- Error message display
- Link to registration page
- Automatic navigation after login
- Loading state during authentication

**State Management:**
- `username`, `password`: form state
- `error`: error message
- `loading`: loading state

**Usage:**
```tsx
import Login from './components/Login';

function App() {
  return <Login />;
}
```

---

### Register Component
**File:** `frontend/src/components/Register.tsx`  
**Purpose:** User registration form  
**Props:** None (standalone page component)  
**Features:**
- Username, email, password, confirm password inputs
- Password matching validation
- Minimum length validation (4 characters)
- Error message display
- Link to login page
- Automatic navigation after registration
- Optional email field

**State Management:**
- `username`, `password`, `confirmPassword`, `email`: form state
- `error`: error message
- `loading`: loading state

**Usage:**
```tsx
import Register from './components/Register';

function App() {
  return <Register />;
}
```

---

### UserSettings Component
**File:** `frontend/src/components/UserSettings.tsx`  
**Purpose:** User profile and password management  
**Props:** None (standalone page component)  
**Features:**
- Side-by-side layout (profile update left, password change right)
- Update username and email
- Change password with current password verification
- Form validation
- Success/error messages per section
- Pre-populated fields with current user data

**State Management:**
- Profile: `username`, `email`, `profileError`, `profileSuccess`, `profileLoading`
- Password: `currentPassword`, `newPassword`, `confirmPassword`, `passwordError`, `passwordSuccess`, `passwordLoading`

**Usage:**
```tsx
import UserSettings from './components/UserSettings';

function App() {
  return <UserSettings />;
}
```

---

## 5. AUTHENTICATION & MIDDLEWARE

### Authentication Mechanism
- **Type:** JWT (JSON Web Tokens)
- **Algorithm:** HS256
- **Expiration:** 24 hours (configurable via `JWT_EXPIRATION_HOURS`)
- **Secret Key:** Stored in environment variable `JWT_SECRET_KEY`

### Password Security
- **Hashing:** bcrypt with automatic salt generation
- **Minimum Length:** 4 characters
- **Validation:** Password strength check before registration/change

### How to Protect Endpoints

**Backend (FastAPI):**
```python
from auth import get_current_user
from database import User

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    """
    This endpoint requires authentication.
    current_user is automatically populated from JWT token.
    """
    return {"message": f"Hello {current_user.username}"}
```

**Admin-Only Endpoint:**
```python
from admin import get_admin_user
from database import User

@router.get("/admin-only")
async def admin_route(admin_user: User = Depends(get_admin_user)):
    """
    This endpoint requires admin privileges.
    Returns 403 if user is not admin.
    """
    return {"message": "Admin access granted"}
```

**Frontend (React):**
```tsx
import { getAuthHeader } from './utils/auth';

// Make authenticated request
const response = await axios.get(`${API_URL}/api/protected`, {
  headers: getAuthHeader()  // Adds "Authorization: Bearer <token>"
});
```

### Token Management

**Create Token:**
```python
from auth_utils import create_access_token

token = create_access_token(
    data={
        "sub": str(user_id),
        "username": username,
        "is_admin": is_admin
    }
)
```

**Decode Token:**
```python
from auth_utils import decode_access_token

payload = decode_access_token(token)
if payload:
    user_id = payload.get("sub")
    username = payload.get("username")
```

**Frontend Token Storage:**
```tsx
import { setToken, getToken, clearToken } from './utils/auth';

// Store token after login
setToken(jwt_token);

// Retrieve token
const token = getToken();

// Clear token on logout
clearToken();
```

### CORS Configuration
**Allowed Origins:**
- `http://localhost:3000` (local dev)
- `http://localhost:5173` (Vite dev server)
- Azure Static Web App URL
- Azure App Service URL

**Settings:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[...],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

---

## 6. FILE UPLOAD PATTERNS

### Upload Endpoint
**Route:** `POST /api/poc/upload`  
**Auth:** Required (Bearer token)

### Supported File Types
- **Documents:** PDF, TXT, MD
- **Images:** PNG, JPG, JPEG

### Size Limits
- No explicit limit set (relies on FastAPI defaults)
- Recommended: Add size validation for production

### Storage Location
- **Path Pattern:** `uploads/{user_id}/{timestamp}_{filename}`
- **Example:** `uploads/1/20251009_120000_requirements.pdf`

### How to Add File Upload to New Endpoints

**Backend:**
```python
from fastapi import UploadFile, File
import os
import shutil

@router.post("/upload-custom")
async def upload_custom_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Validate file type
    allowed_types = ["pdf", "txt"]
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Create directory
    upload_dir = f"custom_uploads/{current_user.id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "path": file_path}
```

**Frontend:**
```tsx
const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(
    'http://localhost:8000/api/poc/upload',
    formData,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    }
  );
};
```

### Document Processing
- **PDF:** Loaded with `PyPDFLoader`, split into chunks
- **TXT/MD:** Loaded with `TextLoader`, split into chunks
- **Images (PNG/JPG):** Analyzed with GPT-4 Vision, converted to text description
- **Vector Store:** Documents embedded with OpenAI embeddings, stored in FAISS

### Access Pattern
- Documents are user-scoped (isolated by `user_id`)
- Retrieved via `/api/poc/documents` endpoint
- Deleted via `/api/poc/documents/{doc_id}` endpoint

---

## 7. DATABASE PATTERNS

### How to Create New Tables

**Step 1: Define Model in database.py or tenant module**
```python
from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class NewModel(Base):
    """Model description."""
    __tablename__ = "new_table"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

**Step 2: Import in database.py init_db()**
```python
def init_db():
    from tenant.tenant_1.poc_idea_1.backend.models import TaskModel
    from your_module import NewModel  # Add this
    
    Base.metadata.create_all(bind=engine)
```

**Step 3: Run database initialization**
```bash
source venv/bin/activate
python3 database.py
```

### Session Management Pattern
**Dependency Injection:**
```python
from database import get_db
from sqlalchemy.orm import Session

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items
```

### Query Examples

**Create (INSERT):**
```python
new_item = Item(name="Test", value=100)
db.add(new_item)
db.commit()
db.refresh(new_item)  # Get auto-generated fields
```

**Read (SELECT):**
```python
# Get all
items = db.query(Item).all()

# Get by ID
item = db.query(Item).filter(Item.id == 1).first()

# Get with conditions
items = db.query(Item).filter(Item.value > 50).all()

# Get with ordering
items = db.query(Item).order_by(Item.created_at.desc()).all()
```

**Update (UPDATE):**
```python
item = db.query(Item).filter(Item.id == 1).first()
if item:
    item.name = "Updated"
    db.commit()
    db.refresh(item)
```

**Delete (DELETE):**
```python
item = db.query(Item).filter(Item.id == 1).first()
if item:
    db.delete(item)
    db.commit()
```

### Transaction Handling
```python
try:
    # Multiple operations
    item1 = Item(name="Item1")
    db.add(item1)
    
    item2 = Item(name="Item2")
    db.add(item2)
    
    db.commit()
except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

### Database Initialization
- **Automatic:** Database initialized on application startup via `@app.on_event("startup")`
- **Manual:** Run `python3 database.py` to create all tables
- **Location:** `boot_lang.db` in project root

---

## 8. DIRECTORY STRUCTURE CONVENTIONS

### Project Layout
```
/boot_lang                          # Project root
  /venv                             # Python virtual environment
  /frontend                         # React frontend application
    /src
      /components                   # Reusable React components
      /contexts                     # React contexts (AuthContext)
      /utils                        # Utility functions (auth.ts)
      App.tsx                       # Main app component
      index.tsx                     # Entry point
    /build                          # Production build output
    package.json                    # Node dependencies
  /backend (root)                   # FastAPI backend (root level)
    app.py                          # Main application file
    database.py                     # Database models and initialization
    auth.py                         # Authentication endpoints
    auth_utils.py                   # Auth utilities (JWT, bcrypt)
    admin.py                        # Admin endpoints
    user_management.py              # User profile endpoints
    poc_api.py                      # POC agent endpoints
    /agents                         # LangChain agents
      poc_agent.py                  # POC Agent implementation
      poc_agent_prompts.json        # Agent prompt configuration
  /tenant                           # Tenant-specific POCs
    /tenant_1                       # Tenant ID
      /poc_idea_1                   # POC ID
        /frontend                   # POC-specific frontend
          /src
            /components
        /backend                    # POC-specific backend
          models.py                 # POC database models
          routes.py                 # POC API routes
  /pocs                             # Generated POC documentation
    /{user_id}                      # User-specific POCs
      /{poc_id}                     # POC friendly name
        poc_desc.md                 # POC description
        requirements.md             # Captured requirements
        phase_1_frontend.md         # Frontend instructions
        phase_2_backend.md          # Backend instructions
        phase_3_database.md         # Database instructions
        /wireframes                 # Uploaded wireframe images
        /generated                  # Generated code artifacts
  /uploads                          # User-uploaded documents
    /{user_id}                      # User-specific uploads
  /vector_stores                    # FAISS vector stores
    /{user_id}                      # User-specific vector stores
      /faiss_index                  # FAISS index files
  /docs                             # Project documentation
  /imp_plans                        # Implementation plans
  requirements.txt                  # Python dependencies
  boot_lang.db                      # SQLite database file
  .env                              # Environment variables
```

### Tenant POC Naming Convention
- **Pattern:** `/tenant/tenant_{id}/poc_{idea_id}`
- **Example:** `/tenant/tenant_1/poc_idea_1`
- **Frontend:** `/tenant/tenant_{id}/poc_{idea_id}/frontend`
- **Backend:** `/tenant/tenant_{id}/poc_{idea_id}/backend`

### Generated POC Naming Convention
- **Pattern:** `/pocs/{user_id}/{friendly_poc_name}`
- **Example:** `/pocs/test_user_123/customer_feedback_tracker`
- **Friendly Name:** Generated by LLM, lowercase with underscores

---

## 9. DEPLOYMENT CONFIGURATION

### Azure Deployment
**Frontend:** Azure Static Web Apps  
**Backend:** Azure App Service  
**Database:** SQLite (local file, not cloud-hosted)

### Environment Variables Required
```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# OpenAI API
OPENAI_API_KEY=sk-...

# Perplexity API (optional)
PERPLEXITY_API_KEY=pplx-...

# LangSmith (optional, for LLM tracing)
LANGSMITH_API_KEY=ls__...
LANGSMITH_PROJECT=boot_lang

# Application Ports
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Development Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Build Commands
**Frontend:**
```bash
cd frontend
npm install
npm run build
```

**Backend:**
```bash
source venv/bin/activate
pip install -r requirements.txt
python3 database.py  # Initialize database
```

### Start Commands
**Development Backend:**
```bash
source venv/bin/activate
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Development Frontend:**
```bash
cd frontend
npm start
```

**Production Backend:**
```bash
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### CORS Configuration
Pre-configured for:
- Local development (`localhost:3000`, `localhost:5173`)
- Azure Static Web App
- Azure App Service

### Branch/Deployment Strategy
- **Main Branch:** Production-ready code
- **Tenant Branches:** Pattern `tenant/tenant_{id}` for tenant-specific work
- **Current Branch:** `tenant/tenant_1` (tenant-specific features)

---

## 10. LANGCHAIN INTEGRATION PATTERNS

### Available LangChain Components

**LLMs:**
- `ChatOpenAI(model="gpt-3.5-turbo")` - Default for cost efficiency
- `ChatOpenAI(model="gpt-4o")` - For vision capabilities

**Embeddings:**
- `OpenAIEmbeddings()` - For document vectorization

**Vector Stores:**
- `FAISS` - Local vector store for RAG

**Document Loaders:**
- `PyPDFLoader` - PDF documents
- `TextLoader` - TXT/MD files

**Text Splitters:**
- `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`

**Memory:**
- `ConversationBufferMemory(return_messages=True)` - Conversation history

**Chains:**
- `ConversationChain` - Conversational flow
- `LLMChain` - Custom prompt chains

**Output Parsers:**
- `PydanticOutputParser` - Structured output extraction

### Conversational Agent Structure

**POC Agent (`agents/poc_agent.py`):**
```python
class POCAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        # Load prompts from JSON
        self.prompts = self._load_prompts()
        
        # Initialize memory
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings()
        
        # Vector stores (per user)
        self.vector_stores: Dict[str, FAISS] = {}
    
    def process_request(self, prompt: str, user_id: str):
        # Retrieve context from documents
        context = self.retrieve_context(prompt, user_id)
        
        # Process through conversation chain
        response = self.conversation_chain.predict(input=prompt)
        
        return response
```

### Memory Management Pattern
```python
# Save conversation state
saved_state = agent.save_conversation()
# Store in database: POCConversation.langchain_memory

# Restore conversation state
agent.load_conversation(saved_state)
# Continue conversation with memory intact
```

### Prompt Template Pattern
```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["user_input", "context"],
    template="""You are a Technical Product Manager AI.

Context from documents:
{context}

User request: {user_input}

Respond helpfully and professionally."""
)

chain = prompt | llm
result = chain.invoke({"user_input": "...", "context": "..."})
```

### RAG (Retrieval Augmented Generation) Usage

**Upload and Process Document:**
```python
# Load document
docs = agent.load_document("requirements.pdf", "pdf")

# Create/update vector store
vector_store = agent.create_vector_store(docs, user_id="user_123")
```

**Retrieve Context:**
```python
# Semantic search
context = agent.retrieve_context(
    query="What are the UI requirements?",
    user_id="user_123",
    k=3  # Top 3 relevant chunks
)
```

**RAG-Enhanced Conversation:**
```python
# Context automatically retrieved and injected
result = agent.process_request(
    prompt="What did the uploaded doc say about features?",
    user_id="user_123"
)
# Response includes information from uploaded documents
```

### Structured Output with Pydantic

```python
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class RequirementsSchema(BaseModel):
    goal: Optional[str] = Field(None, description="Main goal")
    users: Optional[str] = Field(None, description="Target users")
    frontend: Optional[Dict[str, Any]] = Field(None, description="Frontend requirements")

parser = PydanticOutputParser(pydantic_object=RequirementsSchema)

prompt = PromptTemplate(
    input_variables=["conversation"],
    template="""Extract requirements from this conversation:
{conversation}

{format_instructions}""",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | llm | parser
requirements = chain.invoke({"conversation": "..."})
```

### Image Analysis with GPT-4 Vision

```python
def analyze_wireframe(image_path: str):
    """Analyze wireframe using GPT-4 Vision."""
    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Create vision LLM
    vision_llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    
    # Create prompt with image
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a UI/UX analyst."),
        ("human", [
            {"type": "text", "text": "Analyze this wireframe..."},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_data}"}
            }
        ])
    ])
    
    chain = prompt | vision_llm
    result = chain.invoke({})
    return result.content
```

---

## 11. AVAILABLE TOOLS & UTILITIES

### Authentication Utilities (`auth_utils.py`)

**hash_password(password: str) -> str**
```python
from auth_utils import hash_password

hashed = hash_password("mypassword123")
# Returns bcrypt hash: "$2b$12$..."
```

**verify_password(plain_password: str, hashed_password: str) -> bool**
```python
from auth_utils import verify_password

is_valid = verify_password("mypassword123", stored_hash)
if is_valid:
    print("Password correct!")
```

**create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str**
```python
from auth_utils import create_access_token

token = create_access_token(
    data={"sub": "user123", "username": "john", "is_admin": False}
)
# Returns JWT: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**decode_access_token(token: str) -> Optional[Dict[str, Any]]**
```python
from auth_utils import decode_access_token

payload = decode_access_token(token)
if payload:
    user_id = payload.get("sub")
    username = payload.get("username")
```

**validate_password_strength(password: str) -> tuple[bool, Optional[str]]**
```python
from auth_utils import validate_password_strength

is_valid, error = validate_password_strength("pass")
if not is_valid:
    print(f"Password error: {error}")
```

### Frontend Authentication Utilities (`frontend/src/utils/auth.ts`)

**setToken(token: string): void**
```tsx
import { setToken } from './utils/auth';
setToken(jwt_token);
```

**getToken(): string | null**
```tsx
import { getToken } from './utils/auth';
const token = getToken();
```

**clearToken(): void**
```tsx
import { clearToken } from './utils/auth';
clearToken();  // On logout
```

**getAuthHeader(): object**
```tsx
import { getAuthHeader } from './utils/auth';
const response = await axios.get(url, { headers: getAuthHeader() });
```

### Database Session Management

**get_db() - FastAPI Dependency**
```python
from database import get_db
from sqlalchemy.orm import Session

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

**init_db() - Initialize Database**
```python
from database import init_db

# Run once to create all tables
init_db()
```

---

## 12. STYLING CONVENTIONS

### CSS Framework
**Tailwind CSS** - Utility-first CSS framework

### Color Scheme

**Primary Colors:**
- Blue: `bg-blue-600`, `text-blue-600`, `border-blue-600`
- Blue Hover: `hover:bg-blue-700`
- Blue Light: `bg-blue-50`, `text-blue-100`

**Neutral Colors:**
- Background: `bg-gray-50`, `bg-gray-100`
- Text: `text-gray-900`, `text-gray-700`, `text-gray-500`
- Borders: `border-gray-300`

**Feedback Colors:**
- Success: `bg-green-50`, `text-green-700`, `border-green-200`
- Error: `bg-red-50`, `text-red-700`, `border-red-200`
- Warning: `bg-yellow-50`, `text-yellow-700`
- Info: `bg-blue-50`, `text-blue-700`

### Common Utility Classes

**Layout:**
- Flex: `flex`, `flex-1`, `flex-col`
- Grid: `grid`, `grid-cols-1`, `md:grid-cols-2`
- Spacing: `space-y-4`, `space-x-2`, `gap-6`
- Padding: `p-4`, `px-6`, `py-3`
- Margins: `m-4`, `mx-auto`, `mt-8`, `mb-4`

**Typography:**
- Headings: `text-3xl font-bold`, `text-xl font-semibold`
- Body: `text-sm`, `text-base`
- Weight: `font-medium`, `font-semibold`, `font-bold`
- Colors: `text-gray-900`, `text-gray-600`, `text-blue-600`

**Components:**
- Buttons: `px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700`
- Inputs: `px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500`
- Cards: `bg-white p-6 rounded-lg shadow-md`

### Layout Patterns

**40/60 Split (POCBuilder, AdminPanel):**
```tsx
<div className="flex h-screen">
  {/* Left 40% */}
  <div className="w-2/5 bg-white border-r">
    {/* Content */}
  </div>
  
  {/* Right 60% */}
  <div className="w-3/5 flex flex-col">
    {/* Content */}
  </div>
</div>
```

**Centered Auth Forms:**
```tsx
<div className="min-h-screen flex items-center justify-center bg-gray-50">
  <div className="max-w-md w-full p-8 bg-white rounded-lg shadow-md">
    {/* Form content */}
  </div>
</div>
```

**Message Bubbles (Chat):**
```tsx
<div className={`max-w-[80%] rounded-lg p-3 ${
  isUser ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'
}`}>
  {/* Message content */}
</div>
```

### Responsive Breakpoints
- `sm:` - 640px
- `md:` - 768px
- `lg:` - 1024px
- `xl:` - 1280px

**Example:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* Responsive grid */}
</div>
```

---

## 13. ERROR HANDLING PATTERNS

### Backend Error Response Format

**Standard Error Response:**
```json
{
  "detail": "Error message description"
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Internal Server Error

**Raising Errors:**
```python
from fastapi import HTTPException, status

# Bad request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already exists"
)

# Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials"
)

# Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Admin privileges required"
)

# Not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)
```

### Frontend Error Display Pattern

**Success/Error Messages:**
```tsx
{error && (
  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
)}

{success && (
  <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
    {success}
  </div>
)}
```

**Error Handling in Axios:**
```tsx
try {
  const response = await axios.post(url, data, { headers });
  // Handle success
} catch (err: any) {
  const errorMessage = err.response?.data?.detail || 'Operation failed';
  setError(errorMessage);
}
```

### Logging Configuration
- **Development:** Console logging via `print()` statements
- **Level:** INFO
- **Production:** Consider structured logging (not yet implemented)

### Common Error Scenarios

**Authentication Errors:**
- Invalid token → 401 Unauthorized
- Expired token → 401 Unauthorized
- Missing token → 401 Unauthorized
- Not admin → 403 Forbidden

**Validation Errors:**
- Username too short → 400 Bad Request
- Password too weak → 400 Bad Request
- Invalid email format → 400 Bad Request
- Duplicate username → 400 Bad Request

**Not Found Errors:**
- User not found → 404 Not Found
- Document not found → 404 Not Found
- POC not found → 404 Not Found

---

## 14. TESTING PATTERNS

### Testing Framework
**Status:** Not yet implemented  
**Recommended:** pytest for backend, Jest/React Testing Library for frontend

### How to Run Tests (When Implemented)
```bash
# Backend tests
source venv/bin/activate
python3 -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### Test File Locations (Future)
- Backend: `/tests/test_*.py`
- Frontend: `/frontend/src/**/*.test.tsx`

### Coverage Expectations
- **Goal:** 80%+ coverage
- **Priority:** Critical paths (auth, POC generation, database operations)

### Manual Testing
Currently using manual testing via:
- Curl commands (see endpoint examples)
- Browser testing (frontend)
- POC Agent test script (`python3 agents/poc_agent.py`)

---

## 15. TENANT ARCHITECTURE

### Tenant Isolation Pattern
- **Tenant Directory:** `/tenant/tenant_{id}`
- **POC Directory:** `/tenant/tenant_{id}/poc_{idea_id}`
- **Models:** Separate table per tenant POC (e.g., `tenant_1_poc1_tasks`)
- **Routes:** Mounted with tenant prefix (e.g., `/api/tenant_1/poc_idea_1`)

### Adding New Tenant POC

**Step 1: Create Directory Structure**
```bash
mkdir -p tenant/tenant_2/poc_idea_1/backend
mkdir -p tenant/tenant_2/poc_idea_1/frontend/src/components
```

**Step 2: Define Models**
```python
# tenant/tenant_2/poc_idea_1/backend/models.py
from sqlalchemy import Column, Integer, String
from database import Base

class CustomModel(Base):
    __tablename__ = "tenant_2_poc1_custom"
    id = Column(Integer, primary_key=True)
    # ... fields
```

**Step 3: Create Routes**
```python
# tenant/tenant_2/poc_idea_1/backend/routes.py
from fastapi import APIRouter, Depends
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.get("/items")
async def get_items(db = Depends(get_db), user = Depends(get_current_user)):
    # Implementation
    pass
```

**Step 4: Register in app.py**
```python
from tenant.tenant_2.poc_idea_1.backend.routes import router as t2_poc1_router

app.include_router(
    t2_poc1_router,
    prefix="/api/tenant_2/poc_idea_1",
    tags=["tenant_2"]
)
```

**Step 5: Update database.py init_db()**
```python
def init_db():
    from tenant.tenant_1.poc_idea_1.backend.models import TaskModel
    from tenant.tenant_2.poc_idea_1.backend.models import CustomModel
    
    Base.metadata.create_all(bind=engine)
```

---

## 16. SUMMARY & QUICK REFERENCE

### Quick Start Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Start backend (development)
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Start frontend (development)
cd frontend && npm start

# Initialize database
python3 database.py

# Test POC Agent
python3 agents/poc_agent.py
```

### Key Files
- `app.py` - Main FastAPI application
- `database.py` - Database models and initialization
- `auth.py` - Authentication endpoints
- `poc_api.py` - POC Agent API
- `agents/poc_agent.py` - POC Agent implementation
- `frontend/src/App.tsx` - React application
- `requirements.txt` - Python dependencies
- `.env` - Environment variables

### Key Endpoints
- Auth: `/api/auth/register`, `/api/auth/login`, `/api/auth/me`
- Admin: `/api/admin/users` (GET, POST, DELETE, PUT)
- User: `/api/user/password`, `/api/user/profile`
- POC: `/api/poc/upload`, `/api/poc/chat`, `/api/poc/generate`
- Tenant: `/api/tenant_1/poc_idea_1/tasks`

### Environment Variables
```bash
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your-secret-key
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

---

**Document Version:** 1.0  
**Last Updated:** October 9, 2025  
**Maintainer:** Boot_Lang Platform Team

This document should be updated whenever:
- New endpoints are added
- Database models change
- New components are created
- Dependencies are updated
- Architecture changes occur

