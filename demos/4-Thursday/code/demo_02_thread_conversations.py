"""
Demo 02: Thread-Based Conversations

This demo shows trainees how to:
1. Manage multiple simultaneous conversations
2. Isolate context between different threads
3. Switch between conversation threads
4. Implement user session patterns

Learning Objectives:
- Use thread_id to separate conversations
- Understand context isolation
- Design multi-user agent systems

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/short-term-memory
Last Verified: January 2026

References:
- Written Content: readings/4-Thursday/03-thread-based-conversations.md
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# PART 1: Two Separate Conversations
# ============================================================================

print("=" * 70)
print("PART 1: Two Separate Conversations")
print("=" * 70)

print("""
Different thread_ids create completely isolated conversations.
What happens in Thread A stays in Thread A.
""")

# Create agent with memory
support_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    system_prompt="""You are a customer support agent.
    Remember the customer's name and issue throughout the conversation.""",
    checkpointer=InMemorySaver(),
    name="support_agent"
)

# Define two separate threads (simulating two users)
thread_alice = {"configurable": {"thread_id": "user_alice_session"}}
thread_bob = {"configurable": {"thread_id": "user_bob_session"}}

print("\n[Step 1] Alice starts a conversation...")

result_a1 = support_agent.invoke(
    {"messages": [{"role": "user", "content": "Hi, I'm Alice. I have a billing question about my account."}]},
    thread_alice
)
print(f"  [Alice] User: Hi, I'm Alice. I have a billing question.")
print(f"  [Alice] Agent: {result_a1['messages'][-1].content}")

print("\n[Step 2] Bob starts a separate conversation...")

result_b1 = support_agent.invoke(
    {"messages": [{"role": "user", "content": "Hello, my name is Bob. I need help with a return."}]},
    thread_bob
)
print(f"  [Bob] User: Hello, my name is Bob. I need help with a return.")
print(f"  [Bob] Agent: {result_b1['messages'][-1].content}")

print("\n[Step 3] Alice continues her conversation...")

result_a2 = support_agent.invoke(
    {"messages": [{"role": "user", "content": "What was my issue again?"}]},
    thread_alice
)
print(f"  [Alice] User: What was my issue again?")
print(f"  [Alice] Agent: {result_a2['messages'][-1].content}")

print("\n[Step 4] Bob continues his conversation...")

result_b2 = support_agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name and what did I need help with?"}]},
    thread_bob
)
print(f"  [Bob] User: What's my name and what did I need help with?")
print(f"  [Bob] Agent: {result_b2['messages'][-1].content}")

print("\n✓ Conversations are completely isolated!")

# ============================================================================
# PART 2: Simulating a Multi-User Chat System
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Multi-User Chat System Pattern")
print("=" * 70)

print("""
In a real application, you'd generate thread_ids based on:
- User ID + Session ID
- Conversation UUID
- User ID + Topic/Channel

Pattern: thread_id = f"user_{user_id}_session_{session_id}"
""")

def create_thread_id(user_id: str, session_id: str = "default") -> dict:
    """Generate a config with unique thread_id."""
    thread_id = f"user_{user_id}_session_{session_id}"
    return {"configurable": {"thread_id": thread_id}}

print("\n[Step 5] Simulating three different users...")

users = [
    {"id": "u001", "name": "Charlie", "message": "I'm Charlie from Sales. Looking for sales reports."},
    {"id": "u002", "name": "Diana", "message": "Hi, Diana here from Engineering. Need API docs."},
    {"id": "u003", "name": "Eve", "message": "This is Eve from HR. Question about policies."},
]

# Each user starts a conversation
for user in users:
    config = create_thread_id(user["id"])
    result = support_agent.invoke(
        {"messages": [{"role": "user", "content": user["message"]}]},
        config
    )
    print(f"\n  [{user['name']}] {user['message'][:50]}...")
    print(f"  [Agent] {result['messages'][-1].content[:100]}...")

