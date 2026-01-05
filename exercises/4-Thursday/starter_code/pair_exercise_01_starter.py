"""
Pair Exercise 01: Conversational Agent with Memory - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Build a conversational agent with memory using InMemorySaver.

Pair Programming Instructions:
1. Driver: Types code, focuses on implementation
2. Navigator: Reviews code, catches errors, thinks ahead
3. Rotate every 25-30 minutes!
"""

from typing import Dict, Any, List

# ============================================================================
# IMPORTS
# ============================================================================

# TODO: Import create_agent
# from langchain.agents import create_agent
# from langchain_core.tools import tool

# TODO: Import InMemorySaver for memory
# from langgraph.checkpoint.memory import InMemorySaver


# ============================================================================
# TOOLS FOR THE SUPPORT AGENT
# ============================================================================

# TODO: Create a tool using @tool decorator
# @tool
# def check_subscription_status(customer_name: str) -> str:
#     """Check the subscription status for a customer."""
#     # Mock implementation
#     return f"Subscription for {customer_name}: Active, Premium Plan, renews 2024-12-01"


# ============================================================================
# TODO: TASK 1 - Basic Memory Setup (Driver #1)
# ============================================================================

def create_memory_agent():
    """
    Create a conversational agent with memory.
    
    Requirements:
    - Use create_agent() with InMemorySaver checkpointer
    - Include helpful system prompt about being a support agent
    - Include the 'name' parameter
    
    Returns:
        Configured agent with memory capability
    """
    # TODO: Implement this function
    #
    # checkpointer = InMemorySaver()
    #
    # agent = create_agent(
    #     model="openai:gpt-4o-mini",
    #     tools=[check_subscription_status],
    #     checkpointer=checkpointer,
    #     system_prompt="""You are a helpful customer support agent.
    #     
    #     Remember customer details they share with you (name, issue, etc.)
    #     Be friendly and reference previous context when helpful.
    #     """,
    #     name="support_agent"
    # )
    # return agent
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 2 - Context Retention Test (Driver #2)
# ============================================================================

def test_context_retention(agent) -> bool:
    """
    Test that the agent retains context across turns.
    
    Test scenario:
    1. User introduces themselves with a name
    2. User asks "What's my name?"
    3. Agent should respond with the correct name
    
    Args:
        agent: The memory-enabled agent
        
    Returns:
        True if context is retained, False otherwise
    """
    # TODO: Implement this function
    #
    # thread_id = "test_context_123"
    # config = {"configurable": {"thread_id": thread_id}}
    #
    # # First message: introduction
    # result1 = agent.invoke(
    #     {"messages": [{"role": "user", "content": "Hi, I'm Sarah."}]},
    #     config
    # )
    # print(f"Agent: {result1['messages'][-1].content}")
    #
    # # Second message: ask for name
    # result2 = agent.invoke(
    #     {"messages": [{"role": "user", "content": "What's my name?"}]},
    #     config
    # )
    # response = result2['messages'][-1].content
    # print(f"Agent: {response}")
    #
    # # Check if "Sarah" is in the response
    # return "sarah" in response.lower()
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 3 - Multi-Turn Conversation (Driver #3)
# ============================================================================

def run_multi_turn_conversation(agent) -> List[Dict[str, str]]:
    """
    Run a multi-turn conversation demonstrating memory.
    
    Create a 5-turn conversation where:
    - Turn 1: User introduces and states problem
    - Turn 2: Agent asks clarifying question
    - Turn 3: User provides more details
    - Turn 4: Agent references earlier context
    - Turn 5: Resolution that shows full context awareness
    
    Args:
        agent: The memory-enabled agent
        
    Returns:
        List of conversation turns (dicts with 'role' and 'content')
    """
    # TODO: Implement this function
    #
    # conversation_log = []
    # thread_id = "support_conversation_456"
    # config = {"configurable": {"thread_id": thread_id}}
    #
    # messages = [
    #     "Hi, I'm Mike and my dashboard isn't loading properly.",
    #     "The page shows a spinning icon but never loads.",
    #     "I've tried refreshing but it still doesn't work.",
    #     "Can you summarize what we've discussed so far?",
    #     "Thanks for your help!"
    # ]
    #
    # for msg in messages:
    #     result = agent.invoke(
    #         {"messages": [{"role": "user", "content": msg}]},
    #         config
    #     )
    #     conversation_log.append({"role": "user", "content": msg})
    #     conversation_log.append({
    #         "role": "assistant", 
    #         "content": result['messages'][-1].content
    #     })
    #
    # return conversation_log
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 4 - Memory Inspection (Driver #4)
# ============================================================================

def inspect_memory_state(agent, thread_id: str) -> Dict[str, Any]:
    """
    Inspect the memory state for a given thread.
    
    Args:
        agent: The memory-enabled agent
        thread_id: The thread ID to inspect
        
    Returns:
        Dict containing memory state information:
        - 'thread_id': The thread ID
        - 'message_count': Number of messages
        - 'first_user_message': First user message (if any)
        - 'last_response': Last agent response (if any)
    """
    # TODO: Implement this function
    # Note: Accessing internal state may vary based on implementation
    # This is a simplified version for learning purposes
    #
    # config = {"configurable": {"thread_id": thread_id}}
    # state = agent.get_state(config)
    # 
    # messages = state.get("messages", [])
    #
    # return {
    #     "thread_id": thread_id,
    #     "message_count": len(messages),
    #     "first_user_message": messages[0].content if messages else None,
    #     "last_response": messages[-1].content if messages else None
    # }
    
    pass  # Remove this and add your implementation


# ============================================================================
# TEST HARNESS
# ============================================================================

def main():
    """Run the memory agent exercise."""
    print("=" * 60)
    print("Pair Exercise 01: Conversational Agent with Memory")
    print("=" * 60)
    print()
    
    # Task 1: Create agent
    print("[INFO] Creating agent with memory...")
    agent = create_memory_agent()
    
    if agent is None:
        print("[ERROR] create_memory_agent() not implemented")
        return
    
    print("[OK] Agent created with InMemorySaver")
    print()
    
    # Task 2: Test context retention
    print("=" * 60)
    print("Context Retention Test")
    print("=" * 60)
    print()
    
    retention_works = test_context_retention(agent)
    
    if retention_works is None:
        print("[ERROR] test_context_retention() not implemented")
    elif retention_works:
        print("\n[OK] Context retention working!")
    else:
        print("\n[ERROR] Context retention failed")
    
    print()
    
    # Task 3: Multi-turn conversation
    print("=" * 60)
    print("Multi-Turn Conversation")
    print("=" * 60)
    print()
    
    conversation = run_multi_turn_conversation(agent)
    
    if conversation is None:
        print("[ERROR] run_multi_turn_conversation() not implemented")
    else:
        for turn in conversation:
            prefix = "User:  " if turn["role"] == "user" else "Agent: "
            content = turn["content"][:150] + "..." if len(turn["content"]) > 150 else turn["content"]
            print(f"{prefix}{content}")
        print(f"\n[OK] {len(conversation)} turns completed")
    
    print()
    
    # Task 4: Memory inspection
    print("=" * 60)
    print("Memory State Inspection")
    print("=" * 60)
    print()
    
    memory_state = inspect_memory_state(agent, "support_conversation_456")
    
    if memory_state is None:
        print("[ERROR] inspect_memory_state() not implemented")
    else:
        print(f"Thread ID: {memory_state.get('thread_id')}")
        print(f"Message Count: {memory_state.get('message_count')}")
        print(f"First Message: {memory_state.get('first_user_message', 'N/A')[:50]}...")
        print(f"Last Response: {memory_state.get('last_response', 'N/A')[:50]}...")
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
