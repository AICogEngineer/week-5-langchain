# Short-Term Memory (State)

## Learning Objectives
- Understand what agent state is and how it works
- Distinguish between state (session-scoped) and store (persistent)
- Identify what data is stored in state
- Access and work with state in agents

## Why This Matters

Without memory, every agent invocation is isolated—the agent has no idea what you discussed 10 seconds ago. State enables continuity: multi-turn conversations, context accumulation, and incremental task completion.

For our **"From Basics to Production"** journey, understanding state is essential for building agents that feel intelligent and aware.

## The Concept

### What is State?

State is the **session-scoped memory** that persists across turns within a single conversation. It holds:

- **Messages**: The conversation history (user, assistant, tool messages)
- **Custom data**: Any additional fields you define
- **Thread context**: Scoped to a specific `thread_id`

```
Conversation Thread: user_123
┌─────────────────────────────────────────────────┐
│ State                                           │
│ ├── messages: [msg1, msg2, msg3, ...]          │
│ └── custom_fields: {...}                        │
└─────────────────────────────────────────────────┘
         ↓ persists across ↓
    Turn 1 → Turn 2 → Turn 3 → ...
```

### State vs. Store

LangChain v1.0 distinguishes between two types of memory:

| Aspect | State | Store |
|--------|-------|-------|
| **Scope** | Single conversation (thread) | Cross-conversation |
| **Lifetime** | Until thread ends | Permanent |
| **Use case** | Message history, session data | User preferences, memories |
| **Access** | Automatic via checkpointer | Via `runtime.store` |

**State** = "Remember what we talked about this session"
**Store** = "Remember what we learned about this user forever"

We'll cover `store` in detail in Friday's reading on when to use each.

### How State Works

When you create an agent with a checkpointer, state is automatically managed:

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=InMemorySaver(),  # Enables state
    name="stateful_agent"
)
```

Each invocation with the same `thread_id` shares state:

```python
config = {"configurable": {"thread_id": "session_123"}}

# Turn 1
result = agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Alice."}]},
    config
)

# Turn 2 - agent remembers!
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config
)
# Agent responds: "Your name is Alice."
```

### What's Stored in State

By default, state contains:

```python
{
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "My name is Alice."},
        {"role": "assistant", "content": "Nice to meet you, Alice!"},
        {"role": "user", "content": "What's my name?"},
        {"role": "assistant", "content": "Your name is Alice."}
    ]
}
```

Each turn adds messages to the list. The full history is passed to the LLM on every turn.

### Session Scoping

State is isolated by `thread_id`:

```python
# User A's conversation
config_a = {"configurable": {"thread_id": "user_a_session"}}

# User B's conversation (completely separate)
config_b = {"configurable": {"thread_id": "user_b_session"}}

# These don't share any state
agent.invoke({"messages": [...]}, config_a)  # Only sees A's history
agent.invoke({"messages": [...]}, config_b)  # Only sees B's history
```

### State Grows Over Time

Important consideration: state accumulates messages, which means more tokens:

```
Turn 1:  System (50) + User (20) + Assistant (30) = 100 tokens
Turn 5:  System (50) + [9 messages, 500 tokens] = 550 tokens
Turn 10: System (50) + [19 messages, 1200 tokens] = 1250 tokens
Turn 20: System (50) + [39 messages, ~3000 tokens] = 3050 tokens
```

Strategies to manage this:
- **Message trimming**: Keep only last N messages
- **Summarization**: Replace old messages with summary (covered Week 6)
- **Session limits**: Start new threads after X turns

### Temporary State vs. Persisted State

| Checkpointer | Data Location | Survives Restart? |
|--------------|---------------|-------------------|
| `InMemorySaver()` | RAM | No |
| `SqliteSaver()` | SQLite file | Yes |
| `PostgresSaver()` | PostgreSQL | Yes |

For development, `InMemorySaver()` is fine. For production, use a database-backed saver.

### Accessing State Manually

While state is usually managed automatically, you can inspect it:

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=checkpointer,
    name="inspectable_agent"
)

config = {"configurable": {"thread_id": "test_thread"}}

# Run agent
agent.invoke({"messages": [{"role": "user", "content": "Hello!"}]}, config)

# Inspect the state
state = checkpointer.get(config)
print(state)  # Shows full state including messages
```

## Code Example

```python
"""
Understanding Short-Term Memory (State)
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

# Create a checkpointer for state management
checkpointer = InMemorySaver()

@tool
def remember_preference(category: str, preference: str) -> str:
    """Remember a user preference for this session."""
    return f"Noted: Your {category} preference is {preference}"

# Create stateful agent
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[remember_preference],
    checkpointer=checkpointer,
    system_prompt="""You are a helpful assistant with memory.
    You remember what users tell you during the conversation.
    Reference previous messages when relevant.""",
    name="memory_demo_agent"
)

# Same thread = shared state
config = {"configurable": {"thread_id": "demo_session_001"}}

print("=== Multi-turn Conversation Demo ===\n")

# Turn 1: User shares information
print("Turn 1:")
result = agent.invoke({
    "messages": [{"role": "user", "content": "Hi! My name is Bob and I prefer dark mode."}]
}, config)
print(f"User: Hi! My name is Bob and I prefer dark mode.")
print(f"Agent: {result['messages'][-1].content}\n")

# Turn 2: User asks a question
print("Turn 2:")
result = agent.invoke({
    "messages": [{"role": "user", "content": "What display mode do I prefer?"}]
}, config)
print(f"User: What display mode do I prefer?")
print(f"Agent: {result['messages'][-1].content}\n")

# Turn 3: Reference earlier information
print("Turn 3:")
result = agent.invoke({
    "messages": [{"role": "user", "content": "Can you remind me what my name is?"}]
}, config)
print(f"User: Can you remind me what my name is?")
print(f"Agent: {result['messages'][-1].content}\n")

# Different thread = separate state
different_config = {"configurable": {"thread_id": "different_session"}}

print("=== Different Session (No Memory) ===\n")
result = agent.invoke({
    "messages": [{"role": "user", "content": "What's my name?"}]
}, different_config)
print(f"User: What's my name?")
print(f"Agent: {result['messages'][-1].content}")
print("(Agent doesn't know - different session!)")
```

## Key Takeaways

- **State is session-scoped memory**: Persists within a conversation (thread)
- **Enabled by checkpointers**: Use `InMemorySaver` for development
- **Contains messages**: Full conversation history by default
- **Thread-isolated**: Each `thread_id` has separate state
- **Grows over time**: More turns = more tokens (plan for this)
- **Different from store**: State is session-based, store is permanent

## Additional Resources

- [LangGraph State Concepts](https://docs.langchain.com/oss/python/langraph/concepts/state)
- [Checkpointers Documentation](https://docs.langchain.com/oss/python/langraph/concepts/persistence)
- [Memory in Agents](https://docs.langchain.com/oss/python/langchain/how-to/memory)
