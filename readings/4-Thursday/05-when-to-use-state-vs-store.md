# When to Use State vs. Store

## Learning Objectives
- Clearly distinguish between state and store
- Identify appropriate use cases for each
- Make informed decisions about where to persist data
- Understand the tradeoffs of each approach

## Why This Matters

Both state and store provide memory, but they serve different purposes. Using the wrong one leads to:
- Lost data (state when you needed store)
- Unnecessary complexity (store when state was enough)
- Poor performance (overfetching from store)

Making the right choice is essential for efficient agent design.

## The Concept

### State vs. Store: Core Differences

| Aspect | State | Store |
|--------|-------|-------|
| **Scope** | Single thread/conversation | Cross-conversation, permanent |
| **Lifetime** | Until thread ends or is deleted | Forever (until explicitly deleted) |
| **Automatic?** | Yes, via checkpointer | Manual read/write in tools |
| **Content** | Messages + custom fields | Any key-value data |
| **Use case** | Conversation memory | User profiles, learned facts |

### Visualizing the Difference

```
State (Conversation-Scoped)           Store (Permanent)
─────────────────────────            ────────────────────
Thread: "alice_session_1"            Namespace: ["users", "alice"]
├── Message 1                        ├── preferences: {theme: "dark"}
├── Message 2                        ├── facts: ["likes pizza"]
├── Message 3                        └── history: ["order_123", ...]
└── (cleared when session ends)      (persists forever)

Thread: "alice_session_2"
├── Message 1 (fresh start!)
└── ...
```

### When to Use State

**Use state when data is:**
- Specific to the current conversation
- Temporary by nature
- Automatically managed (messages)

**Examples:**

```python
# State: Conversation context
"What we've discussed so far" → State (messages)
"User's current task in this session" → State (custom field)
"Shopping cart contents (for checkout flow)" → State
"Follow-up questions queue" → State
```

### When to Use Store

**Use store when data is:**
- Relevant across conversations
- Worth remembering permanently  
- Independent of conversation flow

**Examples:**

```python
# Store: Permanent knowledge
"User prefers dark mode" → Store
"User's timezone" → Store
"Past order history" → Store
"Learned facts: User is vegetarian" → Store
"User's name" → Store
```

### Decision Framework

Ask these questions:

1. **Will I need this in a future conversation?**
   - Yes → Store
   - No → State

2. **Is this part of the conversation flow?**
   - Yes → State (messages)
   - No → Consider custom state field or store

3. **Should this survive a "clear history" action?**
   - Yes → Store
   - No → State

4. **Is this user-specific or session-specific?**
   - User-specific → Store
   - Session-specific → State

### Practical Examples

**Scenario 1: Food preferences**
```
User: "I'm vegetarian"

Where to store? → STORE
Why? This is a permanent preference that should affect 
recommendations in all future conversations.
```

**Scenario 2: Current order**
```
User: "I want to order a pizza"
User: "Make it large"
User: "Add mushrooms"

Where to store? → STATE
Why? The order details are part of this conversation.
Once the order is placed, we'd store the order record elsewhere.
```

**Scenario 3: Conversation summary**
```
After 20 turns, summarize the conversation.

Where to store? → Depends!
- Session summary (for context) → State
- Long-term memory ("We discussed X last week") → Store
```

### Combining State and Store

Often you'll use both:

```python
from langchain_core.tools import tool
from langchain.tools import ToolRuntime
from langgraph.types import Command

@tool
def save_preference(category: str, value: str, runtime: ToolRuntime) -> Command:
    """Save a user preference permanently."""
    user_id = runtime.config.get("user_id", "default")
    
    # Read existing preferences from STORE
    prefs = runtime.store.get(
        namespace=["users", user_id],
        key="preferences"
    ) or {}
    
    # Update
    prefs[category] = value
    
    # Write back to STORE (permanent)
    runtime.store.put(
        namespace=["users", user_id],
        key="preferences",
        value=prefs
    )
    
    # Also note in STATE that we did this (for conversation context)
    return Command(
        update={"last_preference_updated": category},
        result=f"Saved your {category} preference: {value}"
    )
```

### State + Store Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   STATE (via Checkpointer)         STORE (via runtime.store)│
│   ─────────────────────────        ──────────────────────────│
│   • messages                       • user preferences        │
│   • session_status                 • learned facts           │
│   • current_task                   • interaction history     │
│   • temp_flags                     • user profile            │
│                                                              │
│   Automatic management             Manual tool operations    │
│   Thread-scoped                    Namespace-scoped          │
│   Temporary                        Permanent                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Common Patterns

**Pattern 1: Load preferences at start**
```python
# In system prompt or early in conversation
"User preferences (from store): {loaded_preferences}"
```

