# Simple Agent Creation with `create_agent()`

## Learning Objectives
- Understand what agents are and how they differ from simple chat models
- Create agents using the `create_agent()` function
- Configure required parameters: model, tools, system_prompt, and name
- Invoke agents and process their responses

## Why This Matters

Agents represent a quantum leap from simple chatbots. While a chat model can only generate text, an agent can *reason about what actions to take* and then *execute those actions* using tools. This is what enables AI systems to actually *do things*—not just talk about doing them.

In our **"From Basics to Production"** journey, `create_agent()` is your primary building block. It's the fastest path from "I have an idea" to "I have a working agent."

## The Concept

### What is an Agent?

An agent is an LLM-powered system that can:
1. **Observe** the current situation (user message, conversation history)
2. **Reason** about what to do next
3. **Act** by calling tools or generating responses
4. **Repeat** until the task is complete

```
                    ┌─────────────────────────┐
                    │         Agent           │
                    │                         │
User Message ───────▶  Observe → Reason → Act ◀───┐
                    │              │           │   │
                    │              ▼           │   │
                    │         Tool Call  ──────────┘
                    │              │           │
                    │              ▼           │
                    │      Generate Response  │
                    │              │           │
                    └──────────────┼───────────┘
                                   ▼
                            Final Response
```

### The Agentic Loop

Agents operate in a loop that the LLM controls:

1. **Model receives**: Messages + tool descriptions
2. **Model decides**: Respond directly OR call a tool
3. **If tool call**: Execute tool, add result to messages, go to step 1
4. **If response**: Return the response to the user

This loop is called the **ReAct pattern** (Reasoning and Acting). In v1.0, `create_agent()` implements this automatically.

### `create_agent()` Parameters

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",           # Required: Model to use
    tools=[tool1, tool2],                  # Required: List of tools
    system_prompt="You are helpful.",      # Optional: System instructions
    name="my_agent",                       # Required: Agent name
    checkpointer=None                      # Optional: Memory (covered Thursday)
)
```

#### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | str | Model specification in provider:model format |
| `tools` | List[BaseTool] | List of tools the agent can use |
| `name` | str | Unique name for tracing and debugging |

#### Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `system_prompt` | str | Instructions that guide agent behavior |
| `checkpointer` | BaseCheckpointer | Memory storage (covered Thursday) |
| `middleware` | List | Context engineering hooks (covered Week 6) |

### Basic Agent Example

```python
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In real use, this would call a weather API
    return f"The weather in {city} is 72°F and sunny."

# Create the agent - just 5 lines!
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful weather assistant.",
    name="weather_agent"
)
```

### Invoking Agents

Agents are invoked with a message dictionary:

```python
# Basic invocation
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What's the weather in Seattle?"}
    ]
})

# Access the response
response = result["messages"][-1].content
print(response)  # "The weather in Seattle is 72°F and sunny."
```

### Understanding the Response

The `invoke()` result contains:
- `messages`: Complete conversation including tool calls and responses
- Additional state (if using memory—covered Thursday)

```python
result = agent.invoke({"messages": [{"role": "user", "content": "Hi!"}]})

# result["messages"] might contain:
# [
#     {"role": "user", "content": "Hi!"},
#     AIMessage(content="Hello! How can I help you today?")
# ]
```

### Agents vs. Direct Model Calls

| Aspect | Model (`.invoke()`) | Agent (`create_agent()`) |
|--------|---------------------|--------------------------|
| Can call tools | No | Yes |
| Multi-step reasoning | No | Yes |
| Automatic iteration | No | Yes |
| Memory built-in | No | Via checkpointer |
| Best for | Simple Q&A | Complex tasks |

### When NOT to Use Agents

Not every problem needs an agent:

- **Simple Q&A**: Direct model call is faster
- **Fixed workflows**: Known sequence of steps (use manual LangGraph)
- **No tools needed**: Agent overhead isn't justified

**Use agents when**: You need tool usage, multi-step reasoning, or the LLM should decide what to do next.

### System Prompts for Agents

The system prompt shapes agent behavior:

```python
# Minimal prompt
system_prompt = "You are a helpful assistant."

# Detailed prompt with tool guidance
system_prompt = """You are a customer service agent for Acme Corp.

Your tools:
- search_orders: Look up order status
- create_ticket: Open support tickets

Guidelines:
- Always greet customers warmly
- Ask clarifying questions if the request is unclear
- Use search_orders before suggesting new orders
- Escalate to a ticket if you can't resolve the issue

Tone: Professional but friendly."""
```

### Multiple Tools Example

```python
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> str:
    """Add two numbers."""
    return f"{a} + {b} = {a + b}"

@tool
def multiply(a: int, b: int) -> str:
    """Multiply two numbers."""
    return f"{a} × {b} = {a * b}"

@tool
def divide(a: float, b: float) -> str:
    """Divide two numbers."""
    if b == 0:
        return "Error: Cannot divide by zero"
    return f"{a} ÷ {b} = {a / b}"

# Agent with multiple tools
calculator_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[add, multiply, divide],
    system_prompt="You are a calculator. Use tools for all math operations.",
    name="calculator_agent"
)

# The agent will choose the right tool based on the question
result = calculator_agent.invoke({
    "messages": [{"role": "user", "content": "What's 15 times 8?"}]
})
# Agent calls multiply(15, 8) → "15 × 8 = 120"
```

## Code Example

```python
"""
Creating Simple Agents with create_agent()
LangChain Version: v1.0+
Documentation: https://docs.langchain.com/oss/python/langchain
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from datetime import datetime

# Define some useful tools
@tool
def get_current_time() -> str:
    """Get the current time. Use when asked about the time."""
    return datetime.now().strftime("%I:%M %p")

@tool
def get_current_date() -> str:
    """Get today's date. Use when asked about the date."""
    return datetime.now().strftime("%B %d, %Y")

@tool
def calculate_days_until(target_date: str) -> str:
    """
    Calculate days until a target date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
    """
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        delta = target - today
        
        if delta.days < 0:
            return f"That date was {abs(delta.days)} days ago."
        elif delta.days == 0:
            return "That's today!"
        else:
            return f"{delta.days} days until {target_date}."
    except ValueError:
        return "Please provide date in YYYY-MM-DD format."

# Create the agent
date_time_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_current_time, get_current_date, calculate_days_until],
    system_prompt="""You are a helpful assistant that answers questions about 
dates and times. Use your tools to give accurate information.""",
    name="datetime_agent"
)

# Test various queries
queries = [
    "What time is it?",
    "What's today's date?",
    "How many days until 2025-01-01?",
    "What time is it and what's the date?"  # May use multiple tools!
]

for query in queries:
    print(f"\nUser: {query}")
    result = date_time_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    print(f"Agent: {result['messages'][-1].content}")
```

## Key Takeaways

- **Agents reason and act**: They decide what tools to use, not just generate text
- **`create_agent()` is the v1.0 way**: Simple, clean, handles the loop for you
- **Four key parameters**: model, tools, system_prompt, and name
- **Name is required**: Essential for tracing and debugging
- **Invoke with messages**: `{"messages": [{"role": "user", "content": "..."}]}`
- **Response in messages**: Access `result["messages"][-1].content`

## Additional Resources

- [LangChain Agent Concepts](https://docs.langchain.com/oss/python/langchain/concepts/agents)
- [create_agent API Reference](https://docs.langchain.com/oss/python/langchain/api/agents)
- [Agent Quickstart Tutorial](https://docs.langchain.com/oss/python/langchain/tutorials/agents)
