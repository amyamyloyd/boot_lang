# Build Agent System - Complete Implementation

**Purpose:** Build the POC Agent system that transforms ideas into deployable POCs  
**Components:** Orchestration Agent, PRD Agent, Cursor Instructions Agent, projman.mdc  
**Execution:** Copy each prompt into Cursor sequentially, test after each

---

## SYSTEM OVERVIEW

### Architecture
```
User Input
    ↓
Orchestration Agent (routes, manages state)
    ↓
[Stage 1] PRD Agent → generates PRD.md + metadata.json
    ↓
[User Review: "Keep Improving" or "Ready to Implement"]
    ↓
[Stage 2] Cursor Instructions Agent → generates Cursorplan.md
    ↓
User opens Cursor with projman.mdc + Cursorplan → POC built
```

### Directory Structure Created
```
/agents/
  orchestration_agent.py       # NEW - Routes and coordinates
  prd_agent.py                 # NEW - Replaces poc_agent.py
  cursor_instructions_agent.py # NEW - Generates implementation plan
  
/tenant/{tenant_id}/
  poc_idea_{n}/
    idea_metadata_{timestamp}.json
    poc_idea{n}_PRD.md
    poc_idea{n}_Cursorplan_{timestamp}.md

/.cursorrules/
  projman.mdc                  # NEW - Enforcement rules
```

### Files to DELETE
- `agents/poc_agent.py` (overengineered, has RAG/wireframes/contradiction detection)
- `agents/poc_agent_prompts.json` (old template system)

---

## PROMPT 1: Orchestration Agent

