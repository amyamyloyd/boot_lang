# Customizing the POC Agent

## Prompt Storage Location

All POC Agent prompts are stored in `agents/poc_agent_prompts.json`. This JSON file contains:

- System prompts
- Requirement gathering questions
- Contradiction detection patterns
- Simplicity enforcement guidelines
- Phase generation templates

## JSON Structure Explanation

```json
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
    "phase_1_frontend_template": "...",
    "phase_2_backend_template": "...",
    "phase_3_database_template": "..."
  }
}
```

## Edit System Prompt

The system prompt defines the agent's personality and role:

```json
"system_prompt": "You are a Technical Product Manager with 10+ years of experience building web applications. You excel at gathering requirements, identifying contradictions, and enforcing simplicity. Your goal is to help users create focused, implementable POC projects."
```

**Customization tips**:
- Adjust experience level
- Change personality traits
- Modify expertise areas
- Update goal statements

## Modify Requirement Questions

### Initial Questions
```json
"initial_questions": [
  "What is the main goal or purpose of this application?",
  "Who are the primary users or target audience?",
  "Can you describe the core workflow a user would follow in 2-3 sentences?"
]
```

### Frontend Questions
```json
"frontend_questions": [
  "What are the main pages or views needed for the frontend?",
  "What UI components do you anticipate (e.g., forms, tables, charts, dashboards)?",
  "Do you have any specific layout or styling preferences?"
]
```

### Backend Questions
```json
"backend_questions": [
  "What data entities will the backend manage?",
  "What API endpoints will be required?",
  "Are there any complex business logic or integrations?"
]
```

### Database Questions
```json
"database_questions": [
  "What are the main tables and their relationships?",
  "What are the key fields for each table?",
  "Are there any specific data types or constraints?"
]
```

## Contradiction Detection Patterns

Add new patterns to detect conflicts:

```json
"patterns": [
  "User requests both 'simple' and 'complex' features for the same component",
  "User specifies a very short timeline but requests extensive features",
  "Frontend requirements imply data not supported by backend/database requirements",
  "Security requirements conflict with ease-of-use requirements",
  "Your custom pattern here"
]
```

## Resolution Prompts

Customize how the agent handles contradictions:

```json
"resolution_prompts": [
  "It seems there might be a conflict between X and Y. Could you clarify which is a higher priority for this POC?",
  "To keep the POC focused, we might need to simplify Z. Would you prefer to prioritize A or B?",
  "Your custom resolution prompt here"
]
```

## Simplicity Enforcement Guidelines

Define what "simple" means for your use case:

```json
"guidelines": [
  "Prioritize core functionality over advanced features for a POC",
  "Suggest minimal viable UI/UX for initial validation",
  "Avoid unnecessary integrations unless critical for core functionality",
  "Focus on one primary user flow for the initial iteration",
  "Your custom guideline here"
]
```

## Simplification Suggestions

Customize how the agent suggests simpler approaches:

```json
"simplification_suggestions": [
  "Let's start with the most critical feature (X) and iterate from there",
  "For the POC, we can use a simplified version of Y and expand later",
  "Instead of Z, how about we implement A for now to validate the core idea?",
  "Your custom suggestion here"
]
```

## Phase Generation Templates

### Frontend Template
```json
"phase_1_frontend_template": "# Frontend Implementation (Phase 1) for @poc_name\n\nThis phase focuses on building the core user interface using React and Tailwind CSS..."
```

**Template variables**:
- `@poc_name`: Replaced with friendly POC name
- `@requirements`: Replaced with gathered requirements
- `@wireframes`: Replaced with wireframe analysis

### Backend Template
```json
"phase_2_backend_template": "# Backend Implementation (Phase 2) for @poc_name\n\nThis phase focuses on building the core API endpoints using FastAPI..."
```

### Database Template
```json
"phase_3_database_template": "# Database Implementation (Phase 3) for @poc_name\n\nThis phase focuses on defining the SQLite database schema..."
```

## Customization Examples

### Example 1: E-commerce Focus
```json
{
  "system_prompt": "You are a Technical Product Manager specializing in e-commerce applications...",
  "requirements_gathering": {
    "initial_questions": [
      "What products will be sold in this e-commerce platform?",
      "What payment methods need to be supported?",
      "What inventory management features are required?"
    ]
  }
}
```

### Example 2: Mobile-First Approach
```json
{
  "simplicity_enforcement": {
    "guidelines": [
      "Prioritize mobile-first responsive design",
      "Focus on touch-friendly interactions",
      "Minimize complex navigation patterns"
    ]
  }
}
```

### Example 3: Enterprise Focus
```json
{
  "contradiction_detection": {
    "patterns": [
      "User requests both 'simple' and 'enterprise-grade' features",
      "Security requirements conflict with rapid deployment needs",
      "Scalability requirements exceed POC scope"
    ]
  }
}
```

## Best Practices

### 1. Keep Questions Specific
- Avoid vague questions like "What features do you want?"
- Use specific questions like "What data will users input?"

### 2. Test Contradiction Patterns
- Add patterns based on common user conflicts
- Test with real user conversations
- Refine based on detection accuracy

### 3. Maintain Consistency
- Keep tone consistent across all prompts
- Use similar language patterns
- Align with your organization's style

### 4. Version Control
- Track changes to prompt files
- Test changes in development environment
- Document customization rationale

## Applying Changes

1. **Edit JSON file**: Modify `agents/poc_agent_prompts.json`
2. **Restart backend**: Changes take effect on next request
3. **Test conversation**: Verify new prompts work as expected
4. **Monitor performance**: Check if changes improve user experience

## Troubleshooting Customizations

### Agent Not Following New Prompts
- Ensure JSON syntax is valid
- Check for missing commas or brackets
- Restart backend service

### Contradiction Detection Not Working
- Verify pattern syntax matches user input
- Test patterns with sample conversations
- Check resolution prompts are appropriate

### Phase Templates Not Generating
- Ensure template variables are correct
- Check for proper markdown formatting
- Verify template completeness

---

## Quick Customization Checklist

- [ ] Identify customization needs
- [ ] Edit `agents/poc_agent_prompts.json`
- [ ] Validate JSON syntax
- [ ] Test with sample conversation
- [ ] Restart backend service
- [ ] Verify changes work as expected
- [ ] Document customization rationale
- [ ] Update team on changes
