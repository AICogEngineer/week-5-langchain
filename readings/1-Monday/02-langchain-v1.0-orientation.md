# LangChain v1.0 Orientation

## Learning Objectives
- Understand the LangChain v1.0 architecture and design philosophy
- Identify the core components: models, tools, agents, and memory
- Recognize the "simplicity first" approach that guides v1.0 development
- Know when to use built-in helpers vs. manual implementations

## Why This Matters

LangChain v1.0 represents a significant shift in how we build AI applications. Gone are the days of complex chain compositions and verbose boilerplate. The new architecture embraces **simplicity first**—providing high-level helper functions that handle 90% of use cases while still allowing low-level access when needed.

For our **"From Basics to Production"** journey, mastering LangChain v1.0 means you can build production-ready agents in a fraction of the code you'd need with raw API calls or the now-deprecated v0.x patterns.

## The Concept

### The "Simplicity First" Philosophy

LangChain v1.0 was redesigned with one core principle: **simple things should be simple; complex things should be possible.**

This means:
- Creating an agent should take 4-5 lines of code, not 50
- You shouldn't need to understand LangGraph internals for basic agents
- Helper functions handle common patterns; low-level APIs exist for advanced needs

### Core Components

LangChain v1.0 has four fundamental building blocks:

```
┌─────────────────────────────────────────────────────────────┐
│                      LangChain v1.0                         │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│   Models    │    Tools    │   Agents    │     Memory        │
│             │             │             │                   │
│ Chat models │ @tool       │ create_     │ Checkpointers     │
│ LLM calls   │ decorator   │ agent()     │ State management  │
│ Embeddings  │ Retrieval   │ Workflows   │ Thread isolation  │
└─────────────┴─────────────┴─────────────┴───────────────────┘
```

#### 1. Models

Models are the AI "brains" that power your applications. LangChain provides a unified interface across providers:

```python
from langchain import init_chat_model

# Simple string format: "provider:model_name"
model = init_chat_model("openai:gpt-4o-mini")
model = init_chat_model("anthropic:claude-3-5-sonnet-20241022")
model = init_chat_model("bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0")
```

The `init_chat_model()` helper abstracts provider-specific setup, giving you a consistent interface.

#### 2. Tools

Tools are functions that agents can call to interact with the world. The `@tool` decorator makes any Python function agent-callable:

```python
from langchain_core.tools import tool

@tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together. Use for arithmetic operations."""
    return a + b
```

The docstring is **critical**—it tells the agent when and how to use the tool.

#### 3. Agents

Agents combine models with tools to create autonomous systems that can reason and take actions:

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[calculate_sum],
    system_prompt="You are a helpful math assistant.",
    name="math_agent"  # Always provide a name!
)
```

#### 4. Memory

Memory enables agents to maintain context across conversation turns:

```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=InMemorySaver(),  # Enables memory
    name="conversational_agent"
)
```

We'll explore memory in depth on Thursday.

### When to Use What

| Situation | Use This | Why |
|-----------|----------|-----|
| Simple chatbot | `create_agent()` | Built-in agent handles everything |
| Tool-calling agent | `create_agent()` + tools | Standard pattern, minimal code |
| Multi-step workflow | `create_agent()` + supervisor pattern | Use agents as tools |
| Custom routing logic | Manual LangGraph `StateGraph` | Need full control over flow |
| Complex state transformations | Manual LangGraph | Built-in agents don't support |

**Rule of Thumb**: Start with `create_agent()`. Only reach for manual LangGraph when you have a specific requirement that the helper can't satisfy.

### The LangChain Ecosystem

LangChain v1.0 is modular. Key packages include:

| Package | Purpose |
|---------|---------|
| `langchain` | Core agents, helpers (`create_agent`, `init_chat_model`) |
| `langchain-core` | Base abstractions (`@tool`, message types) |
| `langchain-openai` | OpenAI provider integration |
| `langchain-anthropic` | Anthropic provider integration |
| `langchain-aws` | AWS Bedrock integration |
| `langchain-community` | Community integrations (vector stores, loaders) |
| `langgraph` | Low-level workflow framework (used internally by agents) |

Install what you need:
```bash
pip install langchain langchain-openai langgraph
```

## Code Example

Here's a complete "Hello World" agent in LangChain v1.0:

```python
"""
LangChain v1.0 Hello World Agent
LangChain Version: v1.0+
Documentation: https://docs.langchain.com/oss/python/langchain
"""
from langchain.agents import create_agent
from langchain_core.tools import tool

# Define a simple tool
@tool
def get_greeting(name: str) -> str:
    """Generate a personalized greeting for a person."""
    return f"Hello, {name}! Welcome to LangChain v1.0!"

# Create the agent (just 4 lines!)
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_greeting],
    system_prompt="You are a friendly greeter. Use the greeting tool when users introduce themselves.",
    name="greeter_agent"
)

# Use the agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "Hi, I'm Alex!"}]
})

print(result["messages"][-1].content)
```

**Compare this to v0.x**: No prompt templates, no output parsers, no agent executors, no memory objects to wire together. Just create and invoke.

## Key Takeaways

- **Simplicity first**: LangChain v1.0 provides high-level helpers for common patterns
- **Four core components**: Models, Tools, Agents, Memory
- **`create_agent()` is the starting point**: Use it for 90% of agent needs
- **`@tool` decorator**: Makes any function agent-callable—docstrings matter!
- **Modular packages**: Install only what you need
- **LangGraph is optional**: Used internally by `create_agent()`; only use directly for advanced cases

## Additional Resources

- [LangChain v1.0 Documentation](https://docs.langchain.com/oss/python/langchain)
- [LangChain GitHub Repository](https://github.com/langchain-ai/langchain)
- [LangChain Agent Conceptual Guide](https://docs.langchain.com/oss/python/langchain/concepts/agents)
