# Tenant Implementation Specification

**Version:** 1.0  
**Purpose:** Exact implementation pattern for 3-tenant POC system  
**Status:** LOCKED - Ready for Cursor Implementation

---

## 1. DIRECTORY STRUCTURE (EXACT)

```
/root
  /tenant/
    /tenant_1/
      /poc_idea_1/
        /frontend/
          /src/
            /components/
            App.tsx
          package.json
        /backend/
          routes.py
          models.py
        poc_idea1_PRD.md
        poc_idea1_Cursorplan_20251009_143022.md
        idea_metadata_20251009_140000.json
    /tenant_2/
      /poc_idea_1/
        (same structure)
    /tenant_3/
      /poc_idea_1/
        (same structure)
```

---

## 2. ROUTER REGISTRATION (EXACT CODE)

### app.py additions:
```python
# Add at top with other imports
from tenant.tenant_1.poc_idea_1.backend.routes import router as t1_poc1_router

# Add after base routers
app.include_router(t1_poc1_router, prefix="/api/tenant_1/poc_idea_1", tags=["tenant_1"])
```

### Tenant router template (routes.py):
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.get("/items")
async def get_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from .models import ItemModel
    items = db.query(ItemModel).filter(
        ItemModel.user_id == current_user.id
    ).all()
    return {"items": items}

@router.post("/items")
async def create_item(
    item_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from .models import ItemModel
    new_item = ItemModel(user_id=current_user.id, **item_data)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"item": new_item}
```

---

## 3. DATABASE PATTERN (EXACT)

### Table naming: `tenant_{tenant_id}_poc{n}_{table_name}`
Example: `tenant_1_poc1_tasks`

### Model template (models.py):
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class TaskModel(Base):
    __tablename__ = "tenant_1_poc1_tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

### Register in database.py:
```python
# Add import
from tenant.tenant_1.poc_idea_1.backend.models import TaskModel

# Models auto-register via Base
```

### Run migration:
```bash
python -c "from database import init_db; init_db()"
```

---

## 4. FRONTEND INTEGRATION (EXACT)

### Main app routing (frontend/src/App.tsx):
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Tenant1Poc1 from '../../tenant/tenant_1/poc_idea_1/frontend/src/App';

<Route path="/tenant_1/poc_idea_1/*" element={<Tenant1Poc1 />} />
```

### Tenant frontend config (tenant/.../frontend/src/config.ts):
```typescript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const POC_PREFIX = '/api/tenant_1/poc_idea_1';
```

### API utility (tenant/.../frontend/src/utils/api.ts):
```typescript
import axios from 'axios';
import { API_BASE_URL, POC_PREFIX } from '../config';

const api = axios.create({
  baseURL: `${API_BASE_URL}${POC_PREFIX}`
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getItems = () => api.get('/items');
export const createItem = (data: any) => api.post('/items', data);
```

---

## 5. DEPLOYMENT WORKFLOW (EXACT STEPS)

### Branch Structure (ISOLATION):
```
main (base system only - auth, admin, POC agent)
├── tenant/tenant_1 (all tenant_1 POCs)
├── tenant/tenant_2 (all tenant_2 POCs)
└── tenant/tenant_3 (all tenant_3 POCs)
```

### Azure Deployment Instances:
- `main` → `boot-lang.azurewebsites.net` (base system)
- `tenant/tenant_1` → `boot-lang-tenant1.azurewebsites.net`
- `tenant/tenant_2` → `boot-lang-tenant2.azurewebsites.net`
- `tenant/tenant_3` → `boot-lang-tenant3.azurewebsites.net`

### Adding new tenant POC:

**Step 1: Work in tenant branch**
```bash
# Switch to tenant branch (or create if first POC)
git checkout tenant/tenant_1
# If doesn't exist: git checkout -b tenant/tenant_1 main

# Pull latest base system updates
git merge main
```

**Step 2: Create POC structure**
```bash
mkdir -p tenant/tenant_1/poc_idea_1/backend
mkdir -p tenant/tenant_1/poc_idea_1/frontend/src
```

**Step 3: Add backend code**
- Create `routes.py` with endpoints
- Create `models.py` with database tables
- Update `app.py`: Import and register router
- Update `database.py`: Import models

**Step 4: Initialize database**
```bash
python -c "from database import init_db; init_db()"
```

**Step 5: Test backend locally**
```bash
python app.py
curl http://localhost:8000/api/tenant_1/poc_idea_1/items \
  -H "Authorization: Bearer TOKEN"
```

**Step 6: Add frontend code**
- Create React components in `frontend/src/`
- Create `api.ts`, `config.ts`
- Update main `App.tsx` with route

**Step 7: Test frontend locally**
```bash
cd tenant/tenant_1/poc_idea_1/frontend
npm install
npm start
```

