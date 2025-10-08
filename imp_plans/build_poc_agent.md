# Implementation Plan: POC Agent System with LangChain

## Project Information
- **Project Name**: Boot_Lang POC Agent (Technical Product Manager AI)
- **Created By**: AI Assistant
- **Date**: 2025-10-08
- **Priority**: High
- **Estimated Effort**: 8-10 hours

## Overview
### Problem Statement
Boot_Lang needs a conversational AI agent that acts as a Technical Product Manager to gather requirements from users, detect contradictions, enforce simplicity, and generate structured POC documentation with phased implementation instructions for Cursor AI.

### Solution Summary
Build a LangChain-based conversational agent that uses RAG for document context, sequential chains for requirements gathering, contradiction detection, and generates phased POC documentation. Users chat with the agent, upload wireframes/specs, and receive structured implementation plans split into frontend, backend, and database phases.

### Success Criteria
- [ ] Users can chat with POC Agent in conversational interface
- [ ] Agent loads prompts from editable JSON configuration
- [ ] Agent can process uploaded documents (PDF, TXT, MD) via RAG
- [ ] Agent can analyze wireframe images using GPT-4 Vision
- [ ] Agent gathers requirements through guided conversation
- [ ] Agent detects contradictions and enforces simplicity
- [ ] Agent generates friendly POC names (e.g., "customer_feedback_analyzer")
- [ ] Agent creates POC directory structure: `pocs/{user_id}/{friendly_name}/`
- [ ] Agent generates 5 markdown files: poc_desc.md, requirements.md, phase_1_frontend.md, phase_2_backend.md, phase_3_database.md
- [ ] Frontend has 40/60 layout with documents/POCs list and chat interface
- [ ] Users can view POC file tree and download POC as ZIP
- [ ] All prompts are version-controlled and editable

## Technical Requirements

### Core Tech Stack (NEVER CHANGE)
- **Frontend**: React 19 + axios + react-router-dom v6 + Tailwind CSS
- **Backend**: Python 3.11 + FastAPI + SQLAlchemy + SQLite
- **LLM Framework**: LangChain + OpenAI (gpt-3.5-turbo for chat, gpt-4-vision for images)
- **Vector Store**: FAISS (local, per-user)
- **Database**: SQLite (boot_lang.db)

### Dependencies
#### New Dependencies Required
- [ ] langchain>=0.1.0 - Core LangChain framework
- [ ] langchain-openai>=0.1.0 - OpenAI LLM integration
- [ ] langchain-community>=0.1.0 - Community tools and loaders
- [ ] faiss-cpu>=1.7.0 - Vector store for RAG
- [ ] pypdf>=3.0.0 - PDF document loading
- [ ] python-multipart>=0.0.5 - File upload handling
- [ ] tiktoken>=0.5.0 - Token counting for OpenAI

#### Existing Dependencies Used
- [ ] FastAPI - Backend API framework
- [ ] SQLAlchemy - Database ORM
- [ ] axios - HTTP client for frontend
- [ ] Tailwind CSS - Styling

### Database Changes
- [ ] Create Document table: id, user_id, filename, file_path, content_text, file_type, created_at
- [ ] Create POC table: id, user_id, poc_id (friendly_name), poc_name (display), description, requirements (JSON), directory, created_at
- [ ] Create POCConversation table: id, poc_id, user_id, conversation_history (JSON), langchain_memory (JSON), created_at
- [ ] Create POCPhase table: id, poc_id, phase_number, phase_name, instructions_file, status, created_at
- [ ] Add indexes on user_id and poc_id

### API Changes
#### New Endpoints to Create
- [ ] POST /api/poc/upload - Upload documents (PDF, TXT, MD, PNG, JPG)
- [ ] GET /api/poc/documents - List user's uploaded documents
- [ ] DELETE /api/poc/documents/{doc_id} - Delete document
- [ ] POST /api/poc/chat - Chat with POC Agent (prompt, user_id, document_ids, conversation_history)
- [ ] POST /api/poc/generate - Generate final POC structure after requirements gathered
- [ ] GET /api/poc/list - List user's POCs
- [ ] GET /api/poc/{poc_id}/files - Get POC file tree
- [ ] GET /api/poc/{poc_id}/download - Download POC as ZIP
- [ ] PUT /api/poc/{poc_id}/update - Update POC and regenerate phases