```
Create agents/orchestration_agent.py - the traffic controller for the POC Agent system.

PURPOSE:
Routes user requests to correct agent (PRD or Cursor Instructions), manages conversation state, coordinates agent outputs.

IMPLEMENTATION:

```python
"""
Orchestration Agent - Routes and coordinates POC Agent system

Responsibilities:
- Route conversations to PRD Agent or Cursor Instructions Agent
- Track conversation state (ideation, PRD review, implementation planning)
- Load/save conversation sessions
- Coordinate transitions between agents
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class ConversationStage(Enum):
    """Conversation stages in POC generation flow"""
    IDEATION = "ideation"                    # Gathering requirements
    PRD_REVIEW = "prd_review"                # User reviewing generated PRD
    IMPLEMENTATION_PLANNING = "implementation_planning"  # Generating Cursor instructions
    COMPLETE = "complete"                    # Cursor instructions generated

class OrchestrationAgent:
    """
    Orchestrates the POC generation flow between agents.
    Routes requests, manages state, coordinates outputs.
    """
    
    def __init__(self):
        """Initialize orchestration agent"""
        self.current_stage = ConversationStage.IDEATION
        self.conversation_id = None
        self.tenant_id = None
        self.poc_idea_number = None
        self.prd_content = None
        
    def route_request(
        self,
        user_input: str,
        user_id: str,
        conversation_id: Optional[str] = None,
        action: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Route user request to appropriate agent based on stage and action.
        
        Args:
            user_input: User's message
            user_id: User identifier
            conversation_id: Optional conversation to resume
            action: Optional action button ("keep_improving", "ready_to_implement")
            
        Returns:
            dict with:
                - agent: Which agent handled request ("prd", "cursor_instructions")
                - response: Agent response
                - stage: Current conversation stage
                - conversation_id: Session identifier
                - next_actions: Available actions (buttons to show)
        """
        # Load existing conversation if provided
        if conversation_id:
            self._load_conversation(conversation_id)
        else:
            # New conversation
            self.conversation_id = self._generate_conversation_id(user_id)
            self.tenant_id = self._determine_tenant_id(user_id)
            self.poc_idea_number = self._get_next_poc_number(self.tenant_id)
        
        # Handle action buttons
        if action == "keep_improving":
            self.current_stage = ConversationStage.IDEATION
            from .prd_agent import PRDAgent
            prd_agent = PRDAgent()
            response = prd_agent.continue_conversation(user_input, self.conversation_id)
            return self._format_response("prd", response, ["keep_improving", "ready_to_implement"])
        
        elif action == "ready_to_implement":
            self.current_stage = ConversationStage.IMPLEMENTATION_PLANNING
            from .cursor_instructions_agent import CursorInstructionsAgent
            cursor_agent = CursorInstructionsAgent()
            response = cursor_agent.generate_instructions(self.prd_content, self.tenant_id, self.poc_idea_number)
            self.current_stage = ConversationStage.COMPLETE
            return self._format_response("cursor_instructions", response, ["download_instructions"])
        
        # Route based on current stage
        if self.current_stage == ConversationStage.IDEATION:
            from .prd_agent import PRDAgent
            prd_agent = PRDAgent()
            response = prd_agent.process_input(user_input, self.conversation_id)
            
            # Check if PRD is ready
            if response.get("prd_ready"):
                self.current_stage = ConversationStage.PRD_REVIEW
                self.prd_content = response.get("prd_content")
                self._save_prd(self.prd_content)
                return self._format_response("prd", response, ["keep_improving", "ready_to_implement"])
            else:
                return self._format_response("prd", response, [])
        
        elif self.current_stage == ConversationStage.PRD_REVIEW:
            # User should use action buttons, but handle text input as "keep improving"
            self.current_stage = ConversationStage.IDEATION
            from .prd_agent import PRDAgent
            prd_agent = PRDAgent()
            response = prd_agent.continue_conversation(user_input, self.conversation_id)
            return self._format_response("prd", response, ["keep_improving", "ready_to_implement"])
        
        else:
            return {
                "agent": "orchestration",
                "response": "POC generation complete. Download Cursor instructions to begin implementation.",
                "stage": self.current_stage.value,
                "conversation_id": self.conversation_id,
                "next_actions": ["download_instructions"]
            }
    
    def _generate_conversation_id(self, user_id: str) -> str:
        """Generate unique conversation ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"conv_{user_id}_{timestamp}"
    
    def _determine_tenant_id(self, user_id: str) -> str:
        """Determine tenant ID for user (hardcoded for now)"""
        # For now, map users to tenants 1-3
        # TODO: Get from user profile or database
        return "tenant_1"
    
    def _get_next_poc_number(self, tenant_id: str) -> int:
        """Get next POC idea number for tenant"""
        tenant_dir = os.path.join("tenant", tenant_id)
        if not os.path.exists(tenant_dir):
            return 1
        
        # Count existing poc_idea_* directories
        existing = [d for d in os.listdir(tenant_dir) if d.startswith("poc_idea_")]
        return len(existing) + 1
    
    def _save_prd(self, prd_content: str):
        """Save PRD to tenant directory"""
        poc_dir = os.path.join("tenant", self.tenant_id, f"poc_idea_{self.poc_idea_number}")
        os.makedirs(poc_dir, exist_ok=True)
        
        prd_path = os.path.join(poc_dir, f"poc_idea{self.poc_idea_number}_PRD.md")
        with open(prd_path, "w") as f:
            f.write(prd_content)
        
        print(f"✓ Saved PRD to {prd_path}")
    
    def _load_conversation(self, conversation_id: str):
        """Load existing conversation state"""
        # Load from metadata file
        # TODO: Implement metadata loading
        pass
    
    def _format_response(self, agent: str, response: Dict[str, Any], next_actions: list) -> Dict[str, Any]:
        """Format response with standard structure"""
        return {
            "agent": agent,
            "response": response.get("response", ""),
            "stage": self.current_stage.value,
            "conversation_id": self.conversation_id,
            "next_actions": next_actions,
            "prd_content": self.prd_content if self.current_stage == ConversationStage.PRD_REVIEW else None
        }


def test_orchestration():
    """Test orchestration agent"""
    agent = OrchestrationAgent()
    
    # Test 1: New conversation
    result1 = agent.route_request("I want to build a task manager", "user_123")
    print(f"Stage: {result1['stage']}")
    print(f"Agent: {result1['agent']}")
    print(f"Response: {result1['response'][:100]}...")
    
    # Test 2: Ready to implement action
    result2 = agent.route_request("", "user_123", conversation_id=result1['conversation_id'], action="ready_to_implement")
    print(f"Stage: {result2['stage']}")
    print(f"Agent: {result2['agent']}")


if __name__ == "__main__":
    test_orchestration()
```

TESTING:
```bash
python3 agents/orchestration_agent.py
# Should show:
# - Stage progression (ideation → prd_review → implementation_planning)
# - Agent routing (prd, cursor_instructions)
# - Conversation ID generation
```

NEXT: Verify orchestration agent works before proceeding to Prompt 2.
```

---

## PROMPT 2: PRD Agent

```
Create agents/prd_agent.py - conversational requirements gathering that generates PRD.md

PURPOSE:
Replaces poc_agent.py with simple, focused PRD generation. No RAG, no wireframes, no contradiction detection - just conversation → PRD.

DELETE FIRST:
```bash
rm agents/poc_agent.py
rm agents/poc_agent_prompts.json
```

IMPLEMENTATION:

```python
"""
PRD Agent - Product Requirements Document Generator

