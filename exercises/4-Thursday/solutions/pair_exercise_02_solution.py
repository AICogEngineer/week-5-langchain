"""
Pair Exercise 02: Multi-Thread Support - Solution

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Complete solution for multi-thread conversation management.
"""

from typing import Dict, Any, List
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================================
# THREAD MANAGER
# ============================================================================

@dataclass
class ThreadInfo:
    """Information about a conversation thread."""
    thread_id: str
    user_name: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    message_count: int = 0


class ThreadManager:
    """Manage multiple conversation threads."""
    
    def __init__(self):
        """Initialize the thread manager."""
        self.threads: Dict[str, ThreadInfo] = {}
    
    def create_thread(self, user_identifier: str = None) -> str:
        """Create a new conversation thread."""
        thread_id = f"{user_identifier or 'user'}_{uuid.uuid4().hex[:8]}"
        self.threads[thread_id] = ThreadInfo(
            thread_id=thread_id,
            user_name=user_identifier or ""
        )
        return thread_id
    
    def get_thread_info(self, thread_id: str) -> ThreadInfo:
        """Get information about a thread."""
        return self.threads.get(thread_id)
    
    def update_thread_activity(self, thread_id: str) -> None:
        """Update the last_active timestamp for a thread."""
        if thread_id in self.threads:
            self.threads[thread_id].last_active = datetime.now()
            self.threads[thread_id].message_count += 1
    
    def list_active_threads(self) -> List[str]:
        """List all active thread IDs."""
        return list(self.threads.keys())


# ============================================================================
# TOOLS
# ============================================================================

@tool
def get_user_info(user_name: str) -> str:
    """Get information about a user. Use when you need to look up user details."""
    return f"User {user_name}: Active customer since 2023, Premium subscriber"


# ============================================================================
# AGENT SETUP
# ============================================================================

def create_multi_thread_agent():
    """Create the agent with memory support."""
    checkpointer = InMemorySaver()
    
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[get_user_info],
        checkpointer=checkpointer,
        system_prompt="""You are a helpful assistant that remembers conversation context.

When a user introduces themselves, remember their name.
When asked about their name, respond with what they told you.
Be friendly and personalized in your responses.""",
        name="multi_thread_agent"
    )
    return agent


# ============================================================================
# SOLUTION IMPLEMENTATIONS
# ============================================================================

def run_parallel_conversations(agent, thread_manager: ThreadManager) -> Dict[str, List[str]]:
    """Run parallel conversations with two different users."""
    results = {}
    
    # Create threads for Alice and Bob
    alice_thread = thread_manager.create_thread("alice")
    bob_thread = thread_manager.create_thread("bob")
    
    alice_config = {"configurable": {"thread_id": alice_thread}}
    bob_config = {"configurable": {"thread_id": bob_thread}}
    
    results[alice_thread] = []
    results[bob_thread] = []
    
    print(f"Created thread for Alice: {alice_thread}")
    print(f"Created thread for Bob: {bob_thread}")
    print()
    
    # Alice introduces herself
    print("--- Alice's Thread ---")
    r1 = agent.invoke(
        {"messages": [{"role": "user", "content": "Hello! My name is Alice."}]},
        alice_config
    )
    response1 = r1["messages"][-1].content
    results[alice_thread].append(response1)
    print(f"Alice: Hello! My name is Alice.")
    print(f"Agent: {response1[:100]}...")
    thread_manager.update_thread_activity(alice_thread)
    print()
    
    # Bob introduces himself
    print("--- Bob's Thread ---")
    r2 = agent.invoke(
        {"messages": [{"role": "user", "content": "Hi there, I'm Bob."}]},
        bob_config
    )
    response2 = r2["messages"][-1].content
    results[bob_thread].append(response2)
    print(f"Bob: Hi there, I'm Bob.")
    print(f"Agent: {response2[:100]}...")
    thread_manager.update_thread_activity(bob_thread)
    print()
    
    # Alice asks a follow-up
    print("--- Back to Alice ---")
    r3 = agent.invoke(
        {"messages": [{"role": "user", "content": "What's my name?"}]},
        alice_config
    )
    response3 = r3["messages"][-1].content
    results[alice_thread].append(response3)
    print(f"Alice: What's my name?")
    print(f"Agent: {response3[:100]}...")
    thread_manager.update_thread_activity(alice_thread)
    print()
    
    # Bob asks a follow-up
    print("--- Back to Bob ---")
    r4 = agent.invoke(
        {"messages": [{"role": "user", "content": "Do you remember who I am?"}]},
        bob_config
    )
    response4 = r4["messages"][-1].content
    results[bob_thread].append(response4)
    print(f"Bob: Do you remember who I am?")
    print(f"Agent: {response4[:100]}...")
    thread_manager.update_thread_activity(bob_thread)
    
    return results


