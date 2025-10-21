# Stack Reference Document

**Version:** 1.0  
**Last Updated:** 2025-10-09  
**Purpose:** Comprehensive stack documentation for Cursor Instructions Generator agent

---

## 1. STACK OVERVIEW

### Core Technologies
- **Backend:** FastAPI 0.100.0+ (Python 3.11)
- **Frontend:** React 18, TypeScript
- **Database:** SQLite with SQLAlchemy 2.0+
- **AI/LLM:** LangChain 0.1.0+, OpenAI (GPT-4), Perplexity
- **Authentication:** JWT (python-jose), bcrypt
- **Styling:** Tailwind CSS
- **Vector Store:** FAISS (faiss-cpu)
- **Deployment:** Azure App Service + Azure Static Web Apps

### Key Dependencies
```
fastapi, uvicorn, gunicorn
langchain, langchain-openai, langchain-community, langserve
sqlalchemy, bcrypt, python-jose, passlib
faiss-cpu, pypdf, tiktoken
python-dotenv, pydantic, python-multipart
```

### Ports
- Backend: 8000
- Frontend: 3000

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
  "email": "string (optional)"
}
```
**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "token": "jwt_token_string",
  "user": {"id": 1, "username": "john", "email": "john@example.com", "is_admin": false}
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass1234","email":"test@example.com"}'
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
  "user": {"id": 1, "username": "john", "is_admin": false}
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass1234"}'
```

#### GET /api/auth/me
**Purpose:** Get current user information  
**Auth Required:** Yes (Bearer token)  
**Response:**
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2025-10-09T12:00:00"
}
```

### Admin Endpoints (`/api/admin`)

#### GET /api/admin/users
**Purpose:** List all users (admin only)  
**Auth Required:** Yes (admin token)  
**Response:**
```json
{
  "success": true,
  "message": "Found 5 users",
  "users": [
    {"id": 1, "username": "admin", "email": "admin@example.com", "is_admin": true, "created_at": "...", "updated_at": "..."}
  ]
}
```

#### POST /api/admin/users
**Purpose:** Create new user as admin  
**Auth Required:** Yes (admin token)  
**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "email": "string (optional)",
  "is_admin": false
}
```

#### DELETE /api/admin/users/{user_id}
**Purpose:** Delete user (cannot delete self)  
**Auth Required:** Yes (admin token)

#### PUT /api/admin/users/{user_id}/reset-password
**Purpose:** Reset user password as admin  
**Auth Required:** Yes (admin token)  
**Request Body:**
```json
{
  "new_password": "string (min 4 chars)"
}
```

### User Management Endpoints (`/api/user`)

#### PUT /api/user/password
**Purpose:** Change own password  
**Auth Required:** Yes  
**Request Body:**
```json
{
  "current_password": "string",
  "new_password": "string (min 4 chars)"
}
```

#### PUT /api/user/profile
**Purpose:** Update own profile (username/email)  
**Auth Required:** Yes  
**Request Body:**
```json
{
  "username": "string (optional)",
  "email": "string (optional)"
}
```

### POC Agent Endpoints (`/api/poc`)

#### POST /api/poc/upload
**Purpose:** Upload document for RAG (PDF, TXT, MD, PNG, JPG)  
**Auth Required:** Yes  
**Request:** multipart/form-data with file  
**Response:**
```json
{
  "id": 1,
  "filename": "requirements.pdf",
  "file_type": "pdf",
  "created_at": "2025-10-09T12:00:00"
}
```

#### GET /api/poc/documents
**Purpose:** List user's uploaded documents  
**Auth Required:** Yes

#### DELETE /api/poc/documents/{doc_id}
**Purpose:** Delete document  
**Auth Required:** Yes

#### POST /api/poc/chat
**Purpose:** Chat with POC Agent  
**Auth Required:** Yes  
**Request Body:**
```json
{
  "prompt": "I need a task manager app",
  "document_ids": [1, 2],
  "conversation_history": {"conversation_id": "abc123"}
}
```
**Response:**
```json
{
  "response": "I can help you build that...",
  "conversation_id": "abc123",
  "agent_state": {},
  "next_action": "continue"
}
```

