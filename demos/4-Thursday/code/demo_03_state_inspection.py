"""
Demo 03: State Inspection and Debugging

This demo shows trainees how to:
1. Access and inspect agent state
2. View message history in conversations
3. Debug state-related issues
4. Understand message structure

Learning Objectives:
- Access state after agent invocation
- Examine message history structure
- Debug conversation flow issues

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/short-term-memory
Last Verified: January 2026

References:
- Written Content: readings/4-Thursday/04-message-history-management.md
"""

import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# PART 1: Accessing State After Invocation
# ============================================================================

print("=" * 70)
print("PART 1: Accessing Agent State")
print("=" * 70)

print("""
After invoking an agent, the result contains:
- messages: Full conversation history
- Additional state fields (if defined)

This is invaluable for debugging!
""")

@tool
def get_product_info(product_id: str) -> str:
    """Look up product information by ID."""
    products = {
        "P001": "Widget Pro - $49.99 - In Stock",
        "P002": "Gadget Plus - $79.99 - Low Stock",
        "P003": "Super Tool - $129.99 - Out of Stock"
    }
    return products.get(product_id, f"Product {product_id} not found")

# Create agent with memory
debug_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_product_info],
    system_prompt="You help customers find product information.",
    checkpointer=InMemorySaver(),
    name="debug_demo_agent"
)

config = {"configurable": {"thread_id": "debug_session_001"}}

print("\n[Step 1] Making first invocation...")
result1 = debug_agent.invoke(
    {"messages": [{"role": "user", "content": "What's the price of product P001?"}]},
    config
)

print("\n[Step 2] Examining the result object...")
print(f"  Result keys: {list(result1.keys())}")
print(f"  Number of messages: {len(result1['messages'])}")

# ============================================================================
# PART 2: Message History Structure
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Message History Structure")
print("=" * 70)

print("\n[Step 3] Inspecting each message in history...")

for i, msg in enumerate(result1['messages']):
    msg_type = type(msg).__name__
    print(f"\n  Message {i+1}: {msg_type}")
    
    # Different message types have different attributes
    if hasattr(msg, 'content'):
        content_preview = str(msg.content)[:80]
        print(f"    Content: {content_preview}{'...' if len(str(msg.content)) > 80 else ''}")
    
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print(f"    Tool Calls: {len(msg.tool_calls)}")
        for tc in msg.tool_calls:
            print(f"      - {tc.get('name', 'unknown')}: {tc.get('args', {})}")
    
    if hasattr(msg, 'name'):
        print(f"    Name: {msg.name}")

# ============================================================================
# PART 3: Building Conversation History
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Watching State Grow")
print("=" * 70)

print("\n[Step 4] Adding more turns and watching state grow...")

# Turn 2
result2 = debug_agent.invoke(
    {"messages": [{"role": "user", "content": "What about P002?"}]},
    config
)
print(f"  After turn 2: {len(result2['messages'])} messages")

# Turn 3
result3 = debug_agent.invoke(
    {"messages": [{"role": "user", "content": "Which of those two is cheaper?"}]},
    config
)
print(f"  After turn 3: {len(result3['messages'])} messages")

# ============================================================================
# PART 4: Debugging Helper Functions
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Debugging Helper Functions")
print("=" * 70)

def print_message_history(result: dict, last_n: int = None):
    """Print formatted message history for debugging."""
    messages = result.get('messages', [])
    if last_n:
        messages = messages[-last_n:]
    
    print(f"\n{'='*60}")
    print(f"  MESSAGE HISTORY ({len(messages)} messages shown)")
    print(f"{'='*60}")
    
    for i, msg in enumerate(messages):
        role = getattr(msg, 'type', type(msg).__name__)
        
        # Format based on message type
        if role == 'human':
            print(f"\n  👤 USER:")
            print(f"     {msg.content}")
        elif role == 'ai':
            print(f"\n  🤖 ASSISTANT:")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"     [Calling tools: {[tc['name'] for tc in msg.tool_calls]}]")
            if msg.content:
                print(f"     {msg.content[:200]}...")
        elif role == 'tool':
            print(f"\n  🔧 TOOL ({msg.name}):")
            print(f"     {msg.content[:100]}...")
    
    print(f"\n{'='*60}")

print("\n[Step 5] Using the debug helper...")
print_message_history(result3, last_n=6)

# ============================================================================
# PART 5: Identifying Common Issues
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Common Issues to Look For")
print("=" * 70)

print("""
When debugging state, look for:

┌──────────────────────────────────────────────────────────────────────┐
│ ISSUE                           │ WHAT TO CHECK IN STATE            │
├─────────────────────────────────┼───────────────────────────────────┤
│ Agent doesn't remember          │ Is thread_id consistent?          │
│                                 │ Is checkpointer configured?       │
├─────────────────────────────────┼───────────────────────────────────┤
│ Wrong tool called               │ Look at tool_calls in AI message  │
│                                 │ What was the user's request?      │
├─────────────────────────────────┼───────────────────────────────────┤
│ Tool result ignored             │ Is tool result in messages?       │
│                                 │ Did LLM receive tool output?      │
├─────────────────────────────────┼───────────────────────────────────┤
│ Conversation too long           │ Count total messages              │
│                                 │ Check token usage                 │
├─────────────────────────────────┼───────────────────────────────────┤
│ Context confusion               │ Are multiple threads mixed?       │
│                                 │ Check thread_id in each call      │
└──────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
# PART 6: Advanced State Access
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: Getting State Snapshot")
print("=" * 70)

print("""
For more advanced debugging, you can get a state snapshot
directly from the checkpointer using get_state().

Note: The exact method depends on your LangGraph version.
""")

def analyze_conversation(result: dict):
    """Analyze conversation patterns."""
    messages = result.get('messages', [])
    
    stats = {
        'total_messages': len(messages),
        'user_messages': 0,
        'assistant_messages': 0,
        'tool_calls': 0,
        'tool_results': 0
    }
    
    for msg in messages:
        msg_type = getattr(msg, 'type', type(msg).__name__).lower()
        if 'human' in msg_type:
            stats['user_messages'] += 1
        elif 'ai' in msg_type:
            stats['assistant_messages'] += 1
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                stats['tool_calls'] += len(msg.tool_calls)
        elif 'tool' in msg_type:
            stats['tool_results'] += 1
    
    return stats

print("\n[Step 6] Analyzing conversation statistics...")
stats = analyze_conversation(result3)
print(f"\n  Conversation Statistics:")
for key, value in stats.items():
    print(f"    {key}: {value}")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: State Inspection")
print("=" * 70)

print("""
Key Takeaways:

1. Agent results contain full message history in 'messages' key
2. Each message has a type: human, ai, tool
3. AI messages may contain tool_calls
4. Create helper functions for debugging
5. Analyze patterns to identify issues

Debugging Workflow:
1. Print the message history
2. Check message flow (user → AI → tool → AI)
3. Verify tool calls and results
4. Count messages for context window issues
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The structure of different message types
2. How to use helper functions for debugging
3. What patterns indicate common issues

Live Demo Tips:
- Step through message history in debugger
- Show JSON representation of messages
- Have trainees create their own debug helpers

Discussion Questions:
- "How would you log state for production debugging?"
- "What information would you save to a database?"
- "How would you implement conversation export?"

Pair Programming Task:
Have pairs create a debug utility that:
- Exports conversation to JSON
- Summarizes tool usage
- Calculates estimated token count
""")

print("=" * 70)
