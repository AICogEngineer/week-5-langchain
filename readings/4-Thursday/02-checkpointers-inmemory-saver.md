# Checkpointers: `InMemorySaver`

## Learning Objectives
- Understand what checkpointers are and why they're needed
- Use `InMemorySaver` for development and testing
- Know when to use different checkpointer types
- Configure checkpointers correctly

## Why This Matters

Checkpointers are the mechanism that enables agent memory. Without a checkpointer, every agent invocation is independent—the agent has no recollection of previous turns. With a checkpointer, you get multi-turn conversations that feel natural.

`InMemorySaver` is your development workhorse—fast, simple, and requiring no external dependencies.

## The Concept

### What is a Checkpointer?

A checkpointer is a storage backend for agent state. After each turn, the checkpointer:
1. **Saves** the current state (messages, custom fields)
2. **Loads** the state on the next turn (using `thread_id`)

```
Turn 1                      Turn 2
┌─────────┐                ┌─────────┐
│ Invoke  │                │ Invoke  │
│ Agent   │                │ Agent   │
│         │                │         │
│ State   │──save──▶ [Checkpointer] ──load──▶│ State   │
│ updated │                │ loaded  │
└─────────┘                └─────────┘
```

### `InMemorySaver`

The simplest checkpointer stores state in RAM:

```python
from langgraph.checkpoint.memory import InMemorySaver

# Create the checkpointer
checkpointer = InMemorySaver()

# Use with create_agent
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=checkpointer,  # Enable memory
    name="memory_agent"
)
```

**Characteristics:**
- ✅ No setup required
- ✅ Fast (RAM access)
- ✅ Perfect for development/testing
- ❌ Data lost on restart
- ❌ Not suitable for production

### Thread-Based Storage

Checkpointers store state by `thread_id`:

```python
# Each thread has independent state
config_alice = {"configurable": {"thread_id": "alice_conversation"}}
config_bob = {"configurable": {"thread_id": "bob_conversation"}}

# Alice's conversation
agent.invoke({"messages": [...]}, config_alice)

# Bob's conversation (separate state)
agent.invoke({"messages": [...]}, config_bob)
```

Internally, the checkpointer maintains a structure like:

```
InMemorySaver
├── "alice_conversation" → [state snapshot 1, snapshot 2, ...]
├── "bob_conversation" → [state snapshot 1, snapshot 2, ...]
└── "session_xyz" → [state snapshot 1, ...]
```

### Basic Usage Pattern

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# 1. Create checkpointer
checkpointer = InMemorySaver()

# 2. Create agent with checkpointer
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=checkpointer,
    system_prompt="You remember our conversation.",
    name="example_agent"
)

# 3. Create config with thread_id
config = {"configurable": {"thread_id": "session_001"}}

# 4. Invoke with config
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hello!"}]},
    config
)

# 5. Subsequent calls share state
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember what I said?"}]},
    config  # Same config = same thread = shared memory
)
```

### Development vs. Production Checkpointers

| Use Case | Checkpointer | Install |
|----------|--------------|---------|
| Development/Testing | `InMemorySaver` | Built-in |
| Local persistence | `SqliteSaver` | `pip install langgraph-checkpoint-sqlite` |
| Production | `PostgresSaver` | `pip install langgraph-checkpoint-postgres` |
| Serverless | `DynamoDBSaver` | AWS SDK |

### When Data is Lost

`InMemorySaver` is volatile:

```python
# Session 1
checkpointer = InMemorySaver()
agent = create_agent(..., checkpointer=checkpointer, name="agent")
agent.invoke(...)  # State saved in RAM

# If your script/server restarts...
# Session 2
checkpointer = InMemorySaver()  # NEW instance!
agent = create_agent(..., checkpointer=checkpointer, name="agent")
# All previous state is gone!
```

For persistence across restarts, use `SqliteSaver` or production databases.

### SqliteSaver for Persistence

Quick upgrade to persistent storage:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Creates/uses a local SQLite file
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=checkpointer,
    name="persistent_agent"
)

# State now survives restarts!
```