#### POST /api/poc/generate
**Purpose:** Generate POC structure with documentation files  
**Auth Required:** Yes  
**Request Body:**
```json
{
  "requirements": {
    "goal": "Task management system",
    "features": ["create tasks", "mark complete"]
  }
}
```
**Response:**
```json
{
  "poc_id": "task_manager",
  "poc_name": "Task Manager",
  "directory": "pocs/user_1/task_manager",
  "files": ["phase_1_frontend.md", "phase_2_backend.md", "phase_3_database.md"]
}
```

#### GET /api/poc/list
**Purpose:** List user's POCs  
**Auth Required:** Yes

#### GET /api/poc/{poc_id}/files
**Purpose:** Get POC file tree  
**Auth Required:** Yes

#### GET /api/poc/{poc_id}/download
**Purpose:** Download POC as ZIP  
**Auth Required:** Yes

### Tenant Endpoints (Example)

#### GET /api/tenant_1/poc_idea_1/tasks
**Purpose:** Get tasks for current user  
**Auth Required:** Yes  
**Pattern:** `/api/tenant_{id}/poc_idea_{n}/{resource}`

---

## 3. DATABASE MODELS CATALOG

### User Model
**Table:** `users`  
**Purpose:** User authentication and authorization  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `username`: String(50), Unique, Not Null, Indexed
- `email`: String(100), Nullable
- `password_hash`: String(255), Not Null (bcrypt hashed)
- `is_admin`: Boolean, Default=False, Not Null
- `created_at`: DateTime, Default=now(), Not Null
- `updated_at`: DateTime, Default=now(), onupdate=now(), Not Null

**Relationships:** None  
**Indexes:** `username` (unique), `id` (primary)

### Document Model
**Table:** `documents`  
**Purpose:** Store uploaded files for RAG  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: Integer, Not Null, Indexed (foreign key to users.id)
- `filename`: String(255), Not Null
- `file_path`: String(500), Not Null
- `content_text`: Text, Nullable (extracted text content, max 10k chars)
- `file_type`: String(10), Not Null (pdf, txt, md, png, jpg)
- `created_at`: DateTime, Default=now(), Not Null

**Relationships:** user_id → users.id  
**Indexes:** `user_id`, `id` (primary)

### POC Model
**Table:** `pocs`  
**Purpose:** Track generated POCs  
**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: Integer, Not Null, Indexed
- `poc_id`: String(100), Not Null, Indexed (friendly name like "task_manager")
- `poc_name`: String(255), Not Null (display name)
- `description`: Text, Nullable
- `requirements`: JSON, Nullable (captured requirements dict)
- `directory`: String(500), Not Null (path to POC files)
- `created_at`: DateTime, Default=now(), Not Null

**Relationships:** user_id → users.id  
**Indexes:** Composite index on (user_id, poc_id)

### POCConversation Model
**Table:** `poc_conversations`  
**Purpose:** Store chat history with POC Agent  
**Fields:**
- `id`: Integer, Primary Key
- `poc_id`: Integer, Nullable, Indexed
- `user_id`: Integer, Not Null, Indexed
- `conversation_history`: JSON, Nullable
- `langchain_memory`: JSON, Nullable
- `created_at`: DateTime, Default=now()

### POCPhase Model
**Table:** `poc_phases`  
**Purpose:** Track POC implementation phases  
**Fields:**
- `id`: Integer, Primary Key
- `poc_id`: Integer, Not Null, Indexed
- `phase_number`: Integer, Not Null (1, 2, 3)
- `phase_name`: String(50), Not Null (Frontend, Backend, Database)
- `instructions_file`: String(500), Not Null
- `status`: String(20), Default="pending" (pending, in_progress, completed)
- `created_at`: DateTime, Default=now()

### Tenant Models (Pattern)
**Table Naming:** `tenant_{id}_poc{n}_{table_name}`  
**Example:** `tenant_1_poc1_tasks`

