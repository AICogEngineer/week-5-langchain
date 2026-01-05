"""
Pair Exercise 02: Multi-Thread Support - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Extend your agent to handle multiple simultaneous conversations.

Pair Programming Instructions:
1. Driver: Types code, focuses on implementation
2. Navigator: Reviews code, catches errors, thinks ahead
3. Rotate every 25-30 minutes!
"""

from typing import Dict, Any, List
import uuid
from dataclasses import dataclass, field
from datetime import datetime

# ============================================================================
# IMPORTS
# ============================================================================

# from langchain.agents import create_agent
# from langchain_core.tools import tool
# from langgraph.checkpoint.memory import InMemorySaver


# ============================================================================
# THREAD MANAGER CLASS
# ============================================================================

@dataclass
class ThreadInfo:
    """Information about a conversation thread."""
    thread_id: str
    user_name: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    message_count: int = 0


# ============================================================================
# TODO: TASK 1 - Thread Manager Setup (Driver #1)
# ============================================================================

class ThreadManager:
    """
    Manage multiple conversation threads.
    
    Responsibilities:
    - Create new threads with unique IDs
    - Track active threads
    - Provide thread information
    """
    
    def __init__(self):
        """Initialize the thread manager."""
        self.threads: Dict[str, ThreadInfo] = {}
    
    def create_thread(self, user_identifier: str = None) -> str:
        """
        Create a new conversation thread.
        
        Args:
            user_identifier: Optional identifier for the user
            
        Returns:
            The unique thread_id for this conversation
        """
        # TODO: Implement this function
        # Generate a unique thread ID
        # Create ThreadInfo and store it
        # Return the thread ID
        
        pass  # Remove this and add your implementation
    
    def get_thread_info(self, thread_id: str) -> ThreadInfo:
        """Get information about a thread."""
        # TODO: Implement this function
        
        pass  # Remove this and add your implementation
    
    def update_thread_activity(self, thread_id: str) -> None:
        """Update the last_active timestamp for a thread."""
        # TODO: Implement this function
        
        pass  # Remove this and add your implementation
    
    def list_active_threads(self) -> List[str]:
        """List all active thread IDs."""
        # TODO: Implement this function
        
        pass  # Remove this and add your implementation


# ============================================================================
# AGENT SETUP (reuse from Exercise 01)
# ============================================================================

