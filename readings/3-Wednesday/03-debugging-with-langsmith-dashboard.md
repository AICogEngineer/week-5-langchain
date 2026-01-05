# Debugging with the LangSmith Dashboard

## Learning Objectives
- Navigate the LangSmith UI effectively
- Inspect individual execution steps
- View inputs and outputs at each stage
- Identify and diagnose agent failures

## Why This Matters

When your agent produces incorrect responses or fails entirely, the LangSmith dashboard is your debugging headquarters. Instead of adding print statements and re-running, you can inspect exactly what happened at every step.

This transforms debugging from guesswork into systematic analysis.

## The Concept

### Dashboard Overview

The LangSmith dashboard has several key areas:

```
┌─────────────────────────────────────────────────────────────────┐
│ LangSmith                                            Profile ▼  │
├─────────────────────────────────────────────────────────────────┤
│ Projects    │ my-project                                        │
│ • Playground│ ┌─────────────────────────────────────────────────│
│ • Datasets  │ │ Recent Traces                                   │
│ • Hub       │ │ ┌─────────────────────────────────────────────  │
│             │ │ │ ✓ customer_support   12:34  2.1s   Success   │
│             │ │ │ ✗ search_agent       12:31  0.4s   Error     │
│             │ │ │ ✓ qa_bot             12:28  1.8s   Success   │
│             │ │ └─────────────────────────────────────────────  │
│             │ └─────────────────────────────────────────────────│
└─────────────────────────────────────────────────────────────────┘
```

### Finding Your Traces

1. **Select your project** from the left sidebar
2. **View recent traces** in the main panel
3. **Filter traces** by:
   - Status (Success/Error)
   - Time range
   - Agent name
   - Search by content

### Inspecting a Trace

Click on any trace to see the detailed view:

```
┌─────────────────────────────────────────────────────────────────┐
│ Run: customer_support_agent                                     │
│ Started: 12:34:56 PM | Duration: 2.1s | Tokens: 847            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Timeline                    Details                            │
│  ─────────                   ───────                            │
│  ▶ customer_support (2.1s)   Status: Success                   │
│    ├─ ChatOpenAI (0.8s)       Tokens: 847                       │
│    ├─ search_kb (1.0s)        Cost: $0.0012                    │
│    └─ ChatOpenAI (0.3s)                                        │
│                                                                 │
│  Click any node to see inputs/outputs                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Viewing Inputs and Outputs

Click on any node in the trace tree to see:

**For LLM calls:**
- Input messages (system, user, assistant, tool)
- Output message (response or tool call)
- Token counts (input/output)
- Model name and parameters

**For tool calls:**
- Function name
- Input arguments
- Return value
- Execution time

### Common Debugging Scenarios

#### Scenario 1: Wrong Tool Selected

**Symptom**: Agent uses `search_web` instead of `search_internal_docs`

**Debug steps**:
1. Find the trace in LangSmith
2. Click on the first ChatOpenAI node
3. View the **Input** → check:
   - Are both tools in the tool list?
   - Are tool descriptions clear?
4. View the **Output** → check:
   - What reasoning led to the wrong choice?

**Solution hints**:
- Improve tool description differentiation
- Add "DO NOT USE FOR" guidance in descriptions
- Adjust system prompt

#### Scenario 2: Tool Returns Unexpected Value

**Symptom**: Tool returns data but agent misinterprets it

**Debug steps**:
1. Find the trace
2. Click on the tool execution node
3. View exact **Input** and **Output**
4. Check if output format is what agent expects

**Solution hints**:
- Standardize tool return formats
- Return strings, not complex objects
- Include context in tool responses

#### Scenario 3: Agent Loops Indefinitely

**Symptom**: Trace shows many LLM calls before completion

**Debug steps**:
1. View the trace timeline
2. Look for repeating patterns
3. Click on each LLM call to see what it decided
4. Identify where the loop starts

**Solution hints**:
- Check for circular tool dependencies
- Improve stopping conditions in prompts
- Add loop detection in tools

### Reading Error Traces

When a trace has errors, LangSmith highlights them:

```
▶ my_agent (Error)
  ├─ ChatOpenAI ✓
  ├─ call_api ✗ ERROR
  │    └─ HTTPError: 500 Server Error
  └─ (halted)
```

Click on the error node to see:
- Exception type
- Error message
- Stack trace
- Input that caused the error

### Using the Comparison View

To compare two traces:

1. Select traces using checkboxes
2. Click "Compare" button
3. View side-by-side execution

Use this to understand:
- Why similar inputs produced different outputs
- What changed between code versions
- How errors differ from successful runs

### Metadata and Tags

Add metadata to traces for better filtering:

```python
# When invoking the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "..."}]},
    config={
        "metadata": {
            "user_id": "user_123",
            "request_type": "order_inquiry",
            "version": "v2.1"
        },
        "tags": ["production", "high-priority"]
    }
)
```

Then filter in the dashboard by these tags and metadata.

### Exporting Traces

For deeper analysis or sharing:

1. Click on a trace
2. Use the "Export" option
3. Choose format (JSON, etc.)
4. Share with teammates or save for records

## Code Example

```python
"""
Creating Traces for Dashboard Debugging
LangChain Version: v1.0+
"""
import os
from langchain.agents import create_agent
from langchain_core.tools import tool

os.environ["LANGSMITH_PROJECT"] = "debugging-demo"

# Tool that might fail
@tool
def risky_api_call(query: str) -> str:
    """Make an API call that might fail."""
    if "error" in query.lower():
        raise Exception("Simulated API Error: Service unavailable")
    return f"API Response for '{query}': Success"

# Tool with unexpected behavior
@tool
def ambiguous_search(query: str) -> str:
    """Search that returns possibly confusing results."""
    # Returns data in inconsistent format
    if len(query) < 5:
        return "No results"
    return f"Found: {query.upper()} | Status: Active | ID: 12345"

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[risky_api_call, ambiguous_search],
    system_prompt="You are a helpful assistant. Use tools when needed.",
    name="debug_demo_agent"
)

print("Creating traces for debugging demonstration...\n")

# Successful case
print("Test 1: Successful call")
try:
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Search for 'widget product'"}]
    })
    print(f"Response: {result['messages'][-1].content}\n")
except Exception as e:
    print(f"Error: {e}\n")

# Potentially confusing case
print("Test 2: Short query (might confuse agent)")
try:
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Search for 'xyz'"}]
    })
    print(f"Response: {result['messages'][-1].content}\n")
except Exception as e:
    print(f"Error: {e}\n")

# Error case
print("Test 3: Triggering an error")
try:
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Make an api call with 'error test'"}]
    })
    print(f"Response: {result['messages'][-1].content}\n")
except Exception as e:
    print(f"Expected error occurred: {e}\n")

print("=" * 50)
print("Now go to LangSmith and inspect these traces!")
print("Project: debugging-demo")
print("\nThings to look for:")
print("1. Successful case: See the full flow")
print("2. Short query: See how 'No results' was handled")
print("3. Error case: See the error details in red")
```

## Key Takeaways

- **Dashboard is debugging HQ**: Central place for all agent execution data
- **Click nodes for details**: Every step has full input/output available
- **Error traces show root cause**: Exception details and stack traces
- **Compare traces**: Understand differences between runs
- **Use metadata for filtering**: Add context to make traces findable
- **Systematic debugging**: Follow the execution path to find issues

## Additional Resources

- [LangSmith Dashboard Guide](https://docs.smith.langchain.com/tracing/faq/logging_and_viewing)
- [Debugging Agent Runs](https://docs.smith.langchain.com/tracing/tutorials/debugging)
- [Trace Filtering and Search](https://docs.smith.langchain.com/tracing/tutorials/filtering)