**TaskModel (Example):**
```python
class TaskModel(Base):
    __tablename__ = "tenant_1_poc1_tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## 4. FRONTEND COMPONENTS CATALOG

### AdminPanel Component
**File:** `frontend/src/components/AdminPanel.tsx`  
**Purpose:** Admin interface for user management  
**Props:** None (standalone page)  
**Features:**
- Create new users with admin flag
- List all users in table view
- Delete users (cannot delete self)
- Reset user passwords
- 40/60 layout (actions left, user list right)
- Form validation and error handling

**Usage:**
```tsx
import AdminPanel from './components/AdminPanel';
<Route path="/admin" element={<AdminPanel />} />
```

### Login Component
**File:** `frontend/src/components/Login.tsx`  
**Purpose:** User authentication  
**Props:** None  
**Features:**
- Username/password form
- Link to registration
- Error display
- Loading states

### Register Component
**File:** `frontend/src/components/Register.tsx`  
**Purpose:** New user registration  
**Props:** None  
**Features:**
- Username/password/email form
- Password validation (min 4 chars)
- Success/error messages

### POCBuilder Component
**File:** `frontend/src/components/POCBuilder.tsx`  
**Purpose:** Interactive POC Agent chat and document management  
**Props:** None  
**Features:**
- 40/60 layout (documents/POCs left, chat right)
- Document upload (PDF, TXT, MD, PNG, JPG)
- Document list with delete
- Chat interface with message history
- POC generation trigger
- POC list view

### UserSettings Component
**File:** `frontend/src/components/UserSettings.tsx`  
**Purpose:** User profile and password management  
**Props:** None  
**Features:**
- Change username/email
- Change password
- Form validation

---

## 5. AUTHENTICATION & MIDDLEWARE

### Authentication Mechanism
- **Type:** JWT (JSON Web Tokens)
- **Library:** python-jose with cryptography
- **Token Expiration:** 24 hours (configurable via JWT_EXPIRATION_HOURS)
- **Storage:** localStorage (frontend)
- **Header Format:** `Authorization: Bearer <token>`

### How to Protect Endpoints

**Backend (FastAPI):**
```python
from auth import get_current_user
from database import User

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id}
```

**Admin-only endpoints:**
```python
from admin import get_admin_user

@router.get("/admin-only")
async def admin_route(admin_user: User = Depends(get_admin_user)):
    return {"admin": admin_user.username}
```

**Frontend (React):**
```typescript
import { getAuthHeader } from '../utils/auth';

const response = await axios.get(`${API_URL}/api/protected`, {
  headers: getAuthHeader()
});
```

### Token Management

**Backend Functions (auth_utils.py):**
```python
create_access_token(data: dict) -> str
decode_access_token(token: str) -> Optional[dict]
hash_password(password: str) -> str
verify_password(plain: str, hashed: str) -> bool
validate_password_strength(password: str) -> tuple[bool, Optional[str]]
```

**Frontend Functions (utils/auth.ts):**
```typescript
setToken(token: string): void
getToken(): string | null
removeToken(): void
setUser(user: any): void
getUser(): any | null
clearAuth(): void
getAuthHeader(): {Authorization: string} | {}
isAuthenticated(): boolean
isAdmin(): boolean
```

### User Roles
- **User:** Default role, access to own data
- **Admin:** `is_admin=true`, access to admin panel and all users

### Password Requirements
- Minimum 4 characters
- Bcrypt hashing with salt

---

## 6. FILE UPLOAD PATTERNS

### Upload Endpoint
**Route:** `POST /api/poc/upload`  
**Content-Type:** `multipart/form-data`  
**Supported Types:** pdf, txt, md, png, jpg, jpeg  
**Size Limit:** Not explicitly set (recommend 10MB)  
**Storage:** `uploads/{user_id}/{timestamp}_{filename}`

### How to Add File Upload

**Backend:**
```python
from fastapi import UploadFile, File

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "txt", "md"]:
        raise HTTPException(400, "Unsupported file type")
    
    # Create upload directory
    upload_dir = f"uploads/{current_user.id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "path": file_path}
```

**Frontend:**
```typescript
const handleUpload = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  await axios.post(`${API_URL}/api/upload`, formData, {
    headers: {
      ...getAuthHeader(),
      'Content-Type': 'multipart/form-data'
    }
  });
};
```

---

## 7. DATABASE PATTERNS

### Creating New Tables

**Step 1: Define Model (models.py or database.py)**
```python
from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class MyModel(Base):
    __tablename__ = "my_table"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Step 2: Import in database.py init_db()**
```python
from mymodule.models import MyModel
```

**Step 3: Run Migration**
```bash
python3 -c "from database import init_db; init_db()"
```

### Session Management Pattern

**Dependency Injection:**
```python
from database import get_db

@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(MyModel).all()
    return items
```

### CRUD Examples

**Create:**
```python
new_item = MyModel(user_id=1, name="Test")
db.add(new_item)
db.commit()
db.refresh(new_item)
```

