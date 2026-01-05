# Agent Naming Best Practices

## Learning Objectives
- Understand why agent names are required in LangChain v1.0
- Follow naming conventions for clarity and consistency
- Use descriptive names that aid debugging and tracing
- Apply naming strategies for multi-agent systems

## Why This Matters

The `name` parameter in `create_agent()` is not optional—it's required. But beyond being a syntax requirement, good naming is crucial for:
- Debugging when things go wrong
- Tracing agent execution in LangSmith
- Distinguishing agents in multi-agent systems
- Maintaining readable, maintainable code

In production systems, you'll thank yourself for using clear, descriptive names.

## The Concept

### Why Names Are Required

In LangChain v1.0, every agent must have a name:

```python
# ❌ This will fail - no name provided
agent = create_agent(model="openai:gpt-4o-mini", tools=[])

# ✅ This works
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    name="my_agent"  # Required!
)
```

**Why the requirement?**
1. **LangSmith Tracing**: Names appear in traces, making execution visible
2. **Multi-Agent Systems**: Identify which agent performed which action
3. **Logging**: Meaningful log messages with agent context
4. **Debugging**: Quickly find the agent responsible for an error

### Naming Conventions

Follow these conventions for consistent, readable names:

#### Format: snake_case
```python
# ✅ Good - snake_case
name="weather_agent"
name="customer_service_bot"
name="document_search_agent"

# ❌ Avoid - other cases
name="WeatherAgent"        # PascalCase
name="weather-agent"       # kebab-case
name="WEATHER_AGENT"       # SCREAMING_CASE
```

#### Pattern: `[domain]_[role]`
```python
# Domain-first pattern
name="finance_analyst"
name="hr_assistant"
name="inventory_manager"

# Role-first pattern (also acceptable)
name="search_agent"
name="qa_bot"
name="support_agent"
```

### Descriptive vs. Generic Names

```python
# ❌ Too generic - doesn't tell you what it does
name="agent"
name="bot"
name="my_agent"
name="test_agent"

# ✅ Descriptive - purpose is clear
name="product_recommendation_agent"
name="order_status_checker"
name="technical_support_assistant"
name="meeting_scheduler_bot"
```

### Names in LangSmith

When you view traces in LangSmith, agent names appear in the execution graph:

```
Run: "product_recommendation_agent"
├── ChatOpenAI
├── ToolCall: search_products
│   └── search_products executed
├── ChatOpenAI
└── Response: "Based on your preferences..."
```

Good names make traces immediately understandable. Bad names require hunting through logs.

### Multi-Agent System Naming

When building systems with multiple agents, names become critical:

```python
# Supervisor pattern example
supervisor = create_agent(
    model="openai:gpt-4o-mini",
    tools=[research_tool, writer_tool, reviewer_tool],
    name="content_supervisor"  # Orchestrator name
)

research_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_web, search_academic],
    name="research_assistant"  # Sub-agent with clear role
)

writer_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    name="content_writer"  # Another sub-agent
)

reviewer_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[check_grammar, check_facts],
    name="content_reviewer"  # Yet another sub-agent
)
```

In traces, you'll see clearly which agent did what:
```
content_supervisor → research_assistant → web_search
content_supervisor → content_writer → (no tools)
content_supervisor → content_reviewer → check_facts
```

### Naming for Different Environments

Consider environment-specific naming for debugging:

```python
import os

env = os.getenv("ENVIRONMENT", "dev")

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[...],
    name=f"support_agent_{env}"  # "support_agent_dev" or "support_agent_prod"
)
```

This helps when reviewing logs across environments.

### Common Naming Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| `{function}_agent` | `search_agent` | Single-purpose agents |
| `{domain}_assistant` | `finance_assistant` | Domain specialists |
| `{task}_bot` | `scheduler_bot` | Task-specific bots |
| `{team}_{role}` | `sales_researcher` | Multi-agent teams |
| `{product}_{function}` | `acme_support` | Product-specific agents |

### What Names to Avoid

```python
# ❌ Avoid these patterns

# Too generic
name="agent1"
name="test"
name="main"

# Too long (hard to read in traces)
name="the_agent_that_handles_customer_service_inquiries_for_premium_users"

# Special characters (may cause issues)
name="agent@v2"
name="agent.backup"
name="agent#1"

# Confusing abbreviations
name="csa"  # Customer service agent? Content search? 
name="pra1"  # What does this mean?
```

### Best Practices Summary

| Do | Don't |
|-----|-------|
| Use snake_case | Use other case styles |
| Be descriptive | Use generic names |
| Keep it readable | Make names too long |
| Indicate purpose | Use abbreviations |
| Be consistent | Mix naming patterns |
| Version if needed (`v2`) | Use special characters |

## Code Example

```python
"""
Agent Naming Best Practices Demo
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool

# Example 1: Well-named single-purpose agent
@tool
def check_order_status(order_id: str) -> str:
    """Check the status of an order."""
    return f"Order {order_id} is being shipped."

order_tracker = create_agent(
    model="openai:gpt-4o-mini",
    tools=[check_order_status],
    system_prompt="You help customers track their orders.",
    name="order_tracking_agent"  # Clear purpose
)

# Example 2: Named agents in a team scenario
@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base."""
    return "Found relevant information..."

@tool
def draft_response(content: str) -> str:
    """Draft a customer response."""
    return f"Draft: {content}"

# Research team member
researcher = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_knowledge_base],
    name="support_researcher"  # Role on team
)

# Response team member  
responder = create_agent(
    model="openai:gpt-4o-mini",
    tools=[draft_response],
    name="support_responder"  # Different role
)

# Example 3: Environment-aware naming
import os

env = os.getenv("DEPLOY_ENV", "development")
version = "v2"

production_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    name=f"billing_assistant_{version}_{env}"
    # Result: "billing_assistant_v2_development"
)

# Example 4: Demonstrating trace visibility
# When you run this agent, LangSmith will show:
# "order_tracking_agent" → ToolCall: check_order_status → Response

result = order_tracker.invoke({
    "messages": [{"role": "user", "content": "Where is order ORD-12345?"}]
})
print(f"Agent response: {result['messages'][-1].content}")

# In the LangSmith trace, you'll clearly see:
# ┌─ order_tracking_agent ─────────────────┐
# │  ├─ ChatOpenAI                         │
# │  ├─ check_order_status("ORD-12345")    │
# │  └─ Final Response                     │
# └────────────────────────────────────────┘
```

## Key Takeaways

- **Names are required**: LangChain v1.0 mandates the `name` parameter
- **Use snake_case**: Consistent, readable convention
- **Be descriptive**: Names should indicate purpose at a glance
- **Avoid generic names**: "agent" tells you nothing
- **Multi-agent clarity**: Good names make complex systems debuggable
- **LangSmith visibility**: Names appear in traces—make them useful

## Additional Resources

- [LangChain Agent Configuration](https://docs.langchain.com/oss/python/langchain/concepts/agents)
- [LangSmith Tracing Guide](https://docs.smith.langchain.com/tracing)
- [Python Naming Conventions (PEP 8)](https://peps.python.org/pep-0008/#naming-conventions)
