# Thursday: Memory & State Management (Pair Programming)

## Exercise Schedule

| Exercise | Type | Duration | Prerequisites |
|----------|------|----------|---------------|
| Pair 01: Conversational Agent | Pair Programming | 90-120 min | Reading 01-03, Demo 01-02 |
| Pair 02: Multi-Thread Support | Pair Programming | 90-120 min | Reading 04-05, Demo 03 |

## Pair Programming Format

Today's exercises are designed for **pair programming**. Work in pairs with rotating roles:

### Roles
- **Driver**: Types the code, focuses on implementation details
- **Navigator**: Reviews code as written, thinks about strategy and edge cases

### Rotation Schedule
- Rotate every 25-30 minutes
- At each rotation:
  1. Driver pushes/saves current work
  2. Swap roles
  3. Navigator (now Driver) reviews before continuing

## Learning Objectives

By completing these exercises, you will:
- Implement conversation memory using `InMemorySaver` checkpointer
- Manage multiple conversation threads with `thread_id`
- Understand state vs store for different data persistence needs
- Build agents that maintain context across multiple turns

## Before You Begin

1. **Complete the readings** in `readings/4-Thursday/`
2. **Watch/run demos** in `demos/4-Thursday/code/`
3. **Find your pair**: Partner up for today's exercises
4. Ensure dependencies are installed:
   ```bash
   pip install langchain langgraph
   ```

## Exercises

### Pair Exercise 01: Conversational Agent (Pair Programming)
See [pair_exercise_01_conversational_agent.md](pair_exercise_01_conversational_agent.md)
Starter code: `starter_code/pair_exercise_01_starter.py`

Build an agent with memory that maintains context across conversation turns.

### Pair Exercise 02: Multi-Thread Support (Pair Programming)
See [pair_exercise_02_multi_thread_support.md](pair_exercise_02_multi_thread_support.md)
Starter code: `starter_code/pair_exercise_02_starter.py`

Extend your agent to handle multiple simultaneous conversations using thread IDs.

## Estimated Time
**Total: 3-4 hours** (with pair rotations)

## Key v1.0 Memory Patterns

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Create agent with memory
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[my_tool],
    checkpointer=InMemorySaver(),  # Enables memory!
    name="memory_agent"
)

# Invoke with thread_id for conversation continuity
config = {"configurable": {"thread_id": "user_123"}}

# First message
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Alice"}]},
    config
)

# Second message - agent remembers!
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config
)
# Agent responds: "Your name is Alice"
```

> **Important**: The same `thread_id` means the same conversation. Different `thread_id` values are isolated conversations.