def create_multi_thread_agent():
    """Create the agent with memory support."""
    # TODO: Implement (similar to Exercise 01)
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 2 - Parallel Conversations (Driver #2)
# ============================================================================

def run_parallel_conversations(agent, thread_manager: ThreadManager) -> Dict[str, List[str]]:
    """
    Run parallel conversations with two different users.
    
    Scenario:
    - Alice starts a conversation
    - Bob starts a separate conversation
    - Interleave messages between them
    - Each should maintain their own context
    
    Returns:
        Dict mapping thread_id to list of responses
    """
    # TODO: Implement this function
    #
    # alice_thread = thread_manager.create_thread("alice")
    # bob_thread = thread_manager.create_thread("bob")
    #
    # alice_config = {"configurable": {"thread_id": alice_thread}}
    # bob_config = {"configurable": {"thread_id": bob_thread}}
    #
    # # Alice introduces herself
    # alice_msg1 = agent.invoke(
    #     {"messages": [{"role": "user", "content": "Hi, I'm Alice"}]},
    #     alice_config
    # )
    #
    # # Bob introduces himself
    # bob_msg1 = agent.invoke(
    #     {"messages": [{"role": "user", "content": "Hello, I'm Bob"}]},
    #     bob_config
    # )
    #
    # # Continue interleaving...
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 3 - Thread Isolation Test (Driver #3)
# ============================================================================

def test_thread_isolation(agent, thread_manager: ThreadManager) -> Dict[str, bool]:
    """
    Test that threads are properly isolated.
    
    Test:
    1. Alice introduces herself in thread A
    2. Bob introduces himself in thread B
    3. Ask "What's my name?" in thread A - should say Alice
    4. Ask "What's my name?" in thread B - should say Bob
    
    Returns:
        Dict with 'alice_correct' and 'bob_correct' booleans
    """
    # TODO: Implement this function
    #
    # results = {"alice_correct": False, "bob_correct": False}
    #
    # # Create threads
    # alice_thread = thread_manager.create_thread("alice_test")
    # bob_thread = thread_manager.create_thread("bob_test")
    #
    # # Alice introduces herself
    # agent.invoke(
    #     {"messages": [{"role": "user", "content": "I'm Alice"}]},
    #     {"configurable": {"thread_id": alice_thread}}
    # )
    #
    # # Bob introduces himself
    # agent.invoke(
    #     {"messages": [{"role": "user", "content": "I'm Bob"}]},
    #     {"configurable": {"thread_id": bob_thread}}
    # )
    #
    # # Test Alice's thread
    # alice_response = agent.invoke(
    #     {"messages": [{"role": "user", "content": "What's my name?"}]},
    #     {"configurable": {"thread_id": alice_thread}}
    # )
    # results["alice_correct"] = "alice" in alice_response["messages"][-1].content.lower()
    #
    # # Test Bob's thread
    # ...
    #
    # return results
    
    pass  # Remove this and add your implementation


# ============================================================================
# TODO: TASK 4 - Thread Switching (Driver #4)
# ============================================================================

def demonstrate_thread_switching(agent, thread_manager: ThreadManager) -> None:
    """
    Demonstrate switching between threads preserves context.
    
    Scenario:
    1. Start conversation in Thread A
    2. Switch to Thread B, have a different conversation
    3. Return to Thread A, verify context is preserved
    4. Return to Thread B, verify its context is preserved
    
    Print output showing the thread switching and context preservation.
    """
    # TODO: Implement this function
    #
    # thread_a = thread_manager.create_thread("thread_a")
    # thread_b = thread_manager.create_thread("thread_b")
    #
    # print("\n--- Starting Thread A ---")
    # # Conversation in Thread A
    #
    # print("\n--- Switching to Thread B ---")
    # # Different conversation in Thread B
    #
    # print("\n--- Back to Thread A ---")
    # # Verify Thread A still has its context
    #
    # print("\n--- Back to Thread B ---")
    # # Verify Thread B still has its context
    
    pass  # Remove this and add your implementation


# ============================================================================
# TEST HARNESS
# ============================================================================

def main():
    """Run the multi-thread exercise."""
    print("=" * 60)
    print("Pair Exercise 02: Multi-Thread Support")
    print("=" * 60)
    print()
    
    # Setup
    print("[INFO] Creating thread manager...")
    thread_manager = ThreadManager()
    
    if not hasattr(thread_manager, 'threads'):
        print("[ERROR] ThreadManager not properly initialized")
        return
    
    print("[OK] Thread manager ready")
    print()
    
    print("[INFO] Creating agent...")
    agent = create_multi_thread_agent()
    
    if agent is None:
        print("[ERROR] create_multi_thread_agent() not implemented")
        return
    
    print("[OK] Agent ready")
    print()
    
    # Task 2: Parallel conversations
    print("=" * 60)
    print("Parallel Conversations")
    print("=" * 60)
    print()
    
    parallel_results = run_parallel_conversations(agent, thread_manager)
    
    if parallel_results is None:
        print("[ERROR] run_parallel_conversations() not implemented")
    else:
        for thread_id, responses in parallel_results.items():
            print(f"Thread: {thread_id}")
            for r in responses:
                print(f"  {r[:100]}...")
            print()
    
    # Task 3: Thread isolation
    print("=" * 60)
    print("Thread Isolation Test")
    print("=" * 60)
    print()
    
    isolation_results = test_thread_isolation(agent, thread_manager)
    
    if isolation_results is None:
        print("[ERROR] test_thread_isolation() not implemented")
    else:
        status = "[OK]" if isolation_results.get("alice_correct") else "[ERROR]"
        print(f"{status} Alice's thread: correctly identifies as Alice")
        
        status = "[OK]" if isolation_results.get("bob_correct") else "[ERROR]"
        print(f"{status} Bob's thread: correctly identifies as Bob")
        
        if all(isolation_results.values()):
            print("\n[OK] Threads are properly isolated!")
    
    print()
    
    # Task 4: Thread switching
    print("=" * 60)
    print("Thread Switching Demo")
    print("=" * 60)
    
    demonstrate_thread_switching(agent, thread_manager)
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
