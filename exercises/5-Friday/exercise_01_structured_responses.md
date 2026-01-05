# Exercise 01: Structured Responses

## Overview

LLMs naturally produce free-form text, but production applications often need structured data. In this exercise, you'll use Pydantic models with LangChain to enforce reliable, validated output from your agents.

## Learning Objectives

- Define output schemas using Pydantic models
- Configure the `response_format` parameter
- Handle validation errors gracefully
- Build agents that return structured JSON

## The Scenario

Your product team needs agents that return consistent, parseable data:
1. A **Task Analyzer** that outputs structured complexity assessments
2. A **Content Extractor** that extracts specific fields from text
3. An **Error Handler** that gracefully handles invalid outputs

## Your Tasks

### Task 1: Define Output Schemas (20 min)

Create Pydantic models in the starter code:

**TaskAnalysis Schema:**
```python
class TaskAnalysis(BaseModel):
    task_name: str
    complexity: Literal["low", "medium", "high"]
    estimated_hours: float
    required_skills: list[str]
    risks: list[str]
    recommendation: str
```

**ContentExtraction Schema:**
```python
class ContentExtraction(BaseModel):
    title: str
    summary: str
    key_points: list[str]
    sentiment: Literal["positive", "negative", "neutral"]
```

> **Hint**: Use `Field(description="...")` to help the LLM understand each field.

### Task 2: Structured Agent Creation (25 min)

Implement `create_structured_agent()`:
- Use `create_agent()` with `response_format` parameter
- Pass your Pydantic model as the response format
- Create agents that output structured data

### Task 3: Output Validation (20 min)

Implement `validate_and_process_output()`:
- Parse the agent's structured response
- Validate that all required fields are present
- Handle cases where validation fails

### Task 4: Error Handling (15 min)

Implement `handle_structured_errors()`:
- Test with inputs that might cause validation errors
- Implement retry logic for failed responses
- Provide fallback values when needed

## Definition of Done

- [_] Pydantic schemas defined with proper field descriptions
- [_] Agent returns structured TaskAnalysis output
- [_] Agent returns structured ContentExtraction output
- [_] Validation catches malformed responses
- [_] Error handling provides graceful fallbacks

## Testing Your Solution

```bash
cd exercises/5-Friday/starter_code
python exercise_01_starter.py
```

Expected output:
```
=== Structured Output Test ===

[INFO] Testing TaskAnalysis output...
{
  "task_name": "API Integration",
  "complexity": "medium",
  "estimated_hours": 8.0,
  "required_skills": ["Python", "REST APIs", "Testing"],
  "risks": ["Third-party API changes", "Rate limiting"],
  "recommendation": "Start with sandbox testing"
}
[OK] TaskAnalysis validated successfully

[INFO] Testing ContentExtraction output...
{
  "title": "Quarterly Report Summary",
  "summary": "Revenue increased 15% year-over-year...",
  "key_points": ["Revenue up 15%", "New product launch", ...],
  "sentiment": "positive"
}
[OK] ContentExtraction validated successfully

=== All Structured Outputs Valid ===
```

## Key Patterns

```python
from pydantic import BaseModel, Field
from typing import Literal

class MyOutput(BaseModel):
    """Describe what this output represents."""
    
    field_one: str = Field(
        description="What this field contains"
    )
    field_two: Literal["a", "b", "c"] = Field(
        description="One of the allowed values"
    )
    field_three: list[str] = Field(
        default_factory=list,
        description="List of items"
    )

# Create agent with structured output
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    response_format=MyOutput,
    name="structured_agent"
)

# Invoke and get typed response
result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
output: MyOutput = result["structured_output"]  # Typed!
```

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Missing descriptions | LLM doesn't understand field purpose | Always use `Field(description=...)` |
| Too many fields | Output is unreliable | Keep schemas focused (5-7 fields max) |
| No validation | Silent failures | Always validate output against schema |
| No fallback | Application crashes | Provide default values or retry |

## Stretch Goals (Optional)

1. Create nested Pydantic models (model within model)
2. Implement custom validators with `@field_validator`
3. Compare structured output across different models
4. Measure reliability rates for complex schemas