## Implementation Phases

### Phase 1: Prompt Configuration & Agent Foundation
**Duration**: 1.5 hours
**Dependencies**: None

#### Tasks
- [ ] Create agents/poc_agent_prompts.json with full structure:
  - [ ] system_prompt (Technical Product Manager personality)
  - [ ] requirements_gathering (initial, frontend, backend, database questions)
  - [ ] contradiction_detection (patterns, resolution_prompts)
  - [ ] simplicity_enforcement (guidelines, simplification_suggestions)
  - [ ] phased_generation (phase_1_frontend, phase_2_backend, phase_3_database templates)
  - [ ] Include version field and comments for tracking
- [ ] Add langchain packages to requirements.txt
- [ ] Create agents/poc_agent.py with POCAgent class skeleton
- [ ] Implement __init__ with ChatOpenAI (gpt-3.5-turbo, temp=0.7)
- [ ] Implement load_prompts() method to read JSON config
- [ ] Implement generate_friendly_name() method using LLM

#### Deliverables
- [ ] /agents/poc_agent_prompts.json - Complete prompt templates
- [ ] /agents/poc_agent.py - Agent skeleton with LLM initialization
- [ ] Updated requirements.txt

#### Testing
- [ ] Verify JSON loads without errors
- [ ] Test LLM connection with simple prompt
- [ ] Test friendly name generation (e.g., "Build a customer feedback tool" → "customer_feedback_analyzer")

#### Phase Review
**STOP**: Compare what was implemented in Phase 1 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 2.

### Phase 2: Conversational Core & Memory
**Duration**: 2 hours
**Dependencies**: Phase 1 complete

#### Tasks
- [ ] Import ConversationChain, ConversationBufferMemory, PromptTemplate
- [ ] Create process_request(prompt, user_id, document_ids, conversation_history) method
- [ ] Initialize ConversationChain with ConversationBufferMemory
- [ ] Load conversation history from database if exists
- [ ] Use system_prompt from JSON as base prompt
- [ ] Return structured response: {response, conversation_id, agent_state}
- [ ] Implement save_conversation() to persist to database
- [ ] Implement load_conversation() to restore from database

#### Deliverables
- [ ] Conversational agent with memory in poc_agent.py
- [ ] Conversation persistence methods

#### Testing
- [ ] Test multi-turn conversation with memory
- [ ] Test conversation save/load
- [ ] Verify agent personality matches system_prompt

#### Phase Review
**STOP**: Compare what was implemented in Phase 2 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 3.

### Phase 3: RAG System for Document Context
**Duration**: 2 hours
**Dependencies**: Phase 2 complete

#### Tasks
- [ ] Import FAISS, OpenAIEmbeddings, RetrievalQA from langchain
- [ ] Import Document, TextLoader, PyPDFLoader from langchain_community
- [ ] Create load_document(file_path, file_type) method
  - [ ] Handle PDF with PyPDFLoader
  - [ ] Handle TXT/MD with TextLoader
- [ ] Create create_vector_store(documents, user_id) method
  - [ ] Use OpenAIEmbeddings
  - [ ] Store in FAISS per user: `vector_stores/{user_id}/`
- [ ] Create retrieve_context(query, user_id) method using RetrievalQA
- [ ] Update process_request() to inject retrieved context into prompt

#### Deliverables
- [ ] Document loading methods in poc_agent.py
- [ ] FAISS vector store creation and retrieval
- [ ] RAG integration into conversation flow

#### Testing
- [ ] Upload test PDF, verify text extraction
- [ ] Upload test TXT, verify embedding creation
- [ ] Test context retrieval with sample queries
- [ ] Verify context injection into conversation

#### Phase Review
**STOP**: Compare what was implemented in Phase 3 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 4.

### Phase 4: Requirements Gathering Chain
**Duration**: 2 hours
**Dependencies**: Phase 3 complete

#### Tasks
- [ ] Import StructuredOutputParser from langchain
- [ ] Create requirements_schema using Pydantic or JSON schema
- [ ] Create gather_requirements() method using SequentialChain:
  - [ ] Chain 1: Ask about application goal/users (using initial_questions from JSON)
  - [ ] Chain 2: Request frontend requirements (using frontend_questions)
  - [ ] Chain 3: Ask backend needs (using backend_questions)
  - [ ] Chain 4: Identify database requirements (using database_questions)
