# Cursor Instructions: Build Stack Reference Document

**Purpose:** Generate comprehensive stack documentation for Cursor Instructions Generator agent

---

## Prompt: Create Complete Stack Reference Document

```
Create docs/stack_reference.md - a comprehensive living document that catalogs our entire stack for AI agent consumption. This document will be read by the Cursor Instructions Generator agent to understand available capabilities when designing POC implementations.

CRITICAL: This document must be factual, complete, and structured for LLM parsing. Include examples and specifics, not generalizations.

## Document Structure:

### 1. STACK OVERVIEW
List current versions and purpose:
- Backend framework and version
- Frontend framework and version  
- Database type and ORM
- AI/LLM libraries
- Deployment platform
- Key dependencies from requirements.txt

### 2. BACKEND ENDPOINTS CATALOG
For EACH existing endpoint in the codebase, document:
- Route path (e.g., /api/admin/users)
- HTTP method (GET, POST, PUT, DELETE)
- Purpose (one sentence)
- Request schema (parameters, body structure with types)
- Response schema (success and error formats)
- Authentication required (yes/no)
- Example curl command

Scan these files for endpoints:
- app.py
- admin.py
- auth.py
- user_management.py
- poc_api.py
- tenant/*/backend/routes.py

Format:
```markdown
#### POST /api/admin/users
**Purpose:** Create new user account
**Auth Required:** Yes (admin token)
**Request Body:**
\`\`\`json
{
  "username": "string",
  "password": "string"
}
\`\`\`
**Response:**
\`\`\`json
{
  "success": true,
  "user_id": "integer"
}
\`\`\`
**Example:**
\`\`\`bash
curl -X POST http://localhost:8000/api/admin/users \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'
\`\`\`
```

### 3. DATABASE MODELS CATALOG
For EACH SQLAlchemy model in database.py and tenant models, document:
- Table name
- All fields with types and constraints
- Relationships to other tables
- Indexes
- Purpose/use case

Format:
```markdown
#### User Model
**Table:** users
**Purpose:** Stores user authentication and profile data
**Fields:**
- id: Integer, Primary Key, Auto-increment
- username: String(50), Unique, Not Null
- password_hash: String(255), Not Null
- created_at: DateTime, Default=now()
**Relationships:** None
**Indexes:** username (unique)
```

### 4. FRONTEND COMPONENTS CATALOG
For EACH reusable component in frontend/src/components/, document:
- Component name and file path
- Purpose
- Props interface (name, type, required/optional, description)
- Key features/capabilities
- Usage example

Format:
```markdown
#### AdminPanel Component
**File:** src/components/AdminPanel.tsx
**Purpose:** Admin interface for user management
**Props:**
- None (standalone page component)
**Features:**
- Create new users
- List existing users
- Form validation
- Error handling
**Usage:**
\`\`\`tsx
import AdminPanel from './components/AdminPanel';
<AdminPanel />
\`\`\`
```

### 5. AUTHENTICATION & MIDDLEWARE
Document:
- Authentication mechanism (JWT, session, etc.)
- How to protect endpoints
- Token/session management
- User roles/permissions if applicable
- Code examples for adding auth to new endpoints

Reference: auth.py, auth_utils.py, frontend/src/contexts/AuthContext.tsx

### 6. FILE UPLOAD PATTERNS
Document:
- File upload endpoint(s)
- Supported file types
- Size limits
- Storage location
- How to add file upload to new endpoints
- Access/retrieval patterns

Reference: poc_api.py for multipart/form-data handling

### 7. DATABASE PATTERNS
Document:
- How to create new tables (SQLAlchemy model pattern)
- How to run migrations/initialize DB
- Session management pattern (get_db dependency)
- Query examples (CRUD operations)
- Transaction handling

### 8. DIRECTORY STRUCTURE CONVENTIONS
Document the standard project layout:
```
/root
  /frontend
    /src
      /components
      /contexts
      /utils
    package.json
  /backend (root level)
    app.py
    database.py
    auth.py
    /agents
  /tenant
    /tenant_1
      /poc_idea_1
        /frontend
        /backend
  requirements.txt
  .env
```

Explain where new tenant POC code should live and naming conventions.

### 9. DEPLOYMENT CONFIGURATION
Document:
- Azure deployment setup
- Environment variables required (JWT_SECRET_KEY, OPENAI_API_KEY, etc.)
- Build commands (frontend: npm build, backend: pip install)
- Start commands (development and production)
- CORS configuration
- Branch/deployment strategy (main vs tenant branches)

### 10. TENANT ARCHITECTURE (NEW SECTION - CRITICAL)
Document the tenant isolation pattern:
- Directory structure: /tenant/tenant_{id}/poc_idea_{n}
- Table naming: tenant_{id}_poc{n}_{table_name}
- Route prefixes: /api/tenant_{id}/poc_idea_{n}
- Router registration pattern in app.py
- Model registration in database.py
- How to add new tenant POC step-by-step
- Shared database vs separate databases (SQLite shared)
- Authentication scope (base auth reused by all tenants)

Reference: tenant_implementation_spec.md Section 2 & 3

### 11. STANDARD POC SKELETON (NEW SECTION - CRITICAL)
Document what EVERY generated POC must include:

**Auto-Generated Components:**
- Admin panel (CRUD UI for all POC tables)
- User management integration (reuses base AuthContext)
- Error handling components (success/error message display)
- Loading states (spinners, loading indicators)

**Required Files:**
- Backend: routes.py, models.py
- Frontend: App.tsx, Dashboard.tsx, {Resource}List.tsx, {Resource}Form.tsx, AdminPanel.tsx
- API utils: api.ts with CRUD functions
- Config: config.ts with API_BASE_URL and POC_PREFIX

**Standard Endpoints Pattern:**
Every POC backend must include:
- GET /{resource} - List all for current user
- POST /{resource} - Create new
- PUT /{resource}/{id} - Update existing
- DELETE /{resource}/{id} - Delete

**Standard Frontend Pattern:**
- 40/60 layout (actions left, data right)
- Reusable form components
- Table/list views with filtering
- Responsive design (Tailwind responsive classes)

Reference: tenant_implementation_spec.md Section 6

### 12. GIT WORKFLOW & DEPLOYMENT (NEW SECTION - CRITICAL)
Document the exact git and deployment strategy:

**Branch Structure:**
```
main (base system - auth, admin, POC agents)
├── tenant/tenant_1 (all tenant_1 POCs)
├── tenant/tenant_2 (all tenant_2 POCs)
└── tenant/tenant_3 (all tenant_3 POCs)
```

**Azure Deployment Instances:**
- main → boot-lang.azurewebsites.net
- tenant/tenant_1 → boot-lang-tenant1.azurewebsites.net
- tenant/tenant_2 → boot-lang-tenant2.azurewebsites.net
- tenant/tenant_3 → boot-lang-tenant3.azurewebsites.net

**Workflow Steps:**
1. Work in tenant branch (git checkout tenant/tenant_1)
2. Merge base updates from main (git merge main)
3. Implement POC
4. Commit and push tenant branch
5. Deployment auto-triggers for that tenant only

**Isolation:**
- Each tenant deploys independently
- Base system remains stable
- One tenant's code cannot break others

Reference: tenant_implementation_spec.md Section 5

### 13. PERFORMANCE & SECURITY BEST PRACTICES (NEW SECTION - CRITICAL)
Document production-ready patterns:

**Performance:**
- When to add indexes (user_id, foreign keys, frequently queried fields)
- Query optimization (select specific columns, use joins wisely)
- Caching strategies (not yet implemented, but document pattern)
- File size limits (recommend 10MB max for uploads)
- Pagination for large lists (limit 50 items per page)

**Security:**
- Input sanitization (validate all user input, use Pydantic schemas)
- SQL injection prevention (always use SQLAlchemy ORM, never raw SQL)
- XSS prevention (React escapes by default, avoid dangerouslySetInnerHTML)
- CSRF protection (JWT tokens, not cookies)
- Password requirements (min 4 chars, bcrypt hashing)
- File upload validation (whitelist extensions, scan for malicious content)
- Environment variables (never hardcode secrets)

**Code Organization:**
- File size limits (components < 300 lines, split if larger)
- When to split components (reusable logic, complex state, >200 lines)
- Function length (< 50 lines, extract helpers)
- Comment requirements (30% coverage for public functions)

### 14. AVAILABLE TOOLS & UTILITIES
List helper functions in:
- auth_utils.py (hash_password, verify_password, create_access_token, etc.)
- frontend/src/utils/auth.ts (setToken, getToken, getAuthHeader, etc.)
- database.py (get_db, init_db)

Include function signatures and usage examples.

### 15. STYLING CONVENTIONS
Document:
- CSS framework (Tailwind CSS)
- Color scheme (blue primary, gray neutral, green success, red error)
- Common utility classes (flex, grid, spacing, typography)
- Layout patterns (40/60 splits, centered forms, message bubbles)
- Responsive breakpoints (sm, md, lg, xl)

### 16. ERROR HANDLING PATTERNS
Document:
- Backend error response format (HTTPException with status_code and detail)
- Frontend error display (bg-red-50 message boxes)
- Common error scenarios (401, 403, 404, 500)
- Logging configuration (console logging for development)

### 17. TESTING PATTERNS
Document:
- Testing framework (pytest for backend, Jest for frontend - not yet implemented)
- Manual testing approach (curl commands, browser testing)
- Where tests should go (/tests/, *.test.tsx)
- Coverage expectations (80%+ for critical paths)

---

## Instructions for Cursor:

1. **Scan the entire codebase** - Read all mentioned files thoroughly
2. **Be specific, not generic** - Include actual endpoint paths, model names, field types
3. **Include working examples** - Real curl commands, real code snippets
4. **Reference tenant_implementation_spec.md** for sections 10, 11, 12
5. **Use consistent formatting** - Follow the markdown structure exactly
6. **Verify accuracy** - Double-check all technical details against source code
7. **Add metadata** - Last updated timestamp, version number at top

## Critical Sections (Must Be Complete):
- Section 10: Tenant Architecture
- Section 11: Standard POC Skeleton
- Section 12: Git Workflow & Deployment
- Section 13: Performance & Security Best Practices

## Output:
Save as: docs/stack_reference.md

## After completion:
Provide summary of:
- Number of endpoints documented
- Number of models documented
- Number of components documented
- Any missing sections or uncertainties
```

---

## This document is ready for implementation when you confirm it's complete.