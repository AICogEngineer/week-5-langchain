# Tracing Agent Execution

## Learning Objectives
- Understand how LangSmith automatically traces LangChain operations
- Read and interpret trace hierarchies
- Identify what gets captured in traces
- Use trace information for understanding agent behavior

## Why This Matters

When an agent runs, dozens of operations happen under the hood—LLM calls, tool executions, state updates. Without tracing, you're left guessing. With tracing, you have a complete record of exactly what happened, when, and why.

Tracing transforms agent development from art to science.

## The Concept

### Automatic Tracing

Once LangSmith is configured, tracing is automatic. Every LangChain operation is captured:

```python
# No special code needed - just run your agent
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_tool, calculate_tool],
    name="demo_agent"
)

# This run is automatically traced
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
# Trace appears in LangSmith dashboard within seconds
```

### What Gets Traced

LangSmith captures comprehensive information:

| Component | Captured Data |
|-----------|---------------|
| **Agent Run** | Start time, end time, status, agent name |
| **LLM Calls** | Prompt, response, tokens, latency, model |
| **Tool Calls** | Tool name, arguments, return value |
| **State Changes** | Messages added, state mutations |
| **Errors** | Exception type, message, stack trace |

### Trace Hierarchy

Traces form a tree structure showing parent-child relationships:

```
Run: "customer_support_agent" (4.2s)
├── ChatOpenAI (0.8s)
│   ├── Input: [SystemMessage, HumanMessage]
│   └── Output: AIMessage with tool_call
├── search_knowledge_base (1.1s)
│   ├── Input: {"query": "return policy"}
│   └── Output: "Our return policy allows..."
├── ChatOpenAI (0.9s)
│   ├── Input: [SystemMessage, HumanMessage, AIMessage, ToolMessage]
│   └── Output: AIMessage (final response)
└── Total tokens: 847 (input: 623, output: 224)
```

### Understanding the Trace View

When you click on a trace in LangSmith, you see:

1. **Timeline**: Visual representation of execution order and duration
2. **Input/Output**: What went in and came out of each step
3. **Metadata**: Tokens, latency, cost estimates
4. **Errors**: Any failures with full details

### Tracing Multi-Step Agent Runs

Agents that call multiple tools create richer traces:

```python
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M")

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: 72°F, sunny"

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_time, get_weather],
    system_prompt="You are a helpful assistant.",
    name="multi_tool_agent"
)

# This will make multiple tool calls
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What time is it and what's the weather in Seattle?"}
    ]
})
```

**Resulting trace:**
```
Run: "multi_tool_agent"
├── ChatOpenAI → decides to call tools
├── get_time() → "14:30"
├── get_weather("Seattle") → "Weather in Seattle: 72°F, sunny"
├── ChatOpenAI → synthesizes final answer
└── "It's 2:30 PM and the weather in Seattle is 72°F and sunny."
```

### Trace Properties

Each trace node has properties:

```
┌─────────────────────────────────────────────────────────┐
│ Name: ChatOpenAI                                        │
│ Status: Success ✓                                       │
│ Duration: 823ms                                         │
│ Tokens: 412 (input: 289, output: 123)                  │
│                                                         │
│ Input:                                                  │
│   messages: [                                           │
│     {"role": "system", "content": "You are..."},       │
│     {"role": "user", "content": "What's the weather?"} │
│   ]                                                     │
│                                                         │
│ Output:                                                 │
│   AIMessage(content="Let me check...",                 │
│             tool_calls=[{name: "get_weather", ...}])   │
└─────────────────────────────────────────────────────────┘
```

### Identifying Trace Patterns

Look for these patterns in traces:

**Healthy patterns:**
- Linear sequence: LLM → Tool → LLM → Response
- Reasonable latency (LLM calls < 2-3 seconds typically)
- Successful tool executions

**Warning patterns:**
- Multiple consecutive LLM calls without tools (agent might be confused)
- Very high token counts (inefficient prompts)
- Long tool execution times (external API issues)
- Error status on any node

