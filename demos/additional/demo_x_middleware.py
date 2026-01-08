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


# === Simple demo tools ===
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


# === 1. Model Call Limit Middleware ===
# Prevents runaway agents from making too many LLM API calls
def demo_model_call_limit():
    """Limit how many times the model can be called per run/thread."""
    print("\n🔒 Model Call Limit Middleware")
    print("-" * 40)

    agent = create_agent(
        name="limited_agent",
        model="gpt-4o-mini",
        checkpointer=InMemorySaver(),  # Required for thread_limit
        tools=[search, calculate],
        middleware=[
            ModelCallLimitMiddleware(
                thread_limit=10,  # Max calls across entire conversation
                run_limit=5,  # Max calls per single invocation
                exit_behavior="end",  # Options: "end", "error"
            ),
        ],
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What is 2 + 2?"}]},
        config={"configurable": {"thread_id": "demo-1"}},
    )
    print(f"Response: {response['messages'][-1].content}")


# === 2. Tool Call Limit Middleware ===
# Prevents excessive calls to expensive tools or APIs
def demo_tool_call_limit():
    """Limit how many times specific tools can be called."""
    print("\n🔧 Tool Call Limit Middleware")
    print("-" * 40)

    agent = create_agent(
        name="tool_limited_agent",
        model="gpt-4o-mini",
        tools=[search, calculate],
        middleware=[
            # Global limit for all tools
            ToolCallLimitMiddleware(thread_limit=20, run_limit=10),
            # Specific limit for search (expensive external API)
            ToolCallLimitMiddleware(
                tool_name="search",
                thread_limit=5,
                run_limit=3,
                exit_behavior="continue",  # Block with error, agent continues
            ),
        ],
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Calculate 10 * 5"}]}
    )
    print(f"Response: {response['messages'][-1].content}")


# === 3. Model Retry Middleware ===
# Automatic retries with exponential backoff for transient failures
def demo_model_retry():
    """Retry model calls on transient failures."""
    print("\n🔄 Model Retry Middleware")
    print("-" * 40)

    agent = create_agent(
        name="resilient_agent",
        model="gpt-4o-mini",
        tools=[search],
        middleware=[
            ModelRetryMiddleware(
                max_retries=3,  # Retry up to 3 times
                backoff_factor=2.0,  # Exponential backoff multiplier
                initial_delay=1.0,  # Start with 1 second delay
                max_delay=60.0,  # Cap delay at 60 seconds
                jitter=True,  # Add randomness to prevent thundering herd
                on_failure="continue",  # Return error message vs "error" to raise
            ),
        ],
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Hello!"}]}
    )
    print(f"Response: {response['messages'][-1].content}")


# === 4. Tool Retry Middleware ===
# Retry tools on transient failures (network issues, API rate limits)
def demo_tool_retry():
    """Retry tool calls on transient failures."""
    print("\n🛠️ Tool Retry Middleware")
    print("-" * 40)

    agent = create_agent(
        name="tool_retry_agent",
        model="gpt-4o-mini",
        tools=[search, calculate],
        middleware=[
            ToolRetryMiddleware(
                max_retries=3,
                backoff_factor=2.0,
                initial_delay=1.0,
                tools=["search"],  # Only retry search tool
                on_failure="return_message",  # Return error to LLM
            ),
        ],
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Search for Python tutorials"}]}
    )
    print(f"Response: {response['messages'][-1].content}")


# === 5. Combined Middleware Stack ===
# Production-ready agent with multiple middleware layers
def demo_combined_middleware():
    """Combine multiple middleware for production-grade agents."""
    print("\n🏭 Combined Middleware Stack")
    print("-" * 40)

    agent = create_agent(
        name="production_agent",
        model="gpt-4o-mini",
        checkpointer=InMemorySaver(),
        tools=[search, calculate],
        middleware=[
            # Layer 1: Retry transient failures
            ModelRetryMiddleware(max_retries=3, on_failure="continue"),
            ToolRetryMiddleware(max_retries=2, on_failure="return_message"),
            # Layer 2: Enforce limits
            ModelCallLimitMiddleware(run_limit=10, exit_behavior="end"),
            ToolCallLimitMiddleware(tool_name="search", run_limit=5),
        ],
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What is 100 / 4?"}]},
        config={"configurable": {"thread_id": "production-1"}},
    )
    print(f"Response: {response['messages'][-1].content}")


# === Run All Demos ===
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 LangChain v1.0 Built-in Middleware Demo")
    print("=" * 50)

    demo_model_call_limit()
    demo_tool_call_limit()
    demo_model_retry()
    demo_tool_retry()
    demo_combined_middleware()

    print("\n" + "=" * 50)
    print("✅ All middleware demos complete!")
    print("=" * 50)
