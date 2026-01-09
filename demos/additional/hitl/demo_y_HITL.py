"""
Demo Y: Human-in-the-Loop (HITL) Patterns in LangChain v1.0
============================================================
Multiple examples demonstrating HITL patterns for learning.

Examples:
  1. Basic Approval Flow - Simple approve/reject
  2. Edit Capability - Modify tool arguments
  3. Reject with Feedback - Reject with explanation
  4. Streaming with HITL - Using stream() with interrupts
  5. Interactive CLI - Full interactive demo

Reference: https://docs.langchain.com/oss/python/langchain/human-in-the-loop
"""

import os
import uuid
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()


# === Demo Tools ===

@tool
def delete_file(filepath: str) -> str:
    """Delete a file from the filesystem."""
    return f"File '{filepath}' deleted successfully."


@tool
def execute_sql(query: str) -> str:
    """Execute a SQL query against the database."""
    return f"Query executed: {query}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return f"Email sent to {to}: '{subject}'"


@tool
def search_web(query: str) -> str:
    """Search the web (safe, no approval needed)."""
    return f"Results for '{query}': Found 10 relevant articles."


# === Example 1: Basic Approval Flow ===
def example_basic_approval():
    """Demonstrate simple approve/reject flow."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Approval Flow")
    print("=" * 60)

    agent = create_agent(
        name="basic_approval_agent",
        model="gpt-4o-mini",
        tools=[delete_file, search_web],
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "delete_file": True,  # Requires approval
                    "search_web": False,  # No approval needed
                },
            ),
        ],
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    # Trigger a dangerous operation
    print("\nUser: Delete the file old_data.csv")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Delete the file old_data.csv"}]},
        config=config,
    )

    # Handle interrupt
    if "__interrupt__" in result and result["__interrupt__"]:
        interrupt = result["__interrupt__"][0]
        action = interrupt.value["action_requests"][0]
        print(f"\nInterrupt: {action['name']} with args: {action['arguments']}")

        # Approve the action
        print("Decision: APPROVE")
        result = agent.invoke(
            Command(resume={"decisions": [{"type": "approve"}]}),
            config=config,
        )

    print(f"\nAgent: {result['messages'][-1].content}")


# === Example 2: Edit Capability ===
def example_edit_capability():
    """Demonstrate editing tool arguments before execution."""
    print("\n" + "=" * 60)
    print("Example 2: Edit Capability")
    print("=" * 60)

    agent = create_agent(
        name="edit_agent",
        model="gpt-4o-mini",
        tools=[send_email],
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "send_email": {"allowed_decisions": ["approve", "edit", "reject"]},
                },
            ),
        ],
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    print("\nUser: Send an email to bob@example.com about the meeting")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Send an email to bob@example.com about the meeting tomorrow",
                }
            ]
        },
        config=config,
    )

    if "__interrupt__" in result and result["__interrupt__"]:
        interrupt = result["__interrupt__"][0]
        action = interrupt.value["action_requests"][0]
        print(f"\nInterrupt: {action['name']}")
        print(f"   Original args: {action['arguments']}")

        # Edit the email recipient
        print("\nDecision: EDIT (changing recipient to alice@example.com)")
        edited_args = action["arguments"].copy()
        edited_args["to"] = "alice@example.com"

        result = agent.invoke(
            Command(
                resume={
                    "decisions": [
                        {
                            "type": "edit",
                            "edited_action": {
                                "name": "send_email",
                                "args": edited_args,
                            },
                        }
                    ]
                }
            ),
            config=config,
        )

    print(f"\nAgent: {result['messages'][-1].content}")


# === Example 3: Reject with Feedback ===
def example_reject_with_feedback():
    """Demonstrate rejecting with an explanation message."""
    print("\n" + "=" * 60)
    print("Example 3: Reject with Feedback")
    print("=" * 60)

    agent = create_agent(
        name="reject_agent",
        model="gpt-4o-mini",
        tools=[execute_sql],
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={"execute_sql": True},
            ),
        ],
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    print("\nUser: Delete all records from the users table")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Delete all records from the users table"}]},
        config=config,
    )

    if "__interrupt__" in result and result["__interrupt__"]:
        interrupt = result["__interrupt__"][0]
        action = interrupt.value["action_requests"][0]
        print(f"\nInterrupt: {action['name']}")
        print(f"   Query: {action['arguments']}")

        # Reject with explanation
        print("\nDecision: REJECT")
        print("   Reason: 'This would delete all user data. Try a WHERE clause instead.'")
        result = agent.invoke(
            Command(
                resume={
                    "decisions": [
                        {
                            "type": "reject",
                            "message": "This would delete all user data. Please use a WHERE clause to target specific records, such as: DELETE FROM users WHERE status = 'inactive'",
                        }
                    ]
                }
            ),
            config=config,
        )

    print(f"\nAgent: {result['messages'][-1].content}")


# === Example 4: Streaming with HITL ===
def example_streaming_hitl():
    """Demonstrate streaming with interrupt handling."""
    print("\n" + "=" * 60)
    print("Example 4: Streaming with HITL")
    print("=" * 60)

    agent = create_agent(
        name="streaming_agent",
        model="gpt-4o-mini",
        tools=[delete_file, search_web],
        middleware=[
            HumanInTheLoopMiddleware(interrupt_on={"delete_file": True}),
        ],
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    print("\nUser: Search for Python tutorials then delete temp.log")
    print("\nStreaming response:")

    # Stream until interrupt
    interrupt_received = None
    for mode, chunk in agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "First search for Python tutorials, then delete temp.log",
                }
            ]
        },
        config=config,
        stream_mode=["updates", "messages"],
    ):
        if mode == "messages":
            token, metadata = chunk
            if token.content:
                print(token.content, end="", flush=True)
        elif mode == "updates" and "__interrupt__" in chunk:
            interrupt_received = chunk["__interrupt__"]
            print(f"\n\nStream interrupted!")

    # Resume if interrupted
    if interrupt_received:
        action = interrupt_received[0].value["action_requests"][0]
        print(f"   Action: {action['name']} with {action['arguments']}")
        print("\nResuming with approval...")

        for mode, chunk in agent.stream(
            Command(resume={"decisions": [{"type": "approve"}]}),
            config=config,
            stream_mode=["updates", "messages"],
        ):
            if mode == "messages":
                token, metadata = chunk
                if token.content:
                    print(token.content, end="", flush=True)

    print()


# === Example 5: Interactive CLI Demo ===
def example_interactive_cli():
    """Full interactive demo with user input."""
    print("\n" + "=" * 60)
    print("Example 5: Interactive CLI Demo")
    print("=" * 60)

    agent = create_agent(
        name="interactive_agent",
        model="gpt-4o-mini",
        tools=[delete_file, execute_sql, send_email, search_web],
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "delete_file": True,
                    "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                    "send_email": {"allowed_decisions": ["approve", "edit", "reject"]},
                    "search_web": False,
                },
                description_prefix="Approval required",
            ),
        ],
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    print("\nInteractive HITL Demo")
    print("   Type 'quit' to exit")
    print("-" * 40)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        if not user_input:
            continue

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )

        # Handle interrupt loop
        while "__interrupt__" in result and result["__interrupt__"]:
            interrupt = result["__interrupt__"][0]
            action = interrupt.value["action_requests"][0]
            allowed = interrupt.value["review_configs"][0].get(
                "allowed_decisions", ["approve", "edit", "reject"]
            )

            print(f"\nInterrupt: {action['name']}")
            print(f"   Arguments: {action['arguments']}")
            print(f"   Allowed decisions: {allowed}")

            decision = input("   Your decision (approve/edit/reject): ").strip().lower()

            if decision == "approve" and "approve" in allowed:
                result = agent.invoke(
                    Command(resume={"decisions": [{"type": "approve"}]}),
                    config=config,
                )
            elif decision == "edit" and "edit" in allowed:
                print("   (Edit feature: enter new arguments as key=value)")
                # Simplified edit for demo
                result = agent.invoke(
                    Command(
                        resume={
                            "decisions": [
                                {
                                    "type": "edit",
                                    "edited_action": {
                                        "name": action["name"],
                                        "args": action["arguments"],
                                    },
                                }
                            ]
                        }
                    ),
                    config=config,
                )
            elif decision == "reject" and "reject" in allowed:
                reason = input("   Reason for rejection: ").strip()
                result = agent.invoke(
                    Command(resume={"decisions": [{"type": "reject", "message": reason}]}),
                    config=config,
                )
            else:
                print(f"   Invalid decision. Choose from: {allowed}")
                continue

        print(f"\nAgent: {result['messages'][-1].content}")


# === Run All Examples ===
if __name__ == "__main__":
    print("=" * 60)
    print("LangChain v1.0 Human-in-the-Loop (HITL) Demo")
    print("=" * 60)

    # Run non-interactive examples
    example_basic_approval()
    example_edit_capability()
    example_reject_with_feedback()
    example_streaming_hitl()

    # Optionally run interactive demo
    run_interactive = input("\nRun interactive demo? (y/n): ").strip().lower()
    if run_interactive == "y":
        example_interactive_cli()

    print("\n" + "=" * 60)
    print("HITL Demo Complete!")
    print("=" * 60)