**Read:**
```python
# All
items = db.query(MyModel).all()

# Filter
items = db.query(MyModel).filter(MyModel.user_id == 1).all()

# First/One
item = db.query(MyModel).filter(MyModel.id == 1).first()
```

**Update:**
```python
item = db.query(MyModel).filter(MyModel.id == 1).first()
item.name = "Updated"
db.commit()
db.refresh(item)
```

**Delete:**
```python
item = db.query(MyModel).filter(MyModel.id == 1).first()
db.delete(item)
db.commit()
```

### Transaction Handling
```python
try:
    db.add(item1)
    db.add(item2)
    db.commit()
except Exception as e:
    db.rollback()
    raise
```

---

## 8. DIRECTORY STRUCTURE CONVENTIONS

```
/root
  /frontend                    # Main React app
    /src
      /components              # Reusable UI components
      /contexts                # React contexts (AuthContext)
      /utils                   # Helper functions (auth.ts)
      App.tsx                  # Main app with routing
      config.ts                # API_URL configuration
    package.json
    
  /backend (root level)
    app.py                     # Main FastAPI app
    database.py                # Database models and init
    auth.py                    # Auth endpoints
    auth_utils.py              # Auth helper functions
    admin.py                   # Admin endpoints
    user_management.py         # User profile endpoints
    poc_api.py                 # POC Agent endpoints
    
  /agents                      # LangChain agents
    poc_agent.py               # POC Agent implementation
    poc_agent_prompts.json     # Agent prompts
    
  /tenant                      # Tenant POC isolation
    /tenant_1
      /poc_idea_1
        /frontend              # POC-specific React app
          /src
            /components
            App.tsx
        /backend
          routes.py            # POC endpoints
          models.py            # POC database models
        poc_idea1_PRD.md       # Requirements doc
        
  /pocs                        # Generated POC documentation
    /{username}_poc
      /{poc_name}
        phase_1_frontend.md
        phase_2_backend.md
        phase_3_database.md
        requirements.md
        
  /uploads                     # User uploaded files
    /{user_id}
      {timestamp}_{filename}
      
  /vector_stores              # FAISS vector stores for RAG
    /{user_id}_rag
      /faiss_index
      
  requirements.txt            # Python dependencies
  .env                        # Environment variables
  boot_lang.db               # SQLite database
```

### Tenant POC Naming Conventions
- **Directory:** `/tenant/tenant_{id}/poc_idea_{n}`
- **Table:** `tenant_{id}_poc{n}_{table_name}`
- **Route Prefix:** `/api/tenant_{id}/poc_idea_{n}`
- **Frontend Route:** `/tenant_{id}/poc_idea_{n}/`

---

## 9. DEPLOYMENT CONFIGURATION

### Environment Variables Required
```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# LLM APIs
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=pplx-...

# LangSmith (Optional)
LANGSMITH_API_KEY=ls__...
LANGSMITH_PROJECT=boot_lang

# Development
DEBUG=True
LOG_LEVEL=INFO

# Ports
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### Build Commands

**Backend:**
```bash
pip install -r requirements.txt
python3 -c "from database import init_db; init_db()"
```

**Frontend:**
```bash
cd frontend
npm install
npm run build
```

### Start Commands

**Development:**
```bash
# Backend
python3 app.py
# or
uvicorn app:app --reload --port 8000

# Frontend
cd frontend
npm start
```

**Production:**
```bash
# Backend
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend (served as static)
# Build output in frontend/build/
```

### CORS Configuration
**Allowed Origins (app.py):**
- `http://localhost:3000` (dev)
- `http://localhost:5173` (vite dev)
- `https://proud-smoke-02a8bab0f.1.azurestaticapps.net` (Azure Static Web App)
- `https://boot-lang-gscvbveeg3dvgefh.eastus2-01.azurewebsites.net` (Azure App Service)

### Branch/Deployment Strategy
```
main → boot-lang.azurewebsites.net (base system only)
├── tenant/tenant_1 → boot-lang-tenant1.azurewebsites.net
├── tenant/tenant_2 → boot-lang-tenant2.azurewebsites.net
└── tenant/tenant_3 → boot-lang-tenant3.azurewebsites.net
```

---

## 10. TENANT ARCHITECTURE (CRITICAL)

### Directory Structure Pattern
```
/tenant/tenant_{id}/poc_idea_{n}/
  /frontend/
  /backend/
    routes.py
    models.py
  poc_idea{n}_PRD.md
```

