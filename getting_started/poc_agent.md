# POC Agent Usage Guide

## What is the POC Agent?

The POC Agent is a Technical Product Manager powered by LangChain that helps you create structured proof-of-concept projects. It acts as your technical consultant, gathering requirements, detecting contradictions, enforcing simplicity, and generating actionable implementation plans.

## LangChain Components

The POC Agent uses several LangChain components:

- **ChatOpenAI**: Interfaces with OpenAI's GPT models for conversational AI
- **ConversationChain**: Manages multi-turn conversations with memory
- **ConversationBufferMemory**: Stores conversation history across sessions
- **RetrievalQA**: Retrieves relevant information from uploaded documents
- **FAISS**: Vector store for semantic document search
- **PydanticOutputParser**: Extracts structured data from LLM responses

## How to Use the POC Builder Interface

### 1. Access the Interface
- Navigate to the main page after logging in
- The POC Builder opens with a 40/60 split layout

### 2. Upload Documents (Left Panel - Documents Tab)
- **Supported formats**: PDF, TXT, MD, PNG, JPG
- **Drag & drop** files into the upload area
- **Wireframes**: Upload PNG/JPG images for UI analysis
- **Requirements docs**: Upload PDF/TXT/MD files for context

### 3. Chat with the Agent (Right Panel)
- **Start conversation**: Describe your POC idea
- **Agent questions**: Answer requirement gathering questions
- **Document context**: Agent automatically uses uploaded files
- **Contradiction detection**: Agent identifies conflicts in requirements
- **Simplicity enforcement**: Agent suggests minimal viable approaches

### 4. Generate POC (Right Panel)
- **Click "Generate POC"** when requirements are complete
- **Agent creates**: Structured markdown files with implementation phases
- **Download ZIP**: Get complete POC package for Cursor AI

## Upload Wireframes and Documents

### Wireframe Analysis
- Upload PNG/JPG images to the Documents tab
- Agent uses GPT-4 Vision to analyze layout, components, and styling
- Analysis is converted to text and stored in vector database
- Agent references wireframe details during requirement gathering

### Document Context
- Upload PDF/TXT/MD files for additional context
- Agent performs semantic search to find relevant information
- Documents are chunked and stored in FAISS vector store
- Context is automatically injected into conversations

## Contradiction Detection Examples

The agent identifies common conflicts:

- **Timeline vs Features**: "You want this done in 2 weeks but requested 15 features"
- **Simplicity vs Complexity**: "You asked for 'simple' but described complex integrations"
- **Frontend vs Backend**: "Frontend needs data that backend doesn't provide"
- **Security vs Usability**: "Security requirements conflict with ease-of-use"

## Customize Prompts in JSON

Edit `agents/poc_agent_prompts.json` to customize:

- **System prompt**: Agent personality and role
- **Requirement questions**: What to ask users
- **Contradiction patterns**: What conflicts to detect
- **Simplicity guidelines**: How to suggest minimal approaches
- **Phase templates**: Structure of generated implementation docs

## Phased Approach Explanation

The agent generates 3-phase implementation plans:

### Phase 1: Frontend
- React + Tailwind CSS setup
- Core UI components and pages
- Mock data integration
- Localhost testing

### Phase 2: Backend
- FastAPI setup
- API endpoints and business logic
- Error handling
- API testing

### Phase 3: Database
- SQLite schema definition
- Data models and relationships
- Database initialization
- Integration testing

## How to Use with Cursor AI

1. **Generate POC**: Use the POC Builder to create your project
2. **Download ZIP**: Get the complete POC package
3. **Extract files**: Unzip to your development directory
4. **Follow phases**: Start with `phase_1_frontend.md`
5. **Use Cursor**: Reference the generated instructions

Example Cursor commands:
```
@poc_name build phase 1
@poc_name implement user authentication
@poc_name add data validation
```

## Good POC Description Examples

### ✅ Effective Descriptions
- "A task management app for small teams with drag-and-drop kanban boards"
- "Customer feedback analyzer that categorizes sentiment and extracts key themes"
- "Inventory tracking system with barcode scanning and low-stock alerts"

### ❌ Poor Descriptions
- "A website" (too vague)
- "An app like Facebook but better" (not specific)
- "Something for managing stuff" (no clear purpose)

## Troubleshooting

### Common Issues

**Agent not responding**:
- Check OpenAI API key in `.env`
- Verify backend is running on port 8000
- Check browser console for errors

**Documents not uploading**:
- Ensure file size < 10MB
- Check file format (PDF, TXT, MD, PNG, JPG only)
- Verify backend storage permissions

**POC generation fails**:
- Ensure requirements are complete
- Check conversation has sufficient detail
- Verify database connection

**Vector store errors**:
- Check FAISS installation
- Verify OpenAI embeddings API access
- Clear vector store cache if corrupted

### Debug Mode
Enable debug logging by setting `LOG_LEVEL=DEBUG` in `.env`

### Support
- Check `getting_started/` for additional guides
- Review `imp_plans/build_poc_agent.md` for implementation details
- Contact admin for technical issues

---

## Quick Start Checklist

- [ ] Login to the platform
- [ ] Navigate to POC Builder
- [ ] Upload any wireframes or documents
- [ ] Describe your POC idea in chat
- [ ] Answer agent's requirement questions
- [ ] Review detected contradictions
- [ ] Accept simplicity suggestions
- [ ] Generate POC when ready
- [ ] Download ZIP file
- [ ] Extract and follow phase instructions
- [ ] Use with Cursor AI for implementation
