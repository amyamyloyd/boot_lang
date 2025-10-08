```markdown
# POC Agent Build Instructions for Cursor (LangChain Implementation)

Copy/paste each prompt into Cursor one at a time in order.

---

**Prompt 1: POC Agent Prompt Configuration JSON**
```
Create agents/poc_agent_prompts.json with structured prompt templates:
{
  "version": "1.0",
  "system_prompt": "You are a Technical Product Manager...",
  "requirements_gathering": {
    "initial_questions": [...],
    "frontend_questions": [...],
    "backend_questions": [...],
    "database_questions": [...]
  },
  "contradiction_detection": {
    "patterns": [...],
    "resolution_prompts": [...]
  },
  "simplicity_enforcement": {
    "guidelines": [...],
    "simplification_suggestions": [...]
  },
  "phased_generation": {
    "phase_1_frontend": "...",
    "phase_2_backend": "...",
    "phase_3_database": "..."
  }
}
Make all prompts editable and include version comments for tracking changes.
```

---

**Prompt 2: POC Agent Core System with LangChain**
```
Create agents/poc_agent.py using LangChain components:
- Import ChatOpenAI, ConversationChain, ConversationBufferMemory, PromptTemplate, StructuredOutputParser
- Use gpt-3.5-turbo for cost efficiency
- Load prompts from agents/poc_agent_prompts.json
- Use ConversationChain with ConversationBufferMemory to track multi-turn conversations
- Use PromptTemplate to format system prompts from JSON
- Accept uploaded document IDs as context (wireframes, specs)
- Generate friendly POC names based on user description (e.g., "customer_feedback_analyzer")
- Store conversation history per session in memory
- Main method: process_request(prompt, user_id, document_ids, conversation_history)
- Return structured responses with conversation_id for session tracking
```

---

**Prompt 3: RAG System for Document Context**
```
In agents/poc_agent.py, add RAG (Retrieval Augmented Generation):
- Import FAISS, OpenAIEmbeddings, RetrievalQA from langchain
- Create document loader for PDF, TXT, MD files
- Use OpenAIEmbeddings to create vector embeddings of uploaded documents
- Store embeddings in FAISS vector store per user
- Use RetrievalQA chain to query documents as context during conversation
- When user references uploaded documents, automatically retrieve relevant sections
- Pass retrieved context to ConversationChain for informed responses
```

---

**Prompt 4: Requirements Gathering Chain**
```
In agents/poc_agent.py, create requirements gathering using SequentialChain:
- Chain 1: Ask about application goal and target users using prompts from JSON
- Chain 2: Request frontend requirements (layout, components, styling)
- Chain 3: Ask about backend needs (what data, what operations)
- Chain 4: Identify database requirements
- Use StructuredOutputParser to extract requirements into JSON format
- Accept wireframe uploads (use gpt-4-vision for image analysis)
- Accept CSS file uploads for styling reference
- Store all requirements in structured format
- Validate completeness before proceeding to generation
```

---

**Prompt 5: Contradiction Detection Chain**
```
In agents/poc_agent.py, add contradiction detection using LangChain:
- Create LLMChain with contradiction_detection prompts from JSON
- After each requirement is captured, run contradiction check against previous requirements
- Use StructuredOutputParser to identify conflicts
- If contradictions found, generate clarifying questions using prompts from JSON
- Enforce simplicity using simplicity_enforcement guidelines from JSON
- Always suggest minimal viable approach
- Store contradiction resolutions in conversation history
```

---

**Prompt 6: POC Generation Chain**
```
In agents/poc_agent.py, create POC generation using SequentialChain:
- Chain 1: Generate friendly POC name from description
- Chain 2: Create directory structure: pocs/{user_id}/{friendly_poc_name}/
- Chain 3: Generate poc_desc.md with business goal and features using phased_generation prompts
- Chain 4: Generate requirements.md with captured requirements
- Chain 5: Generate phase_1_frontend.md with Cursor instructions for UI (test in localhost)
- Chain 6: Generate phase_2_backend.md with Cursor instructions for API endpoints
- Chain 7: Generate phase_3_database.md with Cursor instructions for DB models
- Create wireframes/ folder if images uploaded
- Create generated/ folder for Cursor output
- All markdown files must be "agent-ready" - clear, unambiguous instructions for Cursor AI
```

---

**Prompt 7: Document Processing with Vision**
```
Add document processing to agents/poc_agent.py using LangChain:
- Import Document, TextLoader, PyPDFLoader from langchain
- Read uploaded PDFs using PyPDFLoader
- Read TXT and MD files using TextLoader
- For wireframe images (PNG, JPG), use ChatOpenAI with gpt-4-vision-preview model
- Create ImageAnalysisChain that describes wireframe layout, components, and styling
- Extract CSS from uploaded files for styling reference
- Store extracted content with POC for reference in vector store
- Use document content via RetrievalQA to inform requirement questions
```

---

**Prompt 8: Backend Endpoints for POC Agent**
```
Update app.py with POC Agent endpoints:
- POST /api/poc/chat - Chat with POC Agent (prompt, user_id, document_ids, conversation_history)
  - Calls poc_agent.process_request()
  - Returns response and updated conversation_id