### Table Naming Convention
**Pattern:** `tenant_{id}_poc{n}_{table_name}`  
**Examples:**
- `tenant_1_poc1_tasks`
- `tenant_2_poc1_customers`
- `tenant_1_poc2_orders`

### Route Prefix Pattern
**Pattern:** `/api/tenant_{id}/poc_idea_{n}`  
**Examples:**
- `/api/tenant_1/poc_idea_1/tasks`
- `/api/tenant_2/poc_idea_1/customers`

### Router Registration in app.py
```python
# Import tenant router
from tenant.tenant_1.poc_idea_1.backend.routes import router as t1_poc1_router

# Register with prefix
app.include_router(t1_poc1_router, prefix="/api/tenant_1/poc_idea_1", tags=["tenant_1"])
```

### Model Registration in database.py
```python
def init_db():
    # Import tenant models to register with Base
    from tenant.tenant_1.poc_idea_1.backend.models import TaskModel
    
    Base.metadata.create_all(bind=engine)
```

### Adding New Tenant POC (Step-by-Step)

1. **Create directory structure:**
```bash
mkdir -p tenant/tenant_1/poc_idea_2/backend
mkdir -p tenant/tenant_1/poc_idea_2/frontend/src
```

2. **Create backend/models.py:**
```python
from sqlalchemy import Column, Integer, String
from database import Base

class ItemModel(Base):
    __tablename__ = "tenant_1_poc2_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100))
```

3. **Create backend/routes.py:**
```python
from fastapi import APIRouter, Depends
router = APIRouter()

@router.get("/items")
async def get_items(current_user=Depends(get_current_user)):
    # Implementation
    pass
```

4. **Update app.py:**
```python
from tenant.tenant_1.poc_idea_2.backend.routes import router as t1_poc2_router
app.include_router(t1_poc2_router, prefix="/api/tenant_1/poc_idea_2", tags=["tenant_1"])
```

5. **Update database.py init_db():**
```python
from tenant.tenant_1.poc_idea_2.backend.models import ItemModel
```

6. **Run migration:**
```bash
python3 -c "from database import init_db; init_db()"
```

### Isolation Principles
- **Database:** Shared SQLite with tenant-prefixed tables
- **Authentication:** Reuses base auth system
- **Data Isolation:** user_id in all tenant tables
- **Deployment:** Each tenant on separate branch/instance

---

## 11. STANDARD POC SKELETON (CRITICAL)

Every generated POC must include:

### Required Backend Files

**backend/models.py:**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class ResourceModel(Base):
    __tablename__ = "tenant_X_pocN_resources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # Resource-specific fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**backend/routes.py:**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.get("/{resource}")