**Step 8: Commit to tenant branch**
```bash
git add tenant/tenant_1/poc_idea_1/
git commit -m "Add poc_idea_1: Task Manager"

git add app.py database.py frontend/src/App.tsx
git commit -m "Register poc_idea_1 routes and frontend"

git push origin tenant/tenant_1
```

**Step 9: Deploy tenant branch**
```bash
# Push triggers Azure deployment for tenant_1 instance
# Deploys to: boot-lang-tenant1.azurewebsites.net
```

### Updating base system for all tenants:

**Step 1: Update main branch**
```bash
git checkout main
# Make changes to auth, admin, core features
git commit -m "Update base auth system"
git push origin main
```

**Step 2: Merge to tenant branches**
```bash
# Each tenant pulls updates independently
git checkout tenant/tenant_1
git merge main
git push origin tenant/tenant_1

git checkout tenant/tenant_2
git merge main
git push origin tenant/tenant_2

git checkout tenant/tenant_3
git merge main
git push origin tenant/tenant_3
```

### URL Structure (Production):

**Base System:**
- API: `https://boot-lang.azurewebsites.net/api/auth/login`
- Frontend: `https://proud-smoke-02a8bab0f.1.azurestaticapps.net/`

**Tenant 1:**
- API: `https://boot-lang-tenant1.azurewebsites.net/api/tenant_1/poc_idea_1/tasks`
- Frontend: `https://boot-lang-tenant1.azurewebsites.net/tenant_1/poc_idea_1/dashboard`

**Tenant 2:**
- API: `https://boot-lang-tenant2.azurewebsites.net/api/tenant_2/poc_idea_1/customers`
- Frontend: `https://boot-lang-tenant2.azurewebsites.net/tenant_2/poc_idea_1/dashboard`

**Tenant 3:**
- API: `https://boot-lang-tenant3.azurewebsites.net/api/tenant_3/poc_idea_1/orders`
- Frontend: `https://boot-lang-tenant3.azurewebsites.net/tenant_3/poc_idea_1/dashboard`

### Isolation Benefits:
- Tenant 1's code cannot break Tenant 2 or 3
- Each tenant deploys independently
- Base system remains stable on `main`
- Can rollback tenant deployments without affecting others
- Different testing schedules per tenant

---

## 6. STANDARD POC SKELETON (EVERY POC INCLUDES)

### Backend files:
- `routes.py` - FastAPI router with CRUD endpoints
- `models.py` - SQLAlchemy models (1+ tables)

### Frontend files:
- `App.tsx` - Main component
- `components/Dashboard.tsx` - Landing page
- `components/ItemList.tsx` - List view
- `components/ItemForm.tsx` - Create/edit form
- `components/AdminPanel.tsx` - Data management UI
- `utils/api.ts` - API functions
- `config.ts` - API configuration

### Auto-included features:
- Authentication (reuses base AuthContext)
- Admin panel (CRUD for all tables)
- Error handling components
- Loading states

---

## 7. TESTING CHECKPOINTS (EXACT COMMANDS)

### Backend:
```bash
# Verify router registered
curl http://localhost:8000/docs

# Test endpoint
curl -X GET http://localhost:8000/api/tenant_1/poc_idea_1/items \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test create
curl -X POST http://localhost:8000/api/tenant_1/poc_idea_1/items \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Item"}'
```

### Frontend:
```bash
cd tenant/tenant_1/poc_idea_1/frontend
npm install
npm start
# Opens on http://localhost:3001 (or next available port)
```

### Database:
```bash
# Verify tables created
sqlite3 boot_lang.db ".tables"
# Should see tenant_1_poc1_* tables

# Check data
sqlite3 boot_lang.db "SELECT * FROM tenant_1_poc1_tasks;"
```

---

## 8. WHAT "DONE" LOOKS LIKE

### Backend complete when:
- [ ] Router imported in app.py
- [ ] Models imported in database.py
- [ ] Tables exist in boot_lang.db
- [ ] GET /items returns 200
- [ ] POST /items creates record
- [ ] Swagger docs show tenant endpoints

### Frontend complete when:
- [ ] Route registered in main App.tsx
- [ ] npm start works without errors
- [ ] Can navigate to /tenant_X/poc_idea_Y/
- [ ] Can see list of items
- [ ] Can create new item
- [ ] Admin panel shows all tables

### Integration complete when:
- [ ] Frontend can call backend endpoints
- [ ] Authentication works (base system)
- [ ] Data persists in database
- [ ] Can restart server, data remains
- [ ] Multiple users see only their data

---

## 9. EXAMPLE TENANT POC (REFERENCE)

### Tenant 1, POC 1: Task Manager

**Routes:** `/api/tenant_1/poc_idea_1/tasks`

**Table:** `tenant_1_poc1_tasks`
- id, user_id, title, description, status, created_at

**Frontend routes:** `/tenant_1/poc_idea_1/dashboard`

**Features:**
- List tasks
- Create task
- Mark complete
- Admin view all tasks

This serves as reference implementation for all tenant POCs.

---

END OF SPEC