# Thread-Based Conversations

## Learning Objectives
- Understand how `thread_id` isolates conversation contexts
- Manage multiple concurrent conversations
- Create effective thread naming strategies
- Handle thread lifecycle (creation, continuation, cleanup)

## Why This Matters

In production, your agent serves many users simultaneously. Each user expects their own private conversation that doesn't leak into others. Thread-based conversations provide this isolation automatically—every user gets their own memory space.

## The Concept

### What is a Thread?

A thread is a unique identifier that groups related messages into a single conversation:

```
Thread: "user_alice_session_1"
├── User: "Hi, I'm Alice"
├── Agent: "Hello Alice!"
├── User: "What's my name?"
└── Agent: "Your name is Alice."

Thread: "user_bob_session_1"
├── User: "My name is Bob"
├── Agent: "Nice to meet you, Bob!"
├── User: "What's my name?"
└── Agent: "Your name is Bob."
```

Each thread maintains completely separate state.

### The `thread_id` Configuration

Thread IDs are passed in the config:

```python
config = {
    "configurable": {
        "thread_id": "unique_thread_identifier"
    }
}

result = agent.invoke({"messages": [...]}, config)
```

The checkpointer uses this ID to:
1. Load existing state (if thread exists)
2. Save updated state (after the turn)

### Thread Isolation

Threads are completely isolated:

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=checkpointer,
    name="isolated_agent"
)

# Alice's thread
alice_config = {"configurable": {"thread_id": "alice"}}
agent.invoke(
    {"messages": [{"role": "user", "content": "I love pizza!"}]},
    alice_config
)

# Bob's thread - completely separate
bob_config = {"configurable": {"thread_id": "bob"}}
agent.invoke(
    {"messages": [{"role": "user", "content": "I hate pizza!"}]},
    bob_config
)

# Alice's preferences are preserved in her thread
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What do I think about pizza?"}]},
    alice_config
)
# Agent responds about loving pizza (from Alice's history)
```

### Thread Naming Strategies

Choose thread IDs that are:
- **Unique**: No accidental collisions
- **Meaningful**: Debuggable and traceable
- **Consistent**: Same user = same thread

**Common patterns:**

```python
# User-based (persistent per user)
thread_id = f"user_{user_id}"

# Session-based (new session = new thread)
thread_id = f"user_{user_id}_session_{session_id}"

# Time-based (daily threads)
thread_id = f"user_{user_id}_{date.today()}"

# Topic-based (separate thread per topic)
thread_id = f"user_{user_id}_topic_{topic_name}"
```

### Managing Multiple Conversations

Typical patterns for multi-user scenarios:

```python
from fastapi import FastAPI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

app = FastAPI()
checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=checkpointer,
    name="multi_user_agent"
)

@app.post("/chat")
def chat(user_id: str, message: str):
    # Each user gets their own thread
    config = {"configurable": {"thread_id": f"user_{user_id}"}}
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": message}]
    }, config)
    
    return {"response": result["messages"][-1].content}
```

### Starting New Threads

To start a fresh conversation, simply use a new thread ID:

```python
# Continuing an existing conversation
config = {"configurable": {"thread_id": "alice"}}

# Starting fresh (new thread)
import uuid
new_config = {"configurable": {"thread_id": f"alice_{uuid.uuid4()}"}}
```

### Thread History Length

As conversations grow, threads accumulate messages:

```python
# After 10 turns, a thread might contain:
# - 1 system message
# - 10 user messages
# - 10 assistant messages
# - Maybe tool messages
# = 20+ messages

# This means:
# - More tokens per API call
# - Higher costs
# - Potential context window limits
```

**Management strategies:**
- New threads after X messages
- Message summarization (Week 6 topic)
- Sliding window (keep last N messages)

### Thread Lifecycle

```
Create Thread                Use Thread                    Cleanup
──────────────              ───────────                    ───────
First invocation     ───▶   Continue conversations    ▶   Delete old threads
with new ID                 Same ID = same state          (if needed)
```

### Inspecting Thread State

You can inspect what's stored in a thread:

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

# After some conversations...
config = {"configurable": {"thread_id": "alice"}}

# Get the current state
state = checkpointer.get(config)

# View messages
for msg in state.get("messages", []):
    print(f"{msg.get('role', 'unknown')}: {msg.get('content', '')[:50]}...")
```