# Follow-up from Charlie
print("\n[Step 6] Charlie follows up (separate user context)...")
config_charlie = create_thread_id("u001")
result = support_agent.invoke(
    {"messages": [{"role": "user", "content": "Who am I and what department?"}]},
    config_charlie
)
print(f"  [Charlie] Who am I and what department?")
print(f"  [Agent] {result['messages'][-1].content}")

# ============================================================================
# PART 3: Multiple Sessions Per User
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Multiple Sessions Per User")
print("=" * 70)

print("""
A single user can have multiple conversation threads.
Useful for:
- Topic-based conversations
- Historical conversation access
- Conversation archiving
""")

# Same user, different sessions
config_orders = create_thread_id("u001", "orders_topic")
config_technical = create_thread_id("u001", "technical_topic")

print("\n[Step 7] User has conversation about orders...")
result1 = support_agent.invoke(
    {"messages": [{"role": "user", "content": "I want to discuss my recent order #12345."}]},
    config_orders
)
print(f"  [Orders Session] User: I want to discuss my recent order #12345.")
print(f"  [Agent] {result1['messages'][-1].content}")

print("\n[Step 8] Same user, different topic (technical)...")
result2 = support_agent.invoke(
    {"messages": [{"role": "user", "content": "I need help with API authentication."}]},
    config_technical
)
print(f"  [Technical Session] User: I need help with API authentication.")
print(f"  [Agent] {result2['messages'][-1].content}")

print("\n[Step 9] Return to orders session - context is preserved...")
result3 = support_agent.invoke(
    {"messages": [{"role": "user", "content": "What order number were we discussing?"}]},
    config_orders
)
print(f"  [Orders Session] User: What order number were we discussing?")
print(f"  [Agent] {result3['messages'][-1].content}")

# ============================================================================
# PART 4: Thread ID Best Practices
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Thread ID Best Practices")
print("=" * 70)

print("""
┌────────────────────────────────────────────────────────────────────┐
│ THREAD ID PATTERNS                                                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ Pattern 1: User-based (one conversation per user)                  │
│   thread_id = f"user_{user_id}"                                    │
│                                                                    │
│ Pattern 2: Session-based (new conversation each session)           │
│   thread_id = f"user_{user_id}_{uuid.uuid4()}"                     │
│                                                                    │
│ Pattern 3: Topic-based (organized conversations)                   │
│   thread_id = f"user_{user_id}_{topic}"                            │
│                                                                    │
│ Pattern 4: Timestamp-based (conversation history)                  │
│   thread_id = f"user_{user_id}_{datetime.now().isoformat()}"       │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│ GUIDELINES                                                         │
├────────────────────────────────────────────────────────────────────┤
│ ✓ Make thread_ids deterministic when you want to resume            │
│ ✓ Include user_id to prevent cross-user data leakage               │
│ ✓ Store thread_id mapping in your database                         │
│ ✗ Don't use random UUIDs if you need to resume later               │
│ ✗ Don't expose thread_ids to end users                             │
└────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Thread-Based Conversations")
print("=" * 70)

print("""
Key Takeaways:

1. thread_id creates isolated conversation contexts
2. Different users = different thread_ids = separate memories
3. Same user can have multiple thread_ids (different topics)
4. Thread ID design is critical for multi-user applications
5. Combine user_id with session/topic for proper isolation
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. How Alice doesn't see Bob's conversation
2. How to design thread_id patterns for real apps
3. Resuming a conversation with the same thread_id

Live Demo Tips:
- Show the thread isolation clearly
- Have trainees suggest thread_id patterns
- Discuss security implications of thread_id design

Discussion Questions:
- "What happens if two users accidentally get the same thread_id?"
- "How would you implement 'start new conversation' in a chat UI?"
- "When would you want to share context across threads?"

Pair Programming Prompt:
Have pairs implement a support chatbot where:
- Each user gets their own thread
- Users can start new topics (new thread)
- Agent remembers user across reconnections
""")

print("=" * 70)