- POST /api/poc/generate - Generate final POC structure after requirements gathered
  - Triggers POC generation chain
  - Returns POC directory path and file list
- PUT /api/poc/{poc_id}/update - Update POC requirements and regenerate phases
  - Loads existing POC conversation
  - Updates requirements
  - Regenerates phase markdown files
- GET /api/poc/{poc_id}/files - List all POC files
  - Returns file tree of POC directory
- Return conversation_id to track multi-turn sessions
- Handle LangChain exceptions and return user-friendly errors
```

---

**Prompt 9: Database Models for POC System**
```
Update database.py with POC-related models:
- Document model: id, user_id, filename, file_path, content_text, file_type, created_at
- POC model: id, user_id, poc_id (friendly name), poc_name (display name), description, requirements (JSON), directory, created_at
- POCConversation model: id, poc_id, user_id, conversation_history (JSON), langchain_memory (JSON), created_at
- POCPhase model: id, poc_id, phase_number, phase_name, instructions_file, status, created_at
- Add indexes on user_id and poc_id for query performance
- Include init_db() updates to create new tables
```

---

**Prompt 10: Frontend POC Builder Interface**
```
Create src/components/POCBuilder.tsx with 40/60 layout:

LEFT PANEL (40%):
- Tab switcher: "Documents" and "POCs"
- Documents tab: 
  - File upload dropzone supporting PDF, TXT, MD, PNG, JPG
  - List uploaded documents with preview and delete button
  - Show file type icons
- POCs tab: 
  - List created POCs with friendly names
  - Click to open/edit POC
  - Show POC status (in progress, completed)
- Use Tailwind for styling

RIGHT PANEL (60%):
- Chat interface with POC Agent
- Message history display with user/agent bubbles
- Input field for user messages
- Show typing indicator when agent is processing
- Display POC generation progress with phase indicators
- When POC complete, show POC structure tree
- "Open in Cursor" button showing @poc_name command
- Download POC files button (zip download)
- Show generated phase files with syntax highlighting
```

---

**Prompt 11: POC Agent Documentation**
```
Create getting_started/poc_agent.md explaining:
- What POC Agent does (Technical Product Manager using LangChain for capturing requirements)
- How LangChain components work together (ConversationChain, RAG, SequentialChain)
- How to use POC Builder interface
- How to upload wireframes and documents for context
- How POC Agent asks questions and detects contradictions
- How to customize POC Agent prompts in poc_agent_prompts.json
- Phased approach: frontend first, then backend, then database
- How to use generated POC with Cursor (@poc_name build phase 1)
- Examples of good POC descriptions
- Troubleshooting common issues
```

---

**Prompt 12: POC Agent Prompt Customization Guide**
```
Create getting_started/customizing_poc_agent.md explaining:
- Where prompts are stored (agents/poc_agent_prompts.json)
- JSON structure and how each section is used by LangChain
- How to edit system prompt to change agent behavior
- How to modify requirement gathering questions
- How to adjust contradiction detection patterns
- How to adjust simplicity enforcement rules
- How to customize phased generation templates
- Best practices for prompt engineering with LangChain
- Include before/after examples of prompt modifications
- How to version and track prompt changes
```

---

**Prompt 13: LangChain Dependencies**
```
Update requirements.txt to include all necessary LangChain packages:
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-community>=0.1.0
faiss-cpu>=1.7.0
pypdf>=3.0.0
python-multipart>=0.0.5
tiktoken>=0.5.0

Ensure all imports in poc_agent.py are from correct langchain packages.
```

---

End of instructions.
```