def test_thread_isolation(agent, thread_manager: ThreadManager) -> Dict[str, bool]:
    """Test that threads are properly isolated."""
    results = {"alice_correct": False, "bob_correct": False}
    
    # Create fresh threads for isolation test
    alice_thread = thread_manager.create_thread("alice_iso")
    bob_thread = thread_manager.create_thread("bob_iso")
    
    alice_config = {"configurable": {"thread_id": alice_thread}}
    bob_config = {"configurable": {"thread_id": bob_thread}}
    
    # Alice introduces herself
    agent.invoke(
        {"messages": [{"role": "user", "content": "My name is Alice."}]},
        alice_config
    )
    
    # Bob introduces himself
    agent.invoke(
        {"messages": [{"role": "user", "content": "My name is Bob."}]},
        bob_config
    )
    
    # Test Alice's thread
    alice_response = agent.invoke(
        {"messages": [{"role": "user", "content": "What's my name?"}]},
        alice_config
    )
    alice_answer = alice_response["messages"][-1].content.lower()
    results["alice_correct"] = "alice" in alice_answer and "bob" not in alice_answer
    
    # Test Bob's thread
    bob_response = agent.invoke(
        {"messages": [{"role": "user", "content": "What's my name?"}]},
        bob_config
    )
    bob_answer = bob_response["messages"][-1].content.lower()
    results["bob_correct"] = "bob" in bob_answer and "alice" not in bob_answer
    
    return results


def demonstrate_thread_switching(agent, thread_manager: ThreadManager) -> None:
    """Demonstrate switching between threads preserves context."""
    print()
    
    # Create two threads
    thread_a = thread_manager.create_thread("thread_a")
    thread_b = thread_manager.create_thread("thread_b")
    
    config_a = {"configurable": {"thread_id": thread_a}}
    config_b = {"configurable": {"thread_id": thread_b}}
    
    # Start Thread A
    print("--- Starting Thread A ---")
    print("User: I'm in Thread A and my favorite color is blue.")
    ra1 = agent.invoke(
        {"messages": [{"role": "user", "content": "I'm in Thread A and my favorite color is blue."}]},
        config_a
    )
    print(f"Agent: {ra1['messages'][-1].content[:100]}...")
    print()
    
    # Switch to Thread B
    print("--- Switching to Thread B ---")
    print("User: I'm in Thread B and my favorite color is red.")
    rb1 = agent.invoke(
        {"messages": [{"role": "user", "content": "I'm in Thread B and my favorite color is red."}]},
        config_b
    )
    print(f"Agent: {rb1['messages'][-1].content[:100]}...")
    print()
    
    # Back to Thread A
    print("--- Back to Thread A ---")
    print("User: What's my favorite color?")
    ra2 = agent.invoke(
        {"messages": [{"role": "user", "content": "What's my favorite color?"}]},
        config_a
    )
    response_a = ra2['messages'][-1].content
    print(f"Agent: {response_a[:100]}...")
    
    if "blue" in response_a.lower():
        print("[OK] Thread A correctly remembers: blue")
    else:
        print("[WARNING] Thread A context may be incorrect")
    print()
    
    # Back to Thread B
    print("--- Back to Thread B ---")
    print("User: What's my favorite color?")
    rb2 = agent.invoke(
        {"messages": [{"role": "user", "content": "What's my favorite color?"}]},
        config_b
    )
    response_b = rb2['messages'][-1].content
    print(f"Agent: {response_b[:100]}...")
    
    if "red" in response_b.lower():
        print("[OK] Thread B correctly remembers: red")
    else:
        print("[WARNING] Thread B context may be incorrect")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the multi-thread exercise."""
    print("=" * 60)
    print("Pair Exercise 02: Multi-Thread Support - Solution")
    print("=" * 60)
    print()
    
    # Setup
    print("[INFO] Creating thread manager...")
    thread_manager = ThreadManager()
    print("[OK] Thread manager ready")
    print()
    
    print("[INFO] Creating agent...")
    agent = create_multi_thread_agent()
    print("[OK] Agent 'multi_thread_agent' ready")
    print()
    
    # Parallel conversations
    print("=" * 60)
    print("Parallel Conversations")
    print("=" * 60)
    print()
    
    run_parallel_conversations(agent, thread_manager)
    
    print()
    
    # Thread isolation
    print("=" * 60)
    print("Thread Isolation Test")
    print("=" * 60)
    print()
    
    isolation_results = test_thread_isolation(agent, thread_manager)
    
    status = "[OK]" if isolation_results["alice_correct"] else "[ERROR]"
    print(f"{status} Alice's thread correctly identifies as Alice")
    
    status = "[OK]" if isolation_results["bob_correct"] else "[ERROR]"
    print(f"{status} Bob's thread correctly identifies as Bob")
    
    if all(isolation_results.values()):
        print("\n[OK] Threads are properly isolated!")
    else:
        print("\n[WARNING] Thread isolation may not be working correctly")
    
    print()
    
    # Thread switching
    print("=" * 60)
    print("Thread Switching Demo")
    print("=" * 60)
    
    demonstrate_thread_switching(agent, thread_manager)
    
    print()
    
    # Summary
    print("=" * 60)
    print("Thread Summary")
    print("=" * 60)
    print()
    print(f"Total active threads: {len(thread_manager.list_active_threads())}")
    for tid in thread_manager.list_active_threads():
        info = thread_manager.get_thread_info(tid)
        print(f"  - {tid}: {info.message_count} messages")
    
    print()
    print("=" * 60)
    print("Exercise Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