- [ ] Use StructuredOutputParser to extract requirements to JSON
- [ ] Store requirements in agent state
- [ ] Validate completeness before allowing generation

#### Deliverables
- [ ] Requirements gathering chain in poc_agent.py
- [ ] Structured output parsing
- [ ] Requirements validation logic

#### Testing
- [ ] Test full requirements gathering flow
- [ ] Verify JSON structure of captured requirements
- [ ] Test incomplete requirements validation

#### Phase Review
**STOP**: Compare what was implemented in Phase 4 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 5.

### Phase 5: Contradiction Detection & Simplicity Enforcement
**Duration**: 1.5 hours
**Dependencies**: Phase 4 complete

#### Tasks
- [ ] Import LLMChain from langchain
- [ ] Create detect_contradictions(requirements) method using LLMChain
  - [ ] Use contradiction_detection prompts from JSON
  - [ ] Compare new requirement against previous requirements
  - [ ] Return list of conflicts
- [ ] Create suggest_simplification(requirements) method
  - [ ] Use simplicity_enforcement guidelines from JSON
  - [ ] Suggest minimal viable approach
- [ ] Update process_request() to run contradiction check after each requirement
- [ ] Generate clarifying questions if contradictions found
- [ ] Store contradiction resolutions in conversation history

#### Deliverables
- [ ] Contradiction detection chain in poc_agent.py
- [ ] Simplicity enforcement logic
- [ ] Clarifying question generation

#### Testing
- [ ] Test with contradictory requirements (e.g., "simple UI" then "complex dashboard")
- [ ] Verify clarifying questions generated
- [ ] Test simplification suggestions

#### Phase Review
**STOP**: Compare what was implemented in Phase 5 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 6.

### Phase 6: POC Generation Chain
**Duration**: 2 hours
**Dependencies**: Phase 5 complete

#### Tasks
- [ ] Create generate_poc(requirements, user_id) method using SequentialChain:
  - [ ] Chain 1: Generate friendly POC name
  - [ ] Chain 2: Create directory: `pocs/{user_id}/{friendly_poc_name}/`
  - [ ] Chain 3: Generate poc_desc.md (business goal, features, success criteria)
  - [ ] Chain 4: Generate requirements.md (captured requirements)
  - [ ] Chain 5: Generate phase_1_frontend.md (Cursor instructions for UI, test in localhost)
  - [ ] Chain 6: Generate phase_2_backend.md (Cursor instructions for API)
  - [ ] Chain 7: Generate phase_3_database.md (Cursor instructions for DB)
  - [ ] Create wireframes/ folder if images uploaded
  - [ ] Create generated/ folder for Cursor output
- [ ] Use phased_generation prompts from JSON
- [ ] Ensure markdown files are "agent-ready" for Cursor
- [ ] Return POC structure with file list

#### Deliverables
- [ ] POC generation chain in poc_agent.py
- [ ] Directory structure creation
- [ ] All 5 markdown files generated

#### Testing
- [ ] Test end-to-end POC generation
- [ ] Verify directory structure created
- [ ] Verify all markdown files readable and formatted
- [ ] Test friendly name uniqueness

#### Phase Review
**STOP**: Compare what was implemented in Phase 6 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 7.

### Phase 7: Image Analysis with GPT-4 Vision
**Duration**: 1.5 hours
**Dependencies**: Phase 6 complete

#### Tasks
- [ ] Create analyze_wireframe(image_path) method
  - [ ] Use ChatOpenAI with gpt-4-vision-preview model
  - [ ] Create ImageAnalysisChain
  - [ ] Extract layout, components, styling from image
  - [ ] Return structured description
- [ ] Update load_document() to handle PNG, JPG
- [ ] Store wireframe analysis in vector store
- [ ] Copy wireframe images to `pocs/{user_id}/{poc_name}/wireframes/`
- [ ] Reference wireframes in phase_1_frontend.md

#### Deliverables
- [ ] Image analysis with GPT-4 Vision in poc_agent.py
- [ ] Wireframe processing and storage

#### Testing
- [ ] Upload test wireframe image
- [ ] Verify layout description accuracy
- [ ] Test wireframe context in requirements gathering

