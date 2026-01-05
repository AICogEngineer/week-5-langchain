# Pair Exercise 02: Multi-Thread Support

## Overview

Building on Exercise 01, extend your agent to handle multiple simultaneous conversations. Each conversation needs its own isolated memory, managed through unique `thread_id` values.

## Pair Programming Roles

Continue rotating roles:
- **Driver**: Types the code, focuses on implementation
- **Navigator**: Reviews code, catches errors, thinks about architecture

**Rotate every 25-30 minutes!**

## Learning Objectives

- Manage multiple conversation threads simultaneously
- Understand thread isolation (one thread can't see another's history)
- Implement thread management patterns
- Build a multi-user chat system

## The Scenario

Your support agent is now serving multiple customers at once! Each customer:
1. Has their own conversation thread
2. Cannot see other customers' conversations
3. Maintains their own context independently

You need to demonstrate that thread isolation works correctly.

## Your Tasks

### Task 1: Thread Manager Setup (25 min)

**Driver**: Implement `create_thread_manager()` in the starter code:
- Create a class or functions to manage thread IDs
- Generate unique thread IDs for new conversations
- Track active threads

**Navigator**: Consider:
- How should threads be named/identified?
- How do we track which threads are active?

### Task 2: Parallel Conversations (30 min)

**Rotate roles!**

**Driver**: Implement `run_parallel_conversations()`:
- Start conversations with two different "users"
- Each user introduces themselves with a different name
- Interleave messages between the two conversations
- Verify each thread maintains correct context

**Navigator**: Think about:
- How do we prove thread isolation works?
- What would failure look like?

### Task 3: Thread Isolation Test (25 min)

**Rotate roles!**

**Driver**: Implement `test_thread_isolation()`:
- User A introduces as "Alice"
- User B introduces as "Bob"
- Ask each thread "What's my name?"
- Verify Alice's thread says "Alice", Bob's says "Bob"

**Navigator**: Watch for:
- Are we using the correct thread_id for each call?
- Is there any cross-contamination?

### Task 4: Thread Switching (20 min)

**Rotate roles!**

**Driver**: Implement `demonstrate_thread_switching()`:
- Show a scenario where you switch between threads
- Demonstrate that returning to a thread recalls its context
- Simulate a support agent handling multiple customers

**Navigator**: Consider:
- Real-world scenarios where this matters
- Error handling for invalid thread IDs

## Definition of Done

- [_] Thread manager tracks multiple conversations
- [_] Two parallel conversations maintain separate context
- [_] Thread isolation verified (Alice != Bob)
- [_] Thread switching returns to correct context
- [_] Both partners have driven at least once

## Testing Your Solution

```bash
cd exercises/4-Thursday/starter_code
python pair_exercise_02_starter.py
```

Expected output:
```
=== Multi-Thread Support Test ===

[INFO] Creating thread manager...
[OK] Thread manager ready

=== Parallel Conversations ===

Thread: alice_session
  Alice: Hi, I'm Alice.
  Agent: Hello Alice! How can I help?

Thread: bob_session
  Bob: Hey, I'm Bob.
  Agent: Hi Bob! What can I do for you?

Thread: alice_session  
  Alice: What's my name?
  Agent: Your name is Alice!

Thread: bob_session
  Bob: Do you know who I am?
  Agent: Yes, you're Bob!

=== Thread Isolation Test ===
[OK] alice_session correctly identifies user as Alice
[OK] bob_session correctly identifies user as Bob
[OK] Threads are properly isolated!

=== Thread Switching Demo ===
[Shows switching between threads with context preserved]
```

## Key Patterns

```python
# Different thread_id = different conversation memory
config_alice = {"configurable": {"thread_id": "alice_session"}}
config_bob = {"configurable": {"thread_id": "bob_session"}}

# Alice's conversation
agent.invoke({"messages": [{"role": "user", "content": "I'm Alice"}]}, config_alice)

# Bob's conversation (completely separate)
agent.invoke({"messages": [{"role": "user", "content": "I'm Bob"}]}, config_bob)

# Back to Alice (remembers she's Alice)
agent.invoke({"messages": [{"role": "user", "content": "Who am I?"}]}, config_alice)
# Returns: "You're Alice"
```

## Discussion Questions (for both partners)

1. How would you handle thousands of simultaneous threads?
2. What cleanup strategy would you use for abandoned threads?
3. How does this pattern scale in a production web application?
4. What's the difference between `thread_id` and a session cookie?

## Real-World Applications

- **Customer Support**: Each customer chat is a thread
- **Slack/Teams Bot**: Each channel or DM is a thread
- **Web App**: Each user session is a thread
- **Multi-tenant SaaS**: Each tenant might have multiple threads

## Stretch Goals (Optional)

1. Implement thread cleanup (remove old inactive threads)
2. Add thread listing/enumeration
3. Implement "start new conversation" that creates a new thread for the same user
4. Add metadata to threads (created timestamp, last active, etc.)
