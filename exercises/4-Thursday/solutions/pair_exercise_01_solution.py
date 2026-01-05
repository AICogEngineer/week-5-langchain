"""
Pair Exercise 01: Conversational Agent with Memory - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete solution for conversational agent with InMemorySaver.
"""

from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================================
# TOOLS
# ============================================================================

@tool
def check_subscription_status(customer_name: str) -> str:
    """Check the subscription status for a customer.
    
    Use when the customer asks about their subscription, billing, or account status.
    """
    # Mock implementation
    return f"Subscription for {customer_name}: Active, Premium Plan, renews 2024-12-01"


@tool
def search_help_articles(query: str) -> str:
    """Search help articles for troubleshooting information.
    
    Use when the customer has a technical issue or question.
    """
    return f"Help articles found for '{query}': 1) Troubleshooting guide, 2) FAQ section, 3) Video tutorial"


# ============================================================================
# SOLUTION IMPLEMENTATIONS
# ============================================================================

def create_memory_agent():
    """Create a conversational agent with memory."""
    checkpointer = InMemorySaver()
    
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[check_subscription_status, search_help_articles],
        checkpointer=checkpointer,
        system_prompt="""You are a friendly and helpful customer support agent.

Your responsibilities:
- Help customers with their questions and issues
- Remember details they share (name, issue, preferences)
- Reference previous context to provide personalized support
- Use tools when needed to check account info or find help articles

Be conversational and refer back to what the customer has told you.""",
        name="support_agent"
    )
    return agent


def test_context_retention(agent) -> bool:
    """Test that the agent retains context across turns."""
    thread_id = "test_context_123"
    config = {"configurable": {"thread_id": thread_id}}
    
    print("Testing context retention...")
    print()
    
    # First message: introduction
    result1 = agent.invoke(
        {"messages": [{"role": "user", "content": "Hi, I'm Sarah and I love your product!"}]},
        config
    )
    response1 = result1["messages"][-1].content
    print(f"User:  Hi, I'm Sarah and I love your product!")
    print(f"Agent: {response1[:150]}...")
    print()
    
    # Second message: ask for name
    result2 = agent.invoke(
        {"messages": [{"role": "user", "content": "What was my name again?"}]},
        config
    )
    response2 = result2["messages"][-1].content
    print(f"User:  What was my name again?")
    print(f"Agent: {response2[:150]}...")
    
    # Check if "Sarah" is in the response
    return "sarah" in response2.lower()


def run_multi_turn_conversation(agent) -> List[Dict[str, str]]:
    """Run a multi-turn conversation demonstrating memory."""
    conversation_log = []
    thread_id = "support_conversation_456"
    config = {"configurable": {"thread_id": thread_id}}
    
    messages = [
        "Hi, I'm Mike and my dashboard isn't loading properly.",
        "It shows a spinning icon for about 30 seconds then times out.",
        "I've tried refreshing and clearing my cache but nothing works.",
        "Can you summarize what we've discussed so far?",
        "Thanks for your help! I'll try those solutions."
    ]
    
    for msg in messages:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": msg}]},
            config
        )
        response = result["messages"][-1].content
        
        conversation_log.append({"role": "user", "content": msg})
        conversation_log.append({"role": "assistant", "content": response})
    
    return conversation_log


def inspect_memory_state(agent, thread_id: str) -> Dict[str, Any]:
    """Inspect the memory state for a given thread."""
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        state = agent.get_state(config)
        messages = state.values.get("messages", [])
        
        user_messages = [m for m in messages if hasattr(m, 'type') and m.type == 'human']
        ai_messages = [m for m in messages if hasattr(m, 'type') and m.type == 'ai']
        
        return {
            "thread_id": thread_id,
            "message_count": len(messages),
            "user_message_count": len(user_messages),
            "ai_message_count": len(ai_messages),
            "first_user_message": user_messages[0].content if user_messages else None,
            "last_response": ai_messages[-1].content if ai_messages else None
        }
    except Exception as e:
        return {
            "thread_id": thread_id,
            "error": str(e),
            "message_count": 0
        }


# ============================================================================
# TEST HARNESS
# ============================================================================

def main():
    """Run the memory agent exercise."""
    print("=" * 60)
    print("Pair Exercise 01: Conversational Agent with Memory - Solution")
    print("=" * 60)
    print()
    
    # Task 1: Create agent
    print("[INFO] Creating agent with memory...")
    agent = create_memory_agent()
    print("[OK] Agent 'support_agent' created with InMemorySaver")
    print()
    
    # Task 2: Test context retention
    print("=" * 60)
    print("Context Retention Test")
    print("=" * 60)
    print()
    
    retention_works = test_context_retention(agent)
    
    if retention_works:
        print("\n[OK] Context retention working!")
    else:
        print("\n[WARNING] Context retention may not be working as expected")
    
    print()
    
    # Task 3: Multi-turn conversation
    print("=" * 60)
    print("Multi-Turn Conversation")
    print("=" * 60)
    print()
    
    conversation = run_multi_turn_conversation(agent)
    
    for i, turn in enumerate(conversation):
        prefix = "User:  " if turn["role"] == "user" else "Agent: "
        content = turn["content"]
        if len(content) > 150:
            content = content[:150] + "..."
        print(f"{prefix}{content}")
        if turn["role"] == "assistant":
            print()  # Space after agent responses
    
    print(f"[OK] {len(conversation)} turns completed")
    print()
    
    # Task 4: Memory inspection
    print("=" * 60)
    print("Memory State Inspection")
    print("=" * 60)
    print()
    
    memory_state = inspect_memory_state(agent, "support_conversation_456")
    
    print(f"Thread ID: {memory_state.get('thread_id')}")
    print(f"Total Messages: {memory_state.get('message_count')}")
    print(f"User Messages: {memory_state.get('user_message_count', 'N/A')}")
    print(f"Agent Messages: {memory_state.get('ai_message_count', 'N/A')}")
    
    first_msg = memory_state.get('first_user_message', '')
    if first_msg and len(first_msg) > 50:
        first_msg = first_msg[:50] + "..."
    print(f"First User Message: {first_msg}")
    
    last_resp = memory_state.get('last_response', '')
    if last_resp and len(last_resp) > 50:
        last_resp = last_resp[:50] + "..."
    print(f"Last Response: {last_resp}")
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