### Multiple Agents, Same Checkpointer

You can share a checkpointer across agents:

```python
checkpointer = InMemorySaver()

agent_a = create_agent(
    model="openai:gpt-4o-mini", tools=[], 
    checkpointer=checkpointer, name="agent_a"
)

agent_b = create_agent(
    model="openai:gpt-4o-mini", tools=[], 
    checkpointer=checkpointer, name="agent_b"
)

# Both agents use the same storage backend
# But different thread_ids keep them separate
```

### State Snapshots and History

Checkpointers keep snapshots at each turn:

```python
# Turn 1: State snapshot 1
# Turn 2: State snapshot 2
# Turn 3: State snapshot 3

# This enables future features like:
# - Reverting to previous states
# - Branching conversations
# - Debugging by replaying state
```

### Error Handling

Checkpointer operations can fail (especially for databases):

```python
from langgraph.errors import CheckpointerError

try:
    result = agent.invoke({"messages": [...]}, config)
except CheckpointerError as e:
    print(f"Memory error: {e}")
    # Handle gracefully - maybe retry or fall back
```

## Code Example

```python
"""
Using InMemorySaver for Agent Memory
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

# Create the checkpointer
checkpointer = InMemorySaver()

@tool
def set_reminder(task: str, time: str) -> str:
    """Set a reminder for a task at a specific time."""
    return f"Reminder set: '{task}' at {time}"

@tool
def list_reminders() -> str:
    """List all reminders set in this session."""
    # In real app, would read from state
    return "Checking conversation for reminders..."

# Create agent with memory
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[set_reminder, list_reminders],
    checkpointer=checkpointer,
    system_prompt="""You are a personal assistant with memory.
    Track reminders and context from the conversation.
    When listing reminders, look back through the conversation.""",
    name="reminder_agent"
)

# Demonstrate multi-turn memory
config = {"configurable": {"thread_id": "user_session_today"}}

print("=== Conversation with Memory ===\n")

# Turn 1
print("User: Set a reminder to buy groceries at 5pm")
result = agent.invoke({
    "messages": [{"role": "user", "content": "Set a reminder to buy groceries at 5pm"}]
}, config)
print(f"Agent: {result['messages'][-1].content}\n")

# Turn 2
print("User: Also remind me to call mom at 7pm")
result = agent.invoke({
    "messages": [{"role": "user", "content": "Also remind me to call mom at 7pm"}]
}, config)
print(f"Agent: {result['messages'][-1].content}\n")

# Turn 3 - Agent should remember both reminders
print("User: What reminders have I set?")
result = agent.invoke({
    "messages": [{"role": "user", "content": "What reminders have I set?"}]
}, config)
print(f"Agent: {result['messages'][-1].content}\n")

# Show that different thread has no memory
different_config = {"configurable": {"thread_id": "different_session"}}
print("=== Different Session ===")
print("User: What reminders have I set?")
result = agent.invoke({
    "messages": [{"role": "user", "content": "What reminders have I set?"}]
}, different_config)
print(f"Agent: {result['messages'][-1].content}")
print("(Different session has no memory of previous reminders)")
```

## Key Takeaways

- **Checkpointers enable memory**: Without one, agents forget between turns
- **`InMemorySaver` is for development**: Fast, no setup, but non-persistent
- **Thread-based isolation**: Each `thread_id` has independent memory
- **State is saved automatically**: After each turn, before next load
- **Upgrade for production**: Use `SqliteSaver` or database-backed options
- **Share across agents**: One checkpointer can serve multiple agents

## Additional Resources

- [LangGraph Checkpointers](https://docs.langchain.com/oss/python/langraph/concepts/persistence)
- [InMemorySaver API](https://docs.langchain.com/oss/python/langraph/api/checkpoint)
- [Production Persistence Options](https://docs.langchain.com/oss/python/langraph/how-to/persistence)
