"""
Demo X: Built-in Middleware in LangChain v1.0
==============================================
A demo showcasing practical built-in middleware for agents.

Middleware intercepts agent execution to add cross-cutting concerns like:
- Rate limiting (model/tool call limits)
- Retry policies (automatic retries with backoff)
- Cost controls

Reference: https://docs.langchain.com/oss/python/langchain/middleware/built-in
"""

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
    ModelRetryMiddleware,
    ToolRetryMiddleware,
)
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


# === Tools that demonstrate middleware behavior ===

# Failure counter for demonstrating retries
_failure_count = {"unreliable_search": 0}


@tool
def search(query: str) -> str:
    """Search for information about a topic."""
    return f"Search results for: {query}"


@tool
def calculate(expression: str) -> str:
    """Perform a calculation."""
    try:
        result = eval(expression)  # Safe for demo purposes
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"


@tool
def unreliable_search(query: str) -> str:
    """
    A simulated unreliable search that fails twice then succeeds.
    Demonstrates tool retry middleware.
    """
    _failure_count["unreliable_search"] += 1
    if _failure_count["unreliable_search"] <= 2:
        raise Exception(f"Search service timeout (attempt {_failure_count['unreliable_search']})")
    return f"Search results for '{query}': Found 5 relevant articles."


# === 1. Model Call Limit - Demonstrating the limit being hit ===
def demo_model_call_limit():
    """
    Demonstrate model call limits by setting a very low limit.
    The agent will be stopped after 2 model calls.
    """
    print("\n" + "=" * 60)
    print("Example 1: Model Call Limit Middleware")
    print("=" * 60)

    agent = create_agent(
        name="limited_agent",
        model="gpt-4o-mini",
        checkpointer=InMemorySaver(),
        tools=[search, calculate],
        middleware=[
            ModelCallLimitMiddleware(
                run_limit=2,  # Very low limit to demonstrate
                exit_behavior="end",  # Gracefully end when limit hit
            ),
        ],
    )

    # This complex request would normally require multiple model calls
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Search for Python, then calculate 10+5, then search for JavaScript"}]},
        config={"configurable": {"thread_id": "demo-limit"}},
    )
    print(f"Response: {response['messages'][-1].content}")


# === 2. Tool Call Limit - Demonstrating per-tool limits ===
def demo_tool_call_limit():
    """
    Demonstrate tool-specific limits.
    Search is limited to 1 call, calculate is unlimited.
    """
    print("\n" + "=" * 60)
    print("Example 2: Tool Call Limit Middleware")
    print("=" * 60)

    agent = create_agent(
        name="tool_limited_agent",
        model="gpt-4o-mini",
        tools=[search, calculate],
        middleware=[
            ToolCallLimitMiddleware(
                tool_name="search",
                run_limit=1,  # Only allow 1 search
                exit_behavior="continue",  # Return error, agent continues
            ),
        ],
    )

    # Request multiple searches - second one will be blocked
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Search for Python tutorials, then search for JavaScript tutorials"}]}
    )
    print(f"Response: {response['messages'][-1].content}")


# === 3. Tool Retry - Demonstrating automatic retries ===
def demo_tool_retry():
    """
    Demonstrate automatic retries with a flaky tool.
    The unreliable_search tool fails twice then succeeds.
    """
    print("\n" + "=" * 60)
    print("Example 3: Tool Retry Middleware")
    print("=" * 60)
    
    # Reset failure counter
    _failure_count["unreliable_search"] = 0

    agent = create_agent(
        name="retry_agent",
        model="gpt-4o-mini",
        tools=[unreliable_search],
        middleware=[
            ToolRetryMiddleware(
                max_retries=3,
                backoff_factor=1.5,
                initial_delay=0.5,
                tools=["unreliable_search"],
                on_failure="return_message",
            ),
        ],
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Search for LangChain documentation"}]}
    )
    print(f"Response: {response['messages'][-1].content}")


# === 4. Combined Middleware Stack ===
def demo_combined_middleware():
    """
    Production-ready configuration with multiple middleware layers.
    Shows how middleware can be stacked for robust agent behavior.
    """
    print("\n" + "=" * 60)
    print("Example 4: Combined Middleware Stack")
    print("=" * 60)

    agent = create_agent(
        name="production_agent",
        model="gpt-4o-mini",
        checkpointer=InMemorySaver(),
        tools=[search, calculate],
        middleware=[
            # Layer 1: Retry transient failures first
            ModelRetryMiddleware(max_retries=3, on_failure="continue"),
            ToolRetryMiddleware(max_retries=2, on_failure="return_message"),
            # Layer 2: Then enforce limits (after retries)
            ModelCallLimitMiddleware(run_limit=5, exit_behavior="end"),
            ToolCallLimitMiddleware(tool_name="search", run_limit=3),
        ],
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What is 100 / 4?"}]},
        config={"configurable": {"thread_id": "production-1"}},
    )
    print(f"Response: {response['messages'][-1].content}")


# === Run All Demos ===
if __name__ == "__main__":
    print("=" * 60)
    print("LangChain v1.0 Built-in Middleware Demo")
    print("=" * 60)

    demo_model_call_limit()
    demo_tool_call_limit()
    demo_tool_retry()
    demo_combined_middleware()

    print("\n" + "=" * 60)
    print("All middleware demos complete!")
    print("=" * 60)