Gathers requirements through conversation and generates structured PRD.
Uses cheap LLM (GPT-3.5-turbo or Claude Haiku) for cost efficiency.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

load_dotenv()

class PRDAgent:
    """
    Conversational agent for gathering POC requirements and generating PRD.
    
    Questions to cover:
    - What problem does this solve?
    - Who are the users?
    - What value does it provide?
    - What does success look like?
    - Are there similar products?
    - Describe the user flow
    """
    
    def __init__(self):
        """Initialize PRD Agent with cheap LLM"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        # Use cheap model for cost efficiency
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation_id = None
        self.requirements = {}
        
    def process_input(self, user_input: str, conversation_id: str) -> Dict[str, Any]:
        """
        Process user input and gather requirements.
        
        Args:
            user_input: User's message
            conversation_id: Session identifier
            
        Returns:
            dict with response, prd_ready flag, and prd_content if ready
        """
        self.conversation_id = conversation_id
        
        # System prompt for requirements gathering
        system_prompt = """You are a Product Manager helping gather requirements for a POC.

Your job:
1. Ask clarifying questions about the user's idea
2. Understand: problem, users, value, success metrics, user flow
3. Keep it conversational and natural
4. After 5-7 exchanges, you'll have enough to write a PRD

Questions to cover:
- What problem are you solving?
- Who will use this?
- What value does it provide users?
- How do you measure success?
- Are there similar products for reference?
- Walk me through the user flow

