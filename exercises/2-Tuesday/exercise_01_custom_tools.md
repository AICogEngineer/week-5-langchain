# Exercise 01: Custom Tools

## Overview

You're building a productivity assistant for a development team. The assistant needs tools to help developers with common tasks: searching documentation, calculating estimates, and checking system status.

Your job is to create these tools using LangChain's `@tool` decorator with proper docstrings that help the agent route requests correctly.

## Learning Objectives

- Use the `@tool` decorator from `langchain_core.tools`
- Write docstrings that guide agent tool selection
- Implement proper type hints and return types
- Handle tool errors gracefully

## The Scenario

The product manager wants an assistant that can:
1. **Search documentation** - Find relevant docs based on keywords
2. **Calculate story points** - Estimate work based on complexity
3. **Check service status** - Report on system health

Each tool needs a clear, descriptive docstring so the agent knows when to use it.

## Your Tasks

### Task 1: Documentation Search Tool (20 min)

Implement `search_docs()` in the starter code:
- Accept a search query string
- Return matching documentation entries
- Include a docstring that clearly explains when to use this tool

> **Hint**: The docstring is critical! Include keywords the agent should look for: "documentation", "docs", "how to", "reference".

### Task 2: Story Points Calculator Tool (20 min)

Implement `calculate_story_points()`:
- Accept task description and complexity level
- Return estimated story points with rationale
- Handle edge cases (invalid complexity levels)

> **Hint**: Use type hints like `Literal["low", "medium", "high"]` for the complexity parameter.

### Task 3: Service Status Tool (15 min)

Implement `check_service_status()`:
- Accept a service name
- Return current status (healthy, degraded, down)
- Include realistic response format

### Task 4: Independent Testing (15 min)

Implement `test_tools_independently()`:
- Call each tool directly (not through an agent)
- Verify return types and content
- Print test results

## Definition of Done

- [_] All three tools implemented with `@tool` decorator
- [_] Each tool has descriptive docstrings
- [_] Type hints present for all parameters and returns
- [_] Tools handle edge cases gracefully
- [_] Independent tests pass for all tools

## Testing Your Solution

```bash
cd exercises/2-Tuesday/starter_code
python exercise_01_starter.py
```

Expected output format:
```
=== Tool Testing ===

[INFO] Testing search_docs...
[OK] Tool returned: {'results': [...], 'count': 3}

[INFO] Testing calculate_story_points...
[OK] Tool returned: {'points': 5, 'rationale': '...'}

[INFO] Testing check_service_status...
[OK] Tool returned: {'service': 'api', 'status': 'healthy'}

=== All Tools Tested ===
```

## Docstring Best Practices

```python
@tool
def good_docstring_example(query: str) -> str:
    """Search the knowledge base for relevant documentation.
    
    Use this tool when the user asks about:
    - How to do something
    - Documentation or references
    - API usage examples
    - Configuration options
    
    Args:
        query: The search terms to look for
        
    Returns:
        Matching documentation excerpts
    """
    # Implementation
```

## Stretch Goals (Optional)

1. Add input validation with helpful error messages
2. Implement async versions of tools (`async def`)
3. Add structured output using Pydantic models