async def get_resources(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    from .models import ResourceModel
    items = db.query(ResourceModel).filter(ResourceModel.user_id == current_user.id).all()
    return {"items": items}

@router.post("/{resource}")
async def create_resource(data: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    from .models import ResourceModel
    new_item = ResourceModel(user_id=current_user.id, **data)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"item": new_item}

@router.put("/{resource}/{id}")
async def update_resource(id: int, data: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    from .models import ResourceModel
    item = db.query(ResourceModel).filter(ResourceModel.id == id, ResourceModel.user_id == current_user.id).first()
    if not item:
        raise HTTPException(404, "Not found")
    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    return {"item": item}

@router.delete("/{resource}/{id}")
async def delete_resource(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    from .models import ResourceModel
    item = db.query(ResourceModel).filter(ResourceModel.id == id, ResourceModel.user_id == current_user.id).first()
    if not item:
        raise HTTPException(404, "Not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted"}
```

### Required Frontend Files

**frontend/src/config.ts:**
```typescript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const POC_PREFIX = '/api/tenant_1/poc_idea_1';
```

**frontend/src/utils/api.ts:**
```typescript
import axios from 'axios';
import { API_BASE_URL, POC_PREFIX } from '../config';

const api = axios.create({
  baseURL: `${API_BASE_URL}${POC_PREFIX}`
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('boot_lang_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const getItems = () => api.get('/items');
export const createItem = (data: any) => api.post('/items', data);
export const updateItem = (id: number, data: any) => api.put(`/items/${id}`, data);
export const deleteItem = (id: number) => api.delete(`/items/${id}`);
```

**frontend/src/components/Dashboard.tsx:**
- Landing page with overview
- Navigation to other components
- Summary statistics

**frontend/src/components/ItemList.tsx:**
- Table or card view of items
- Filter/search functionality
- Click to edit

**frontend/src/components/ItemForm.tsx:**
- Create/edit form
- Validation
- Success/error messages

**frontend/src/components/AdminPanel.tsx:**
- CRUD for all POC tables
- Data management interface

### Standard Endpoint Pattern
Every POC backend includes:
- `GET /{resource}` - List all for current user
- `POST /{resource}` - Create new
- `PUT /{resource}/{id}` - Update existing
- `DELETE /{resource}/{id}` - Delete

### Standard Frontend Pattern
- **Layout:** 40/60 split (actions left, data right)
- **Responsive:** Tailwind responsive classes (md:, lg:)
- **Auth:** Reuses base AuthContext
- **Styling:** Consistent color scheme (blue primary, gray neutral)

---

## 12. GIT WORKFLOW & DEPLOYMENT (CRITICAL)

### Branch Structure
```
main (base system - auth, admin, POC agents)
├── tenant/tenant_1 (all tenant_1 POCs)
├── tenant/tenant_2 (all tenant_2 POCs)
└── tenant/tenant_3 (all tenant_3 POCs)
```

### Azure Deployment Instances
- `main` → `boot-lang.azurewebsites.net` (base system only)
- `tenant/tenant_1` → `boot-lang-tenant1.azurewebsites.net` (tenant 1 + all POCs)
- `tenant/tenant_2` → `boot-lang-tenant2.azurewebsites.net` (tenant 2 + all POCs)
- `tenant/tenant_3` → `boot-lang-tenant3.azurewebsites.net` (tenant 3 + all POCs)

### Workflow for New POC

**Step 1: Switch to tenant branch**
```bash
git checkout tenant/tenant_1
# If first POC: git checkout -b tenant/tenant_1 main
```

**Step 2: Merge base updates**
```bash
git merge main
```

**Step 3: Implement POC**
- Create directory structure
- Add backend models and routes
- Add frontend components
- Update app.py and database.py

**Step 4: Test locally**
```bash
python3 app.py
curl http://localhost:8000/api/tenant_1/poc_idea_1/tasks -H "Authorization: Bearer TOKEN"
```

**Step 5: Commit and push**
```bash
git add tenant/tenant_1/
git add app.py database.py
git commit -m "Add POC: Task Manager"
git push origin tenant/tenant_1
```

**Step 6: Deployment auto-triggers**
- Push triggers Azure deployment for tenant_1 instance only
- Other tenants unaffected

### Updating Base System

**Step 1: Update main**
```bash
git checkout main
# Make changes to auth, admin, core
git commit -m "Update auth system"
git push origin main
```

**Step 2: Merge to tenants**
```bash
git checkout tenant/tenant_1
git merge main
git push origin tenant/tenant_1
```

### Isolation Benefits
- Tenant 1's code cannot break Tenant 2 or 3
- Each tenant deploys independently
- Base system remains stable on main
- Rollback per tenant without affecting others

---

## 13. PERFORMANCE & SECURITY BEST PRACTICES

### Performance

**Indexes:**
- Add on user_id (required for all tenant tables)
- Add on foreign keys
- Add on frequently queried fields
```python
user_id = Column(Integer, index=True)
status = Column(String(20), index=True)
```

**Query Optimization:**
```python
# Good: Select specific columns
db.query(User.id, User.username).all()

# Good: Use joins instead of N+1 queries
db.query(Task).join(User).filter(User.username == "john").all()

# Bad: Select all when only need one field
db.query(User).all()  # Then iterate for user.id
```

**Pagination:**
```python
page = 1
per_page = 50
offset = (page - 1) * per_page
items = db.query(Item).offset(offset).limit(per_page).all()
```

**File Size Limits:**
- Recommended: 10MB max for uploads
- Implement in endpoint validation

### Security

**Input Sanitization:**
- Use Pydantic models for all request bodies
- Validate all user input
```python
class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    priority: int = Field(..., ge=1, le=5)
```

**SQL Injection Prevention:**
- ALWAYS use SQLAlchemy ORM
- NEVER use raw SQL with user input
```python
# Good
db.query(User).filter(User.username == user_input).first()

# Bad
db.execute(f"SELECT * FROM users WHERE username='{user_input}'")
```

**XSS Prevention:**
- React escapes by default
- NEVER use dangerouslySetInnerHTML with user content

**CSRF Protection:**
- JWT tokens (not cookies), no CSRF needed
- Tokens in Authorization header, not URL params

**Password Requirements:**
- Minimum 4 characters (current)
- Bcrypt hashing with salt
- Never store plain passwords

**File Upload Validation:**
```python
# Whitelist extensions
allowed = ["pdf", "txt", "md", "png", "jpg"]
if file_ext not in allowed:
    raise HTTPException(400, "Invalid file type")

# Check file size
if file.size > 10 * 1024 * 1024:  # 10MB
    raise HTTPException(400, "File too large")
```

**Environment Variables:**
- NEVER hardcode secrets
- Use .env file (not committed)
- Load with python-dotenv

### Code Organization

**File Size:**
- Components < 300 lines (split if larger)
- Functions < 50 lines

**When to Split:**
- Reusable logic → separate file
- Complex state → custom hook
- Component > 200 lines → break into smaller components

**Comment Requirements:**
- 30% coverage for public functions
- Docstrings: Purpose, Args, Returns, Exceptions, Example

---

## 14. AVAILABLE TOOLS & UTILITIES

### Backend Utilities (auth_utils.py)

```python
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    # Returns bcrypt hashed string

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash"""
    # Returns True if match

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token with 24hr expiration"""
    # Usage: create_access_token({"sub": "user_id", "username": "john"})

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate JWT token"""
    # Returns payload dict or None if invalid

def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """Validate password meets requirements (min 4 chars)"""
    # Returns (True, None) or (False, "error message")
```

### Frontend Utilities (utils/auth.ts)

```typescript
function setToken(token: string): void
    // Store JWT in localStorage

function getToken(): string | null
    // Retrieve JWT from localStorage

function removeToken(): void
    // Clear JWT from localStorage

function setUser(user: any): void
    // Store user object in localStorage

function getUser(): any | null
    // Retrieve user from localStorage

function clearAuth(): void
    // Clear all auth data (logout)

function getAuthHeader(): {Authorization: string} | {}
    // Get Bearer token header for API calls

function isAuthenticated(): boolean
    // Check if user has valid token

function isAdmin(): boolean
    // Check if current user is admin
```

### Database Utilities (database.py)

```python
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI endpoints.
    Yields database session, ensures cleanup.
    
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """

def init_db() -> None:
    """
    Initialize database by creating all tables.
    Safe to call multiple times (idempotent).
    
    Usage:
        python3 -c "from database import init_db; init_db()"
    """
```

---

## 15. STYLING CONVENTIONS

### CSS Framework
Tailwind CSS (utility-first)

### Color Scheme
- **Primary:** Blue (`bg-blue-600`, `text-blue-600`, `border-blue-500`)
- **Neutral:** Gray (`bg-gray-50`, `text-gray-700`, `border-gray-300`)
- **Success:** Green (`bg-green-600`, `text-green-700`, `bg-green-50`)
- **Error:** Red (`bg-red-600`, `text-red-700`, `bg-red-50`)
- **Warning:** Yellow (`bg-yellow-600`, `text-yellow-700`, `bg-yellow-50`)
- **Admin:** Purple (`bg-purple-100`, `text-purple-800`)

### Common Utility Classes

**Layout:**
```css
flex, grid
items-center, justify-center
space-x-4, space-y-4, gap-6
w-full, h-full, min-h-screen
max-w-7xl, mx-auto
```

**Spacing:**
```css
p-4, p-6, p-8 (padding)
px-4, py-2 (padding x/y)
m-4, mt-2, mb-4 (margin)
```

**Typography:**
```css
text-sm, text-base, text-lg, text-xl, text-3xl
font-medium, font-semibold, font-bold
text-gray-700, text-blue-600
```

**Forms:**
```css
border border-gray-300 rounded-md
focus:outline-none focus:ring-blue-500 focus:border-blue-500
disabled:opacity-50 disabled:cursor-not-allowed
```

**Buttons:**
```css
bg-blue-600 hover:bg-blue-700 text-white
px-4 py-2 rounded-lg
focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
```

### Layout Patterns

**40/60 Split:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-5 gap-6">
  <div className="md:col-span-2">Left 40%</div>
  <div className="md:col-span-3">Right 60%</div>
</div>
```

**Centered Form:**
```tsx
<div className="min-h-screen flex items-center justify-center bg-gray-50">
  <div className="max-w-md w-full p-8 bg-white rounded-lg shadow-md">
    {/* Form content */}
  </div>
</div>
```

**Message Boxes:**
```tsx
{/* Success */}
<div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
  Success message
</div>

{/* Error */}
<div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
  Error message
</div>
```

### Responsive Breakpoints
- `sm:` - 640px+
- `md:` - 768px+
- `lg:` - 1024px+
- `xl:` - 1280px+

**Example:**
```tsx
<div className="w-full md:w-1/2 lg:w-1/3">
  {/* Full width on mobile, half on tablet, third on desktop */}
</div>
```

---

## 16. ERROR HANDLING PATTERNS

### Backend Error Format

```python
from fastapi import HTTPException

# Standard error
raise HTTPException(
    status_code=404,
    detail="Resource not found"
)

# With custom status codes
raise HTTPException(status_code=400, detail="Invalid input")  # Bad Request
raise HTTPException(status_code=401, detail="Unauthorized")   # Auth required
raise HTTPException(status_code=403, detail="Forbidden")      # No permission
raise HTTPException(status_code=404, detail="Not found")      # Resource missing
raise HTTPException(status_code=500, detail="Server error")   # Internal error
```

### Frontend Error Display

```tsx
// Error state
const [error, setError] = useState('');

// Error display
{error && (
  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
)}

// Catch and display
try {
  await axios.post(url, data);
} catch (err: any) {
  setError(err.response?.data?.detail || 'Operation failed');
}
```

### Common Error Scenarios

**401 Unauthorized:**
- Missing or invalid JWT token
- Expired token
- Redirect to login

**403 Forbidden:**
- User lacks required permissions
- Non-admin accessing admin endpoint

**404 Not Found:**
- Resource doesn't exist
- User trying to access another user's data

**500 Internal Server Error:**
- Database errors
- Unhandled exceptions
- Log and show generic message to user

### Logging Configuration

**Development:**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("User logged in")
logger.error(f"Failed to process: {e}")
```

**Console logging for debugging:**
```python
print(f"Debug: {variable}")  # Development only
```

---

## 17. TESTING PATTERNS

### Testing Framework
- **Backend:** pytest (not yet implemented)
- **Frontend:** Jest + React Testing Library (not yet implemented)

### Manual Testing Approach

**Backend Testing (curl):**
```bash
# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass"}' \
  | jq .

# Test protected endpoint
TOKEN="your_jwt_token_here"
curl http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer $TOKEN"

# Test create
curl -X POST http://localhost:8000/api/tenant_1/poc_idea_1/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task"}' \
  | jq .
```

**Frontend Testing (Browser):**
- Open Developer Console (F12)
- Check Network tab for API calls
- Verify localStorage for tokens
- Test responsive design (Device toolbar)

### Where Tests Should Go
```
/tests/
  test_auth.py
  test_admin.py
  test_poc_api.py
  
/frontend/src/
  components/
    Login.test.tsx
    AdminPanel.test.tsx
```

### Coverage Expectations
- **Critical paths:** 80%+ (auth, payments, data loss)
- **Standard features:** 60%+
- **UI components:** 40%+

### Test Patterns (Future)

```python
# pytest example
def test_user_registration(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "pass1234"
    })
    assert response.status_code == 201
    assert response.json()["success"] == True
```

```typescript
// Jest example
test('renders login form', () => {
  render(<Login />);
  expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
});
```

---

## DOCUMENT METADATA

**Endpoints Documented:** 25+  
**Models Documented:** 6 core + 1 tenant example  
**Components Documented:** 5 main components  
**Complete Sections:** 17/17

### Key Sections for POC Generation
- Section 2: Backend Endpoints Catalog
- Section 3: Database Models Catalog
- Section 4: Frontend Components Catalog
- Section 10: Tenant Architecture
- Section 11: Standard POC Skeleton
- Section 12: Git Workflow & Deployment
- Section 13: Performance & Security

### Missing/Future Enhancements
- LangChain agent implementation details (in agents/poc_agent.py)
- Perplexity API integration patterns
- Vector store management details
- Test suite implementation
- CI/CD pipeline configuration
- Monitoring and logging infrastructure

---

**End of Stack Reference Document**




