# Cursor Instructions: Build Stack Reference Document

Copy and paste this into Cursor to generate the comprehensive stack reference document.

---

## Prompt: Create Stack Reference Document

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
- agents/poc_agent_routes.py (if exists)
- Any other *_routes.py or routers

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
For EACH SQLAlchemy model in database.py, document:
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
For EACH reusable component in src/components/, document:
- Component name and file path
- Purpose
- Props interface (name, type, required/optional, description)
- Key features/capabilities
- Usage example

Scan: src/components/*.tsx

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

Reference: Look for auth decorators, middleware, or dependency injection patterns in app.py and related files

### 6. FILE UPLOAD PATTERNS
Document:
- File upload endpoint(s)
- Supported file types
- Size limits
- Storage location
- How to add file upload to new endpoints
- Access/retrieval patterns

Reference: Check for multipart/form-data handling in routes

### 7. DATABASE PATTERNS
Document:
- How to create new tables (SQLAlchemy model pattern)
- How to run migrations/initialize DB
- Session management pattern
- Query examples (CRUD operations)
- Transaction handling

### 8. DIRECTORY STRUCTURE CONVENTIONS
Document the standard project layout:
```
/root
  /frontend
    /src
      /components
      /pages
    package.json
  /backend (or root)
    app.py
    database.py
    /agents
  /tenant
    /tenant_1
      /poc_idea_1
  requirements.txt
  .env
```

Explain where new tenant POC code should live and naming conventions.

### 9. DEPLOYMENT CONFIGURATION
Document:
- Azure deployment setup (if applicable)
- Environment variables required
- Build commands
- Start commands
- CI/CD pipeline overview
- Branch/deployment strategy

Reference: Check for azure-pipelines.yml, .github/workflows/, or deployment scripts

### 10. LANGCHAIN INTEGRATION PATTERNS
Document:
- Available LangChain components in use
- How conversational agents are structured
- Memory management patterns
- Prompt template patterns
- RAG/vector store usage if applicable

Reference: Check agents/ directory, specifically poc_agent.py

### 11. AVAILABLE TOOLS & UTILITIES
List any helper functions, utilities, or shared code:
- Location
- Purpose
- Function signatures
- Usage examples

### 12. STYLING CONVENTIONS
Document:
- CSS framework (Tailwind)
- Color scheme/theme
- Common utility classes
- Layout patterns (40/60 splits, etc.)
- Responsive breakpoints

### 13. ERROR HANDLING PATTERNS
Document:
- Backend error response format
- Frontend error display patterns
- Logging configuration
- Common error scenarios and handling

### 14. TESTING PATTERNS
Document:
- Testing framework if any
- How to run tests
- Test file locations
- Coverage expectations

---

## Instructions for Cursor:

1. **Scan the entire codebase** - Read all mentioned files thoroughly
2. **Be specific, not generic** - Include actual endpoint paths, model names, field types
3. **Include working examples** - Real curl commands, real code snippets
4. **Note what's missing** - If a section has no implementation yet, state "Not yet implemented"
5. **Use consistent formatting** - Follow the markdown structure exactly
6. **Verify accuracy** - Double-check all technical details against source code
7. **Add last updated timestamp** - At the top of the document

## Output:
Save as: docs/stack_reference.md

## After completion:
Show me a summary of what was documented and flag any gaps or uncertainties you encountered.
```

Hold at this point and ask the user for feedback on the stack_reference.md
---

## Follow-up: Python Auto-Regeneration Script

After you've built the initial stack_reference.md using the above instructions, paste this second prompt:

```
Create scripts/regenerate_stack_reference.py that automatically rebuilds docs/stack_reference.md by:

1. Scanning the codebase for changes:
   - Parse all Python files for FastAPI routes (look for @app.get, @router.post, etc.)
   - Parse database.py for SQLAlchemy models
   - Parse src/components/*.tsx for React components
   - Parse requirements.txt for dependencies

2. Extract structured data:
   - Endpoint definitions (path, method, docstring)
   - Model definitions (table name, columns)
   - Component props (using TypeScript interfaces)
   - Package versions

3. Generate markdown sections:
   - Use Jinja2 templates for consistent formatting
   - Preserve manual documentation sections (like "Authentication Patterns")
   - Update only the auto-generated sections

4. Compare and update:
   - Detect changes since last run
   - Update timestamp
   - Preserve custom notes/sections

5. Make it runnable:
   - `python scripts/regenerate_stack_reference.py`
   - Include --dry-run flag to preview changes
   - Include --force flag to overwrite even if no changes

Requirements:
- Use AST parsing for Python files (ast module)
- Use regex for TypeScript parsing (or typescript-ast library if available)
- Generate diff summary showing what changed
- Exit with error if parsing fails (don't overwrite with incomplete data)

Include clear comments explaining each parsing section so we can extend it later.
```

---

**These instructions will:**
1. Build comprehensive initial documentation
2. Create automation to keep it current
3. Make it easy to extend as stack evolves

**Should I refine anything before you feed this to Cursor?**