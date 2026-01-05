# Pair Exercise 01: Conversational Agent with Memory

## Overview

Work with your pair programming partner to build a conversational agent that remembers context across multiple conversation turns. This exercises uses the `InMemorySaver` checkpointer from LangGraph.

## Pair Programming Roles

- **Driver**: Writes the code, focuses on syntax and implementation
- **Navigator**: Reviews code, catches errors, thinks about edge cases

**Rotate roles every 25-30 minutes!**

## Learning Objectives

- Configure `InMemorySaver` for conversation memory
- Use `thread_id` functionality
- Build multi-turn conversations that maintain context
- Test memory persistence across invocations

## The Scenario

You're building a customer support agent for a software company. The agent needs to:
1. Remember the customer's name when they introduce themselves
2. Track the issue being discussed across multiple messages
3. Reference previous context when providing solutions

Without memory, the agent would "forget" everything between messages.

## Your Tasks

### Task 1: Basic Memory Setup (30 min)

**Driver**: Implement `create_memory_agent()` in the starter code:
- Create an agent using `create_agent()`
- Add `InMemorySaver` as the checkpointer
- Include a helpful system prompt

**Navigator**: Watch for:
- Is the `name` parameter included?
- Is the checkpointer properly configured?
- Does the system prompt mention memory/context?

> **Hint**: `from langgraph.checkpoint.memory import InMemorySaver`

### Task 2: Context Retention Test (25 min)

**Rotate roles!**

**Driver**: Implement `test_context_retention()`:
- Start a conversation with an introduction
- Follow up asking the agent to recall information
- Verify the agent remembers

**Navigator**: Think about:
- What happens if we use a different thread_id?
- How can we verify memory is working vs lucky guessing?

### Task 3: Multi-Turn Conversation (25 min)

**Rotate roles!**

**Driver**: Implement `run_multi_turn_conversation()`:
- Create a 4-5 message conversation
- Each message should build on previous context
- Track and display the full conversation history

**Navigator**: Consider:
- Is context being maintained correctly?
- Are there edge cases to test?

### Task 4: Memory Inspection (20 min)

**Rotate roles!**

**Driver**: Implement `inspect_memory_state()`:
- Access the agent's state/memory
- Display what the agent "remembers"
- Show the message history

**Navigator**: Review:
- How is state structured?
- What data is persisted?

## Definition of Done

- [_] Agent created with InMemorySaver checkpointer
- [_] Context retention test passes (agent remembers name)
- [_] Multi-turn conversation maintains context
- [_] Can inspect and display memory state
- [_] Both partners have driven at least once

## Testing Your Solution

```bash
cd exercises/4-Thursday/starter_code
python pair_exercise_01_starter.py
```

Expected output:
```
=== Memory Agent Test ===

[INFO] Creating agent with memory...
[OK] Agent 'support_agent' created with InMemorySaver

=== Context Retention Test ===
Thread: user_123

Turn 1:
  User: Hi, I'm Sarah and I'm having trouble with my subscription.
  Agent: Hello Sarah! I'd be happy to help with your subscription...

Turn 2:
  User: What's my name again?
  Agent: Your name is Sarah. Now, about your subscription issue...

[OK] Context retention working!

=== Multi-Turn Conversation ===
[Shows full 5-turn conversation with maintained context]

=== Memory Inspection ===
Thread ID: user_123
Message Count: 10
First User Message: Hi, I'm Sarah...
Last Agent Response: ...
```

## Key Patterns

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Memory agent setup
checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[...],
    checkpointer=checkpointer,
    system_prompt="You are a helpful assistant that remembers context.",
    name="memory_agent"
)

# Invoke with thread_id
config = {"configurable": {"thread_id": "unique_id"}}
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]}, config)
```

## Discussion Questions (for both partners)

1. What happens to memory when the Python process restarts?
2. How would you implement persistent memory across restarts?
3. When would you use `InMemorySaver` vs a database checkpointer?

## Stretch Goals (Optional)

1. Add a tool that references conversation history
2. Implement memory summarization for long conversations
3. Test with concurrent threads in a single session