**Pattern 2: Learn and remember**
```python
# User mentions something important
"I'm allergic to peanuts"

# Tool extracts and saves to store
→ store.put(namespace=["users", user_id], key="allergies", value=["peanuts"])
```

**Pattern 3: Conversation context only**
```python
# User clarifies current task
"Actually, make that a large"

# Just update state/messages, no need for store
→ Already in message history, automatically handled
```

### Tradeoffs Summary

| Factor | State | Store |
|--------|-------|-------|
| **Setup** | Automatic | Requires tool code |
| **Performance** | Fast (in memory) | Depends on backend |
| **Persistence** | Until thread ends | Permanent |
| **Scope** | Narrow (thread) | Wide (cross-thread) |
| **Best for** | Conversation flow | User knowledge |

## Code Example

```python
"""
State vs Store Decision Demo
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

# Note: Full store implementation requires BaseStore setup
# This demo focuses on the conceptual distinction

checkpointer = InMemorySaver()

# Simulated store (in production, use LangGraph's Store)
user_store = {}

@tool
def remember_permanently(fact: str) -> str:
    """
    Save a fact permanently about the user (survives conversation reset).
    Use when user shares preferences, personal info, or important facts.
    """
    # This would use runtime.store in full implementation
    user_store.setdefault("facts", []).append(fact)
    return f"Remembered permanently: {fact}"

@tool
def get_permanent_memories() -> str:
    """Get all permanently remembered facts about the user."""
    facts = user_store.get("facts", [])
    if not facts:
        return "No permanent memories stored yet."
    return "Permanent memories: " + "; ".join(facts)

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[remember_permanently, get_permanent_memories],
    checkpointer=checkpointer,
    system_prompt="""You are an assistant with two types of memory:

1. CONVERSATION MEMORY (automatic): You remember what we discussed in THIS session.
   This is cleared when we start a new session.

2. PERMANENT MEMORY (via tools): For important facts the user wants you to always remember.
   - Use remember_permanently for: preferences, allergies, important dates, personal info
   - Use get_permanent_memories to recall stored facts

When users share important personal info, offer to remember it permanently.""",
    name="dual_memory_agent"
)

# Session 1
print("=== Session 1 ===\n")
config1 = {"configurable": {"thread_id": "session_1"}}

# State-based memory (automatic)
result = agent.invoke({
    "messages": [{"role": "user", "content": "Hi, I'm planning a trip to Japan next month."}]
}, config1)
print(f"User: Hi, I'm planning a trip to Japan next month.")
print(f"Agent: {result['messages'][-1].content}\n")

# Ask the agent to remember something permanently
result = agent.invoke({
    "messages": [{"role": "user", "content": "Please remember I'm vegetarian - that's important for my trip."}]
}, config1)
print(f"User: Please remember I'm vegetarian - that's important for my trip.")
print(f"Agent: {result['messages'][-1].content}\n")

# State still works within session
result = agent.invoke({
    "messages": [{"role": "user", "content": "What did I say I was planning?"}]
}, config1)
print(f"User: What did I say I was planning?")
print(f"Agent: {result['messages'][-1].content}")
print("(Agent knows from STATE - conversation history)")
print()

# Session 2 - Fresh start, but permanent memory persists
print("=== Session 2 (New Conversation) ===\n")
config2 = {"configurable": {"thread_id": "session_2"}}

result = agent.invoke({
    "messages": [{"role": "user", "content": "Can you recommend a restaurant?"}]
}, config2)
print(f"User: Can you recommend a restaurant?")
print(f"Agent: {result['messages'][-1].content}\n")

# Check permanent memory
result = agent.invoke({
    "messages": [{"role": "user", "content": "Do you remember any dietary restrictions I have?"}]
}, config2)
print(f"User: Do you remember any dietary restrictions I have?")
print(f"Agent: {result['messages'][-1].content}")
print("(Agent knows from STORE - permanent memory)")
```

## Key Takeaways

- **State = session memory**: Automatic, temporary, conversation-scoped
- **Store = permanent memory**: Manual, persistent, cross-conversation
- **Use state for**: Messages, session context, temporary flags
- **Use store for**: Preferences, learned facts, user profiles
- **Ask**: "Will I need this next session?" → If yes, use store
- **Combine them**: State for flow, store for permanent knowledge

## Additional Resources

- [LangGraph State and Store](https://docs.langchain.com/oss/python/langraph/concepts/state)
- [Memory Persistence Patterns](https://docs.langchain.com/oss/python/langchain/how-to/memory)
- [Cross-Conversation Memory](https://docs.langchain.com/oss/python/langraph/how-to/memory)
