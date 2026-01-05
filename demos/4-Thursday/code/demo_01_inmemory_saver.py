"""
Demo 01: InMemorySaver - Adding Memory to Agents

This demo shows trainees how to:
1. Understand why agents are stateless by default
2. Add memory using InMemorySaver checkpointer
3. Configure thread_id for conversation continuity
4. See memory persistence across multiple turns

Learning Objectives:
- Implement InMemorySaver from langgraph.checkpoint.memory
- Understand the checkpointer pattern
- Use thread_id for conversation management

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/short-term-memory
Last Verified: January 2026

References:
- Written Content: readings/4-Thursday/02-checkpointers-inmemory-saver.md

CRITICAL v1.0 PATTERNS:
- Use InMemorySaver from langgraph.checkpoint.memory
- NOT ConversationBufferMemory (deprecated)
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# PART 1: Agent Without Memory (The Problem)
# ============================================================================

print("=" * 70)
print("PART 1: Agent WITHOUT Memory")
print("=" * 70)

print("""
By default, agents are STATELESS.
Each invocation is independent - no memory of previous turns.
""")

# Create agent WITHOUT memory
agent_no_memory = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt="You are a friendly assistant. Remember important details about the user.",
    name="forgetful_agent"
)

print("\n[Step 1] Testing agent without memory...")

# First message
print("\n  Turn 1:")
result1 = agent_no_memory.invoke({
    "messages": [{"role": "user", "content": "Hi! My name is Alice and I love programming."}]
})
print(f"    User: Hi! My name is Alice and I love programming.")
print(f"    Agent: {result1['messages'][-1].content}")

# Second message - agent forgets!
print("\n  Turn 2:")
result2 = agent_no_memory.invoke({
    "messages": [{"role": "user", "content": "What's my name and what do I love?"}]
})
print(f"    User: What's my name and what do I love?")
print(f"    Agent: {result2['messages'][-1].content}")

print("\n  ❌ The agent forgot! It doesn't remember the previous turn.")

# ============================================================================
# PART 2: Agent WITH Memory (The Solution)
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Agent WITH Memory (InMemorySaver)")
print("=" * 70)

print("""
InMemorySaver is the v1.0 checkpointer for development.
It stores conversation state in memory.

Key pattern:
  from langgraph.checkpoint.memory import InMemorySaver
  
  agent = create_agent(
      model="...",
      tools=[...],
      checkpointer=InMemorySaver(),  # <-- Add this!
      name="my_agent"
  )
""")

# Create agent WITH memory
agent_with_memory = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt="You are a friendly assistant. Remember important details about the user.",
    checkpointer=InMemorySaver(),  # THIS IS THE KEY!
    name="memory_agent"
)

print("\n[Step 2] Testing agent WITH memory...")

# Define thread config
config = {"configurable": {"thread_id": "user_alice_123"}}

# First message
print("\n  Turn 1:")
result1 = agent_with_memory.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Alice and I love programming."}]},
    config  # Pass the config!
)
print(f"    User: Hi! My name is Alice and I love programming.")
print(f"    Agent: {result1['messages'][-1].content}")

# Second message - agent remembers!
print("\n  Turn 2:")
result2 = agent_with_memory.invoke(
    {"messages": [{"role": "user", "content": "What's my name and what do I love?"}]},
    config  # Same config = same conversation
)
print(f"    User: What's my name and what do I love?")
print(f"    Agent: {result2['messages'][-1].content}")

print("\n  ✓ The agent remembers! Memory works!")

# ============================================================================
# PART 3: How Config and Thread ID Work
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Understanding thread_id")
print("=" * 70)

print("""
The thread_id is like a conversation ID.
- Same thread_id = same conversation = shared memory
- Different thread_id = different conversation = separate memory

Config structure:
  config = {"configurable": {"thread_id": "unique_string"}}
""")

# Continue the Alice conversation
print("\n[Step 3] Continuing Alice's conversation...")
result3 = agent_with_memory.invoke(
    {"messages": [{"role": "user", "content": "Can you summarize what you know about me?"}]},
    config
)
print(f"  User: Can you summarize what you know about me?")
print(f"  Agent: {result3['messages'][-1].content}")

# ============================================================================
# PART 4: Multi-Turn Conversation
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Extended Multi-Turn Conversation")
print("=" * 70)

# Start a new conversation
fresh_config = {"configurable": {"thread_id": "user_bob_456"}}

@tool
def get_weather(city: str) -> str:
    """Get weather for a city. Use when asked about weather."""
    weather = {
        "austin": "Sunny, 85°F",
        "seattle": "Rainy, 55°F",
        "new york": "Cloudy, 68°F"
    }
    return weather.get(city.lower(), f"Weather for {city}: Partly cloudy, 70°F")

memory_tool_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
    system_prompt="""You are a travel assistant. 
    Remember user preferences and destinations they mention.
    Use the weather tool when asked about weather.""",
    checkpointer=InMemorySaver(),
    name="travel_assistant"
)

print("\n[Step 4] Multi-turn travel assistant conversation...")

turns = [
    "I'm planning a trip from Austin to Seattle next week.",
    "What's the weather like in my destination?",
    "And what about where I'm leaving from?",
    "What was my original travel plan again?"
]

for i, message in enumerate(turns, 1):
    print(f"\n  Turn {i}:")
    print(f"    User: {message}")
    result = memory_tool_agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        fresh_config
    )
    response = result['messages'][-1].content
    print(f"    Agent: {response[:200]}{'...' if len(response) > 200 else ''}")

# ============================================================================
# PART 5: Deprecated Patterns to Avoid
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Deprecated Patterns to AVOID")
print("=" * 70)

print("""
❌ WRONG - ConversationBufferMemory (deprecated in v1.0):
   from langchain.memory import ConversationBufferMemory
   memory = ConversationBufferMemory()

❌ WRONG - RunnableWithMessageHistory (deprecated):
   from langchain_core.runnables.history import RunnableWithMessageHistory

✅ CORRECT - InMemorySaver for development:
   from langgraph.checkpoint.memory import InMemorySaver
   agent = create_agent(..., checkpointer=InMemorySaver(), ...)

✅ CORRECT - Production checkpointers:
   from langgraph.checkpoint.postgres import PostgresSaver
   from langgraph.checkpoint.redis import RedisSaver
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: InMemorySaver")
print("=" * 70)

print("""
Key Takeaways:

1. Agents are stateless by default - they forget between turns
2. InMemorySaver from langgraph.checkpoint.memory adds memory
3. Always pass config with thread_id for conversation continuity
4. Same thread_id = same conversation = shared memory
5. For production, use PostgresSaver or similar persistent store
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The dramatic difference between with/without memory
2. How thread_id isolates conversations
3. Memory persists even with tool calls

Live Demo Tips:
- Run both agents side by side if possible
- Ask trainees to predict what happens before running
- Show that clearing the script resets InMemorySaver

Discussion Questions:
- "Why is InMemorySaver not good for production?"
- "What happens if your app restarts with InMemorySaver?"
- "How would you implement user sessions in a web app?"

Common Mistakes:
- Forgetting to pass config with thread_id
- Using deprecated ConversationBufferMemory
- Not understanding thread isolation
""")

print("=" * 70)
