# Instructions for Creating 100% Reliable Code Documentation

## 📋 **Pre-Work Verification Checklist**

Before writing ANY documentation, complete this verification:

### **1. Code Structure Verification**
- [ ] List ALL files in the target directory
- [ ] Read the first 50 lines of EVERY file to understand purpose
- [ ] Identify ALL classes, functions, and methods
- [ ] Map ALL imports and dependencies
- [ ] Document ALL file relationships

### **2. Method Implementation Verification**
- [ ] Read the COMPLETE body of EVERY method you document
- [ ] Trace EVERY code path through conditional statements
- [ ] Verify EVERY parameter is used correctly
- [ ] Check EVERY return value matches documentation
- [ ] Test EVERY example code snippet by reading the implementation

### **3. Behavior Verification**
- [ ] Read the ACTUAL implementation of each claimed behavior
- [ ] Verify EVERY step in documented processes
- [ ] Check EVERY error condition and edge case
- [ ] Confirm EVERY interaction between components
- [ ] Validate EVERY data flow and transformation

### **4. Cross-Reference Verification**
- [ ] Verify EVERY referenced file exists
- [ ] Read EVERY referenced function/class
- [ ] Check EVERY endpoint URL against actual routes
- [ ] Validate EVERY database table/field reference
- [ ] Confirm EVERY external dependency

### **5. Example Code Verification**
- [ ] Write EVERY example as if you were implementing it
- [ ] Verify EVERY parameter value is correct
- [ ] Check EVERY import statement
- [ ] Test EVERY method call syntax
- [ ] Confirm EVERY expected output

## 🚫 **Documentation Rules**

### **NEVER Document Without Verification**
- If you haven't read the complete implementation, DON'T document it
- If you can't trace the code execution, DON'T claim it works
- If you haven't verified a behavior, DON'T describe it
- If you can't find the referenced code, DON'T reference it

### **ALWAYS State Verification Level**
- "Verified by reading complete implementation"
- "Verified by tracing code execution"
- "Verified by checking actual file contents"
- "Not verified - requires implementation review"

### **ALWAYS Include Verification Evidence**
- Quote specific code lines that support claims
- Reference specific file paths and line numbers
- Include actual method signatures from code
- Show actual endpoint URLs from route definitions

## 📝 **Documentation Template**

For each component:

```
## Component Name

**Verification Status:** [VERIFIED/UNVERIFIED/PARTIAL]

**Implementation Evidence:**
- File: `/path/to/file.py` lines 1-50
- Method: `def method_name(self, param: str) -> Dict[str, Any]`
- Verified behavior: [specific code quote]

**Actual Implementation:**
[Quote relevant code sections]

**Verified Behavior:**
1. [Behavior] - Verified by reading lines X-Y in file.py
2. [Behavior] - Verified by tracing execution path
3. [Behavior] - Verified by checking actual method body

**Unverified Claims:**
- [Any behavior not verified by reading code]

**Example Code (Verified):**
```python
# Verified by checking actual constructor signature
instance = ClassName("param1", "param2")
# Verified by reading method implementation
result = instance.method_name("input")
```

**Cross-References (Verified):**
- File `/path/to/file.py` exists ✓
- Function `function_name()` exists at line X ✓
- Endpoint `/api/endpoint` exists in app.py line Y ✓
```

## ⚠️ **Failure Conditions**

**STOP and report if:**
- You cannot read the complete implementation
- You cannot trace the code execution
- You cannot verify a claimed behavior
- You cannot find referenced files/functions
- You cannot confirm example code works

**DO NOT proceed with documentation if any verification fails.**

## 🎯 **Success Criteria**

Documentation is only complete when:
- [ ] Every claim is backed by specific code evidence
- [ ] Every example has been verified against implementation
- [ ] Every cross-reference has been confirmed to exist
- [ ] Every behavior has been traced through actual code
- [ ] Verification status is clearly stated for each component

**If you cannot meet these criteria, the documentation is incomplete and unreliable.**
