# Tuesday: Tools & Simple Agents

## Exercise Schedule

| Exercise | Type | Duration | Prerequisites |
|----------|------|----------|---------------|
| 01: Custom Tools | Implementation | 60-75 min | Reading 01-02, Demo 01 |
| 02: First Agent | Implementation | 75-90 min | Reading 03-05, Demo 02-03 |

## Learning Objectives

By completing these exercises, you will:
- Create custom tools using the `@tool` decorator
- Write effective tool docstrings for agent routing
- Build agents using `create_agent()` with the required `name` parameter
- Test tools independently before integrating with agents

## Before You Begin

1. **Complete the readings** in `readings/2-Tuesday/`
2. **Watch/run demos** in `demos/2-Tuesday/code/`
3. Ensure you have API keys configured:
   ```bash
   export OPENAI_API_KEY="your-key"
   ```

## Exercises

### Exercise 01: Custom Tools (Implementation)
See [exercise_01_custom_tools.md](exercise_01_custom_tools.md)
Starter code: `starter_code/exercise_01_starter.py`

Create custom tools for a productivity assistant using the `@tool` decorator with proper docstrings and type hints.

### Exercise 02: First Agent (Implementation)
See [exercise_02_first_agent.md](exercise_02_first_agent.md)
Starter code: `starter_code/exercise_02_starter.py`

Build a complete agent using `create_agent()` that combines multiple tools with a system prompt.

## Estimated Time
**Total: 2.5-3 hours**

## Key v1.0 Patterns to Practice

```python
from langchain_core.tools import tool
from langchain.agents import create_agent

# Tool creation with @tool decorator
@tool
def my_tool(query: str) -> str:
    """Description that helps agent decide when to use this tool."""
    return f"Result for {query}"

# Agent creation (ALWAYS include name)
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[my_tool],
    system_prompt="You are a helpful assistant.",
    name="my_agent"  # REQUIRED in v1.0
)
```

> **Warning**: Always provide the `name` parameter. Unnamed agents cause issues with tracing and debugging.
