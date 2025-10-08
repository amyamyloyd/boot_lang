POC BUILDER COMPLETE REDESIGN:

LEFT PANEL (40%):
- File upload dropzone for documents (PDF, TXT, MD)
- List of uploaded documents with delete option
- List of created POCs with open/edit options
- Simple menu to switch between "Documents" and "POCs" views

RIGHT PANEL (60%):
- Chat interface with POC Agent
- User can say "build a POC for [uploaded document]" or "create a POC that does X"
- Agent reads uploaded documents as context
- Agent generates POC with:
  - poc_desc.md (what it does)
  - imp_document.md (implementation steps for Cursor)
  - Creates new route/page for the POC
  - Generates frontend component
  - Generates backend endpoint
  - Generates database models if needed
- Shows POC output: description, implementation steps, generated files
- "Open in Cursor" button that shows @poc_id command

BACKEND REQUIREMENTS:
- POST /api/documents/upload - save documents, extract text
- GET /api/documents/list - list user's documents
- DELETE /api/documents/{id}
- POST /api/poc/create - POC Agent reads documents + prompt, generates full POC structure
- GET /api/poc/list - list user's POCs
- POC Agent uses uploaded documents as RAG context

DATABASE ADDITIONS:
- Document model: id, user_id, filename, file_path, content_text, created_at
- POC model: id, user_id, poc_id, description, generated_files (JSON), directory, created_at

POC AGENT ENHANCEMENT:
- Accept uploaded document IDs as context
- Generate complete POC including:
  - Frontend component code
  - Backend endpoint code
  - Database models if needed
  - All in proper directory structure under pocs/{user_id}/{poc_id}/

This creates a working POC generation system using your infrastructure.