# agents/poc_agent.py
import os
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class POCAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def create_poc(self, description: str, user_id: str) -> dict:
        """
        Takes user's idea, generates POC structure with implementation docs
        """
        # Generate POC ID
        poc_id = f"POC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        poc_dir = f"pocs/{user_id}/{poc_id}"
        
        # Create directory structure
        os.makedirs(f"{poc_dir}/frontend", exist_ok=True)
        os.makedirs(f"{poc_dir}/backend", exist_ok=True)
        os.makedirs(f"{poc_dir}/agents", exist_ok=True)
        os.makedirs(f"{poc_dir}/database", exist_ok=True)
        
        # Generate POC description
        poc_desc = self._generate_poc_desc(description)
        
        # Generate implementation document
        imp_doc = self._generate_implementation_doc(description, poc_desc)
        
        # Save documents
        with open(f"{poc_dir}/poc_desc.md", "w") as f:
            f.write(poc_desc)
            
        with open(f"{poc_dir}/imp_document.md", "w") as f:
            f.write(imp_doc)
        
        return {
            "poc_id": poc_id,
            "structure": {
                "poc_dir": poc_dir,
                "files": [
                    "poc_desc.md",
                    "imp_document.md",
                    "frontend/",
                    "backend/",
                    "agents/",
                    "database/"
                ]
            }
        }
    
    def _generate_poc_desc(self, description: str) -> str:
        """Generate POC description from user input"""
        prompt = PromptTemplate(
            input_variables=["description"],
            template="""You are a technical product manager. Based on this user description, create a clear POC description with:

User Description: {description}

Generate:
# POC Description

## Purpose
[Clear statement of what this POC does]

## Users
[Who will use this]

## Key Features
[List 3-5 main features]

## Success Criteria
[How we know it works]
"""
        )
        
        chain = prompt | self.llm
        result = chain.invoke({"description": description})
        return result.content
    
    def _generate_implementation_doc(self, description: str, poc_desc: str) -> str:
        """Generate implementation steps for Cursor"""
        prompt = PromptTemplate(
            input_variables=["description", "poc_desc"],
            template="""You are a senior software architect. Based on this POC, create implementation steps for a developer using Cursor AI.

User Description: {description}

POC Description: {poc_desc}

Generate implementation document with:

# Implementation Steps

## Frontend
[Specific steps for React + Tailwind implementation]

## Backend
[Specific steps for FastAPI implementation]

## Agents
[Specific LangChain agents needed]

## Database
[SQLite schema and tables]

## Integration
[How components connect]

Make steps specific and actionable for @poc_id in Cursor.
"""
        )
        
        chain = prompt | self.llm
        result = chain.invoke({"description": description, "poc_desc": poc_desc})
        return result.content