### Filtering and Finding Traces

LangSmith provides search and filtering:

- **By project**: Switch between projects in sidebar
- **By status**: Filter success/error/pending
- **By name**: Search for specific agent names
- **By time**: Recent, last hour, last day, custom range
- **By metadata**: Filter by tags and properties

### Trace Comparison

Compare traces to understand differences:

1. Select multiple traces
2. Click "Compare"
3. See side-by-side execution differences

Use this to:
- Compare successful vs. failed runs
- Analyze different prompt variations
- Debug why two similar inputs produced different outputs

### Programmatic Trace Access

You can also query traces via the LangSmith SDK:

```python
from langsmith import Client

client = Client()

# Get recent traces
traces = client.list_runs(
    project_name="my-project",
    execution_order=1,  # Root traces only
    error=False,        # Successful only
    limit=10
)

for trace in traces:
    print(f"{trace.name}: {trace.total_tokens} tokens, {trace.latency_s:.2f}s")
```

## Code Example

```python
"""
Tracing Agent Execution Demo
LangChain Version: v1.0+
"""
import os
from langchain.agents import create_agent
from langchain_core.tools import tool

# Ensure tracing is enabled
os.environ["LANGSMITH_PROJECT"] = "tracing-demo"

@tool
def lookup_order(order_id: str) -> str:
    """Look up an order by ID."""
    # Simulated lookup
    orders = {
        "ORD-001": "Shipped, arriving tomorrow",
        "ORD-002": "Processing, ships in 2 days",
    }
    return orders.get(order_id, f"Order {order_id} not found")

@tool
def lookup_product(product_id: str) -> str:
    """Look up product information."""
    products = {
        "PROD-A": "Widget Pro - $49.99, In Stock",
        "PROD-B": "Gadget Plus - $89.99, Low Stock",
    }
    return products.get(product_id, f"Product {product_id} not found")

# Create agent
support_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_order, lookup_product],
    system_prompt="""You are a customer support agent.
    Use tools to look up orders and products.
    Never make up information - always use tools.""",
    name="customer_support_agent"
)

# Run scenarios that create interesting traces
print("Running scenarios for tracing demonstration...\n")

# Scenario 1: Simple order lookup (one tool call)
print("Scenario 1: Order lookup")
result = support_agent.invoke({
    "messages": [
        {"role": "user", "content": "Where is my order ORD-001?"}
    ]
})
print(f"Response: {result['messages'][-1].content}\n")

# Scenario 2: Complex question (multiple tools possible)
print("Scenario 2: Order and product lookup")
result = support_agent.invoke({
    "messages": [
        {"role": "user", "content": "Check order ORD-002 and tell me about product PROD-B"}
    ]
})
print(f"Response: {result['messages'][-1].content}\n")

# Scenario 3: Not found case
print("Scenario 3: Item not found")
result = support_agent.invoke({
    "messages": [
        {"role": "user", "content": "What's the status of order ORD-999?"}
    ]
})
print(f"Response: {result['messages'][-1].content}\n")

print("=" * 50)
print("Check LangSmith dashboard to see these traces!")
print(f"Project: tracing-demo")
print("Look for:")
print("  - Single tool call (Scenario 1)")
print("  - Multiple tool calls (Scenario 2)")
print("  - Not found handling (Scenario 3)")
```

## Key Takeaways

- **Tracing is automatic**: No code changes needed once configured
- **Traces are hierarchical**: Parent-child relationships show execution flow
- **Everything is captured**: LLM calls, tools, tokens, latency, errors
- **Use traces to understand behavior**: See exactly what the agent decided to do
- **Look for patterns**: Healthy vs. warning patterns indicate issues
- **Compare traces**: Understand differences between runs

## Additional Resources

- [LangSmith Tracing Concepts](https://docs.smith.langchain.com/tracing/concepts)
- [Understanding Traces](https://docs.smith.langchain.com/tracing/faq/logging_and_viewing)
- [LangSmith SDK Reference](https://docs.smith.langchain.com/reference/sdk)