#### Phase Review
**STOP**: Compare what was implemented in Phase 7 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 8.

### Phase 8: Database Models
**Duration**: 1 hour
**Dependencies**: None (can run in parallel)

#### Tasks
- [ ] Update database.py with new models:
  - [ ] Document model: id, user_id, filename, file_path, content_text, file_type, created_at
  - [ ] POC model: id, user_id, poc_id (friendly), poc_name (display), description, requirements (JSON), directory, created_at
  - [ ] POCConversation model: id, poc_id, user_id, conversation_history (JSON), langchain_memory (JSON), created_at
  - [ ] POCPhase model: id, poc_id, phase_number, phase_name, instructions_file, status, created_at
- [ ] Add indexes on user_id and poc_id
- [ ] Update init_db() to create new tables
- [ ] Create test script to verify schema

#### Deliverables
- [ ] Updated /database.py with POC models
- [ ] Database migration/initialization

#### Testing
- [ ] Run init_db() and verify tables created
- [ ] Test model creation and queries
- [ ] Verify JSON field storage

#### Phase Review
**STOP**: Compare what was implemented in Phase 8 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 9.

### Phase 9: Backend API Endpoints
**Duration**: 2 hours
**Dependencies**: Phase 8 complete, Phase 6 for agent integration

#### Tasks
- [ ] Create poc_api.py with FastAPI router
- [ ] Implement POST /api/poc/upload (file upload with type validation)
- [ ] Implement GET /api/poc/documents (list user documents)
- [ ] Implement DELETE /api/poc/documents/{doc_id}
- [ ] Implement POST /api/poc/chat (call poc_agent.process_request())
- [ ] Implement POST /api/poc/generate (call poc_agent.generate_poc())
- [ ] Implement GET /api/poc/list (list user POCs)
- [ ] Implement GET /api/poc/{poc_id}/files (return file tree)
- [ ] Implement GET /api/poc/{poc_id}/download (ZIP download)
- [ ] Implement PUT /api/poc/{poc_id}/update (regenerate phases)
- [ ] Add LangChain exception handling with user-friendly errors
- [ ] Update app.py to include poc_api router

#### Deliverables
- [ ] /poc_api.py - All POC endpoints
- [ ] Updated app.py

#### Testing
- [ ] Test file upload (PDF, TXT, MD, PNG, JPG)
- [ ] Test chat endpoint with multi-turn conversation
- [ ] Test POC generation end-to-end
- [ ] Test file tree retrieval
- [ ] Test ZIP download
- [ ] Test error handling

#### Phase Review
**STOP**: Compare what was implemented in Phase 9 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 10.

### Phase 10: Frontend POC Builder Interface
**Duration**: 3 hours
**Dependencies**: Phase 9 complete

#### Tasks
- [ ] Create src/components/POCBuilder.tsx with 40/60 layout
- [ ] LEFT PANEL (40%):
  - [ ] Tab switcher: "Documents" and "POCs"
  - [ ] Documents tab:
    - [ ] File upload dropzone (PDF, TXT, MD, PNG, JPG)
    - [ ] Document list with preview and delete button
    - [ ] File type icons
  - [ ] POCs tab:
    - [ ] List created POCs with friendly names
    - [ ] Click to open/edit POC
    - [ ] Show POC status (in progress, completed)
- [ ] RIGHT PANEL (60%):
  - [ ] Chat interface with POC Agent
  - [ ] Message history (user/agent bubbles)
  - [ ] Input field for messages
  - [ ] Typing indicator when agent processing
  - [ ] POC generation progress with phase indicators
  - [ ] POC structure tree when complete
  - [ ] "Open in Cursor" button with @poc_name command
  - [ ] Download POC button (ZIP)
  - [ ] Generated phase files with syntax highlighting
- [ ] Style with Tailwind CSS
- [ ] Add to App.tsx routing

#### Deliverables
- [ ] /frontend/src/components/POCBuilder.tsx
- [ ] Updated /frontend/src/App.tsx

#### Testing
- [ ] Test file upload UI
- [ ] Test document list and delete
- [ ] Test chat interface with agent
- [ ] Test multi-turn conversation display
- [ ] Test POC generation progress display
- [ ] Test file tree display
- [ ] Test ZIP download
- [ ] Test responsive layout