### Thread ID Best Practices

| Practice | Why |
|----------|-----|
| Include user identifier | Ensures per-user isolation |
| Use consistent format | Easier debugging |
| Avoid PII in thread IDs | Security and privacy |
| Include timestamp or session | Enables conversation history |
| Log thread IDs | Enables support and debugging |

## Code Example

```python
"""
Thread-Based Conversations Demo
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import uuid
from datetime import datetime

# Shared checkpointer for all threads
checkpointer = InMemorySaver()

@tool
def get_user_context() -> str:
    """Get context about the current user's preferences."""
    return "Checking conversation history for context..."

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_user_context],
    checkpointer=checkpointer,
    system_prompt="""You are a helpful assistant that remembers user preferences.
    Reference previous messages to provide personalized responses.""",
    name="threaded_agent"
)

def create_thread_id(user_id: str, session_based: bool = False) -> str:
    """Create a thread ID for a user."""
    if session_based:
        # New thread for each session
        return f"user_{user_id}_session_{uuid.uuid4().hex[:8]}"
    else:
        # Persistent thread per user
        return f"user_{user_id}"

def chat(user_id: str, message: str, thread_id: str) -> str:
    """Send a message and get a response."""
    config = {"configurable": {"thread_id": thread_id}}
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": message}]
    }, config)
    
    return result["messages"][-1].content

# Simulate multiple users
print("=== Multi-User Thread Demo ===\n")

# User Alice - persistent thread
alice_thread = create_thread_id("alice")
print(f"Alice's thread: {alice_thread}")
print("Alice: I prefer morning meetings")
print(f"Agent: {chat('alice', 'I prefer morning meetings', alice_thread)}\n")

# User Bob - persistent thread
bob_thread = create_thread_id("bob")
print(f"Bob's thread: {bob_thread}")
print("Bob: I prefer afternoon meetings")
print(f"Agent: {chat('bob', 'I prefer afternoon meetings', bob_thread)}\n")

# Continue Alice's conversation
print("Alice (continued): When should we schedule a meeting?")
print(f"Agent: {chat('alice', 'When should we schedule a meeting?', alice_thread)}")
print("(Agent should reference Alice's morning preference)")
print()

# Continue Bob's conversation
print("Bob (continued): When should we schedule a meeting?")
print(f"Agent: {chat('bob', 'When should we schedule a meeting?', bob_thread)}")
print("(Agent should reference Bob's afternoon preference)")
print()

# Demonstrate session-based threads (fresh start)
print("=== New Session for Alice ===")
alice_new_session = create_thread_id("alice", session_based=True)
print(f"New thread: {alice_new_session}")
print("Alice: When should we schedule a meeting?")
print(f"Agent: {chat('alice', 'When should we schedule a meeting?', alice_new_session)}")
print("(Agent has no memory - it's a new session thread)")
```

## Key Takeaways

- **`thread_id` isolates conversations**: Each ID has separate memory
- **Same ID = continuous conversation**: Agent remembers across turns
- **Choose naming wisely**: Include user ID, optionally session/time
- **Threads grow over time**: Plan for message accumulation
- **New thread = fresh start**: Use new ID to reset memory
- **Log thread IDs**: Essential for debugging and support

## Additional Resources

- [LangGraph Thread Configuration](https://docs.langchain.com/oss/python/langraph/concepts/persistence)
- [Multi-User Agent Patterns](https://docs.langchain.com/oss/python/langchain/how-to/multi_user)
- [Session Management Best Practices](https://docs.langchain.com/oss/python/langraph/how-to/sessions)