Be friendly, ask one question at a time, build on their answers."""

        # Create chat prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Add to memory
        self.memory.chat_memory.add_user_message(user_input)
        
        # Get conversation history
        history = "\n".join([
            f"{'User' if m.type == 'human' else 'Agent'}: {m.content}"
            for m in self.memory.chat_memory.messages
        ])
        
        # Generate response
        chain = prompt | self.llm
        response = chain.invoke({"input": user_input})
        
        self.memory.chat_memory.add_ai_message(response.content)
        
        # Check if ready to generate PRD (after 5+ exchanges)
        num_exchanges = len(self.memory.chat_memory.messages) // 2
        prd_ready = num_exchanges >= 5
        
        result = {
            "response": response.content,
            "prd_ready": prd_ready,
            "conversation_id": self.conversation_id
        }
        
        if prd_ready:
            # Generate PRD
            prd_content = self._generate_prd(history)
            result["prd_content"] = prd_content
            self._save_metadata(history)
        
        return result
    
    def continue_conversation(self, user_input: str, conversation_id: str) -> Dict[str, Any]:
        """Continue conversation after user clicks 'Keep Improving'"""
        return self.process_input(user_input, conversation_id)
    
    def _generate_prd(self, conversation_history: str) -> str:
        """
        Generate PRD from conversation history.
        
        Uses conversation to extract and structure requirements.
        """
        prd_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are writing a Product Requirements Document (PRD) based on a conversation.

Create a comprehensive PRD with these sections:

# Product Requirements Document

**Version:** 1.0
**Date:** {date}
**Status:** Draft

## Executive Summary
[2-3 sentences: what is this, why build it]

## Problem Statement
[What problem does this solve? Pain points?]

## Product Vision
[What does success look like? End goal?]

## Target Users
[Who will use this? User characteristics?]

### User Personas (if discussed)
[Describe 1-2 user types]

## Success Metrics
[How do we measure success? KPIs?]

## Core User Flow
[Step-by-step: user journey through the app]

## Key Features
### Must Have (MVP)
[Essential features for launch]

### Nice to Have (Post-MVP)
[Future enhancements]

## Technical Requirements
[Stack, constraints, integrations mentioned]

## Similar Products
[Competitive landscape, inspiration]

## Assumptions & Constraints
[What are we assuming? What limitations?]

## Open Questions
[What still needs clarification?]

---

Use the conversation history to fill in ALL sections. Be specific and detailed."""),
            ("human", "Conversation:\n{conversation}\n\nGenerate the complete PRD:")
        ])
        
        chain = prd_prompt | self.llm
        result = chain.invoke({
            "conversation": conversation_history,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        
        return result.content
    
    def _save_metadata(self, conversation_history: str):
        """Save conversation metadata to JSON"""
        # Metadata saved by orchestration agent
        # This just prepares the data
        metadata = {
            "conversation_id": self.conversation_id,
            "timestamp": datetime.now().isoformat(),
            "exchanges": len(self.memory.chat_memory.messages) // 2,
            "conversation": conversation_history
        }
        return metadata


def test_prd_agent():
    """Test PRD Agent"""
    agent = PRDAgent()
    
    # Simulate conversation
    conv_id = "test_conv_123"
    
    inputs = [
        "I want to build a task management app for small teams",
        "It solves the problem of teams losing track of who's doing what",
        "Project managers and team members, 5-10 people teams",
        "Success is when teams stop using spreadsheets and sticky notes",
        "Similar to Trello but simpler, just tasks and assignments",
        "User opens app, sees their tasks, adds new task, assigns to teammate"
    ]
    
    for user_input in inputs:
        result = agent.process_input(user_input, conv_id)
        print(f"\nUser: {user_input}")
        print(f"Agent: {result['response'][:100]}...")
        print(f"PRD Ready: {result['prd_ready']}")
        
        if result.get('prd_content'):
            print(f"\n=== GENERATED PRD ===")
            print(result['prd_content'][:500])
            print("...")


if __name__ == "__main__":
    test_prd_agent()
```

TESTING:
```bash
python3 agents/prd_agent.py
# Should show:
# - 6 conversational exchanges
# - PRD generated after 5+ exchanges
# - PRD has all required sections
```

VERIFY:
- agents/poc_agent.py DELETED
- agents/poc_agent_prompts.json DELETED
- PRD generation works

NEXT: Proceed to Prompt 3 only after PRD Agent tested.
```

---

## PROMPT 3: Cursor Instructions Agent

```
Create agents/cursor_instructions_agent.py - generates tactical implementation plan from PRD.

PURPOSE:
Reads stack_reference.md, understands tenant architecture, generates phase-by-phase Cursor instructions.
Uses Claude Sonnet 4.5 for high-quality technical planning.

IMPLEMENTATION:

```python
"""
Cursor Instructions Agent - Generates implementation plans for Cursor AI

Reads:
- PRD (business requirements)
- stack_reference.md (technical capabilities)
- tenant_implementation_spec.md (patterns)

Generates:
- Phased Cursor instructions with testing checkpoints
- Directory structure commands
- Exact file implementations
- Git workflow steps
"""

import os
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

load_dotenv()

class CursorInstructionsAgent:
    """
    Generates detailed Cursor implementation instructions from PRD.
    
    Uses Claude Sonnet 4.5 for high-quality technical planning.
    Knows the full stack from stack_reference.md.
    """
    
    def __init__(self):
        """Initialize with Claude Sonnet 4.5"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0.3,
            api_key=api_key
        )
        
        # Load stack reference
        self.stack_reference = self._load_stack_reference()
        
    def _load_stack_reference(self) -> str:
        """Load stack reference document"""
        stack_ref_path = "docs/stack_reference.md"
        if not os.path.exists(stack_ref_path):
            raise FileNotFoundError(f"Stack reference not found: {stack_ref_path}")
        
        with open(stack_ref_path, "r") as f:
            return f.read()
    
    def generate_instructions(
        self,
        prd_content: str,
        tenant_id: str,
        poc_number: int
    ) -> Dict[str, Any]:
        """
        Generate complete Cursor implementation instructions.
        
        Args:
            prd_content: The PRD markdown
            tenant_id: Tenant identifier (e.g., "tenant_1")
            poc_number: POC idea number (e.g., 1, 2, 3)
            
        Returns:
            dict with instructions_content and file_path
        """
        # Generate instructions using Claude Sonnet 4.5
        instructions_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior technical architect generating implementation instructions for Cursor AI.

You have access to:
1. **Stack Reference Document** - Complete technical capabilities
2. **PRD** - Business requirements
3. **Tenant Implementation Pattern** - How to structure code

Your job:
Generate a complete, phase-by-phase implementation plan that Cursor AI can execute.

CRITICAL REQUIREMENTS:
1. Follow tenant architecture from stack_reference.md Section 10
2. Use standard POC skeleton from stack_reference.md Section 11
3. Follow git workflow from stack_reference.md Section 12
4. Apply security best practices from stack_reference.md Section 13
5. Include testing checkpoints after each phase

STRUCTURE:

# Cursor Implementation Plan: {poc_name}

**Tenant:** {tenant_id}
**POC Number:** {poc_number}
**Generated:** {date}

## Overview
[1 paragraph: what we're building]

## Phase 1: Setup & Directory Structure

### Step 1: Create Branch
```bash
git checkout -b {tenant_id}/poc_idea_{poc_number}
git merge main
```

### Step 2: Create Directory Structure
```bash
mkdir -p tenant/{tenant_id}/poc_idea_{poc_number}/backend
mkdir -p tenant/{tenant_id}/poc_idea_{poc_number}/frontend/src/components
mkdir -p tenant/{tenant_id}/poc_idea_{poc_number}/frontend/src/utils
```

### Step 3: Initialize Files
[List all files to create with exact paths]

**TESTING CHECKPOINT:**
- Verify directory structure exists
- All files created

---

## Phase 2: Backend Implementation

### Step 1: Database Models
Create `tenant/{tenant_id}/poc_idea_{poc_number}/backend/models.py`:
```python
[EXACT CODE - complete implementation]
```

### Step 2: API Routes
Create `tenant/{tenant_id}/poc_idea_{poc_number}/backend/routes.py`:
```python
[EXACT CODE - complete CRUD endpoints]
```

### Step 3: Register in app.py
Add to `app.py`:
```python
[EXACT LINES TO ADD]
```

### Step 4: Register Models in database.py
Add to `database.py` init_db():
```python
[EXACT IMPORT LINE]
```

### Step 5: Run Migration
```bash
python3 -c "from database import init_db; init_db()"
```

**TESTING CHECKPOINT:**
```bash
# Start backend
python3 app.py

# Test endpoints
export TOKEN="your_jwt_token"
curl http://localhost:8000/api/{tenant_id}/poc_idea_{poc_number}/tasks \
  -H "Authorization: Bearer $TOKEN"

# Should return empty list or data
```

**Git Checkpoint:**
```bash
git add tenant/{tenant_id}/poc_idea_{poc_number}/backend/
git add app.py database.py
git commit -m "Add backend: models and routes"
```

---

## Phase 3: Frontend Implementation

### Step 1: Configuration
Create `frontend/src/config.ts`:
```typescript
[EXACT CODE]
```

### Step 2: API Utils
Create `utils/api.ts`:
```typescript
[EXACT CODE - all CRUD functions]
```

### Step 3: Components
Create each component:

**Dashboard.tsx:**
```typescript
[EXACT CODE]
```

**ItemList.tsx:**
```typescript
[EXACT CODE]
```

**ItemForm.tsx:**
```typescript
[EXACT CODE]
```

**AdminPanel.tsx:**
```typescript
[EXACT CODE]
```

### Step 4: Main App
Update `App.tsx` to add route:
```typescript
[EXACT CODE TO ADD]
```

**TESTING CHECKPOINT:**
```bash
cd tenant/{tenant_id}/poc_idea_{poc_number}/frontend
npm install
npm start

# Opens on http://localhost:3001
# Verify:
# - Can navigate to POC route
# - Can see dashboard
# - Can fetch data from backend
```

**Git Checkpoint:**
```bash
git add tenant/{tenant_id}/poc_idea_{poc_number}/frontend/
git add frontend/src/App.tsx
git commit -m "Add frontend: components and routing"
```

---

## Phase 4: Integration & Testing

### Full Integration Test
1. Backend running (port 8000)
2. Frontend running (port 3001)
3. Login as test user
4. Navigate to `/{tenant_id}/poc_idea_{poc_number}/dashboard`
5. Create new item
6. Verify item appears in list
7. Edit item
8. Delete item
9. Verify admin panel shows all data

### Database Verification
```bash
sqlite3 boot_lang.db "SELECT * FROM {tenant_id}_poc{poc_number}_tasks;"
# Should show created data
```

**Final Git Checkpoint:**
```bash
git add .
git commit -m "Integration complete: {poc_name}"
git push origin {tenant_id}/poc_idea_{poc_number}
```

---

## Phase 5: Deployment

Push to tenant branch triggers Azure deployment to:
`boot-lang-{tenant_id}.azurewebsites.net`

Access at:
`https://boot-lang-{tenant_id}.azurewebsites.net/{tenant_id}/poc_idea_{poc_number}/dashboard`

---

## Complete Implementation Checklist

Backend:
- [ ] Models created with correct table name
- [ ] Routes registered in app.py
- [ ] Models imported in database.py
- [ ] Migration run successfully
- [ ] All CRUD endpoints tested

Frontend:
- [ ] Config file created with API_BASE_URL
- [ ] API utils created with all functions
- [ ] All components implemented
- [ ] Route added to main App.tsx
- [ ] npm start works without errors

Integration:
- [ ] Can create data
- [ ] Can read data
- [ ] Can update data
- [ ] Can delete data
- [ ] Admin panel works
- [ ] Data persists across restarts

Deployment:
- [ ] Branch pushed
- [ ] Azure deployment successful
- [ ] Production URL accessible

---

END OF INSTRUCTIONS

Use the PRD and stack reference to generate COMPLETE, WORKING code for each phase.
Include ALL imports, ALL fields, ALL error handling.
Make it copy-paste ready for Cursor AI."""),
            ("human", """Generate complete Cursor instructions for this POC.

**PRD:**
{prd}

**Stack Reference (for your reference):**
{stack_reference}

**Tenant ID:** {tenant_id}
**POC Number:** {poc_number}

Generate the complete implementation plan with EXACT code for all files.""")
        ])
        
        # Generate instructions
        chain = instructions_prompt | self.llm
        result = chain.invoke({
            "prd": prd_content,
            "stack_reference": self.stack_reference,
            "tenant_id": tenant_id,
            "poc_number": poc_number,
            "poc_name": self._extract_poc_name(prd_content),
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        
        instructions_content = result.content
        
        # Save to tenant directory
        poc_dir = os.path.join("tenant", tenant_id, f"poc_idea_{poc_number}")
        os.makedirs(poc_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"poc_idea{poc_number}_Cursorplan_{timestamp}.md"
        file_path = os.path.join(poc_dir, filename)
        
        with open(file_path, "w") as f:
            f.write(instructions_content)
        
        print(f"✓ Saved Cursor instructions to {file_path}")
        
        return {
            "instructions_content": instructions_content,
            "file_path": file_path,
            "response": f"Cursor implementation plan generated. {len(instructions_content)} characters."
        }
    
    def _extract_poc_name(self, prd: str) -> str:
        """Extract POC name from PRD"""
        lines = prd.split("\n")
        for line in lines:
            if line.startswith("# ") and "Product Requirements" in line:
                return line.replace("# Product Requirements Document:", "").replace("#", "").strip()
        return "POC"


def test_cursor_instructions_agent():
    """Test Cursor Instructions Agent"""
    agent = CursorInstructionsAgent()
    
    # Sample PRD
    sample_prd = """# Product Requirements Document: Task Manager

## Executive Summary
Simple task management app for small teams.

## Problem Statement
Teams lose track of tasks in spreadsheets.

## Target Users
Project managers and team members (5-10 person teams).

## Key Features
- Create tasks
- Assign to team members
- Mark complete
- View all team tasks"""
    
    result = agent.generate_instructions(
        prd_content=sample_prd,
        tenant_id="tenant_1",
        poc_number=1
    )
    
    print(f"✓ Instructions generated: {result['file_path']}")
    print(f"Content length: {len(result['instructions_content'])} chars")
    print("\nFirst 500 chars:")
    print(result['instructions_content'][:500])


if __name__ == "__main__":
    test_cursor_instructions_agent()
```

TESTING:
```bash
python3 agents/cursor_instructions_agent.py
# Should show:
# - Instructions file created in tenant/tenant_1/poc_idea_1/
# - Complete phased implementation plan
# - Exact code for all files
```

VERIFY:
- Cursor instructions include all phases
- Code is complete (not placeholders)
- Testing checkpoints at each phase
- Git workflow included

NEXT: Proceed to Prompt 4 only after Cursor Instructions Agent tested.
```

---

## PROMPT 4: projman.mdc Rules

```
Create .cursorrules/projman.mdc - enforcement rules for Cursor AI to follow during POC implementation.

PURPOSE:
Ensures Cursor AI follows best practices, tests at checkpoints, commits to git regularly, doesn't waste tokens.

IMPLEMENTATION:

Create `.cursorrules/projman.mdc`:

```markdown
# Project Manager Rules (projman.mdc)

**Purpose:** Governance rules for POC implementation with Cursor AI  
**Scope:** Applies when implementing Cursor instructions (Cursorplan.md files)  
**Model:** Claude Sonnet 4.5 (max mode)

---

##