#### Phase Review
**STOP**: Compare what was implemented in Phase 10 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete before proceeding to Phase 11.

### Phase 11: Documentation
**Duration**: 1.5 hours
**Dependencies**: Phase 10 complete

#### Tasks
- [ ] Create getting_started/poc_agent.md:
  - [ ] What POC Agent does
  - [ ] LangChain components explanation
  - [ ] How to use POC Builder interface
  - [ ] Upload wireframes and documents
  - [ ] Contradiction detection examples
  - [ ] Customize prompts in JSON
  - [ ] Phased approach explanation
  - [ ] How to use with Cursor (@poc_name build phase 1)
  - [ ] Good POC description examples
  - [ ] Troubleshooting
- [ ] Create getting_started/customizing_poc_agent.md:
  - [ ] Prompt storage location
  - [ ] JSON structure explanation
  - [ ] Edit system prompt
  - [ ] Modify requirement questions
  - [ ] Adjust contradiction patterns
  - [ ] Adjust simplicity rules
  - [ ] Customize phased templates
  - [ ] Prompt engineering best practices
  - [ ] Before/after examples
  - [ ] Version tracking
- [ ] Update architecture/agents.md with POCAgent
- [ ] Update architecture/endpoints.md with POC endpoints
- [ ] Update architecture/schemas.md with POC models

#### Deliverables
- [ ] /getting_started/poc_agent.md
- [ ] /getting_started/customizing_poc_agent.md
- [ ] Updated /architecture/* files

#### Testing
- [ ] Documentation review for accuracy
- [ ] Test all examples in documentation
- [ ] Verify JSON customization examples work

#### Phase Review
**STOP**: Compare what was implemented in Phase 11 against the tasks and deliverables listed in this plan. Verify all checkboxes are complete. Review Success Criteria at top of document to confirm full implementation.

## File Structure

### Files to Create
```
/
├── agents/
│   ├── poc_agent.py - Complete POC Agent with LangChain
│   └── poc_agent_prompts.json - Editable prompt templates
├── poc_api.py - POC Agent API endpoints
├── vector_stores/ - FAISS vector stores per user (gitignored)
└── pocs/ - Generated POC directories (gitignored)
    └── {user_id}/
        └── {friendly_poc_name}/
            ├── poc_desc.md
            ├── requirements.md
            ├── phase_1_frontend.md
            ├── phase_2_backend.md
            ├── phase_3_database.md
            ├── wireframes/ - Uploaded images
            └── generated/ - Cursor output

/getting_started/
├── poc_agent.md - POC Agent usage guide
└── customizing_poc_agent.md - Prompt customization guide

/frontend/src/components/
└── POCBuilder.tsx - 40/60 layout POC builder interface
```

### Files to Modify
```
/
├── app.py - Add poc_api router
├── database.py - Add Document, POC, POCConversation, POCPhase models
├── requirements.txt - Add LangChain packages
└── .gitignore - Add vector_stores/, pocs/

/frontend/src/
└── App.tsx - Add POCBuilder route
```

### Files to Delete
```
None (existing poc_agent.py will be completely rewritten)
```

## Environment Variables
```
# Already in .env
OPENAI_API_KEY=your-openai-api-key

# No new env vars needed
```

## Sign-off

### Stakeholder Approval
- [ ] User - [Date]

---

## Notes
- Use gpt-3.5-turbo for cost efficiency in chat (gpt-4 only for vision)
- FAISS vector stores are per-user, stored locally
- POC directories created on-demand in pocs/{user_id}/
- All prompts in JSON for easy editing without code changes
- Phased approach: frontend first (testable in localhost), then backend, then database
- Generated markdown files are "Cursor-ready" - clear, actionable instructions
- Conversation history persists in database with LangChain memory
- ZIP download for easy POC sharing
- Contradiction detection runs after each requirement capture
- Simplicity enforcement always suggests minimal viable approach

## Change Log
| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-08 | 1.0 | Initial implementation plan | AI Assistant |

---

## 📎 File Checklist

- [ ] Placed in `/imp_plans/`
- [ ] References poc_builder.md instructions
- [ ] Contains 11 clear phases
- [ ] Includes folder/file paths and package names
- [ ] Documents all major deliverables and artifacts
- [ ] Follows guard.mdc structure

