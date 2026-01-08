"""
Demo 02: Error Handling Patterns for Agents

This demo shows trainees how to:
1. Handle common error types in agent systems
2. Implement retry logic with backoff
3. Create fallback mechanisms
4. Build graceful degradation patterns

Learning Objectives:
- Identify common error sources in agent systems
- Implement robust error handling
- Create production-ready agent patterns

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: January 2026

References:
- Written Content: readings/5-Friday/04-error-handling-patterns.md
"""

import os
import time
import random
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# PART 1: Common Error Types
# ============================================================================

print("=" * 70)
print("PART 1: Common Error Types in Agent Systems")
print("=" * 70)

print("""
Agents can fail in many ways:

1. API Errors
   - Rate limits (429)
   - Service unavailable (503)
   - Invalid API key (401)

2. Tool Errors
   - Invalid input
   - External service failures
   - Timeout

3. LLM Errors
   - Context too long
   - Invalid response format
   - Hallucinated tool names

4. Application Errors
   - Schema validation failures
   - Missing required data
   - Business logic violations
""")

# ============================================================================
# PART 2: Tool-Level Error Handling
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Tool-Level Error Handling")
print("=" * 70)

print("""
First line of defense: Handle errors IN the tool.
Return friendly messages, don't let exceptions crash the agent.
""")

# BAD: Tool without error handling
@tool
def bad_api_call(endpoint: str) -> str:
    """Call an external API. BAD: No error handling!"""
    # This would crash on network errors
    import requests
    response = requests.get(endpoint)  # Could throw!
    return response.text

# GOOD: Tool with error handling
print("\n[Step 0] Visualizing Unhandled Errors (Check LangSmith!)")
print("  Calling 'bad_api_call' which will raise an exception...")
try:
    # This URL will fail
    bad_api_call.invoke({"endpoint": "https://this-domain-does-not-exist-12345.com"})
except Exception as e:
    print(f"  ✓ Expected error caught in script: {type(e).__name__}")
    print("    (See the RED trace in LangSmith for 'bad_api_call')")

@tool
def good_api_call(endpoint: str) -> str:
    """
    Call an external API safely.
    Returns error message on failure instead of crashing.
    """
    import requests
    
    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        return response.text[:500]  # Limit response size
    except requests.exceptions.Timeout:
        return "ERROR: Request timed out. The external service is slow. Please try again later."
    except requests.exceptions.ConnectionError:
        return "ERROR: Could not connect to the service. Please check the endpoint URL."
    except requests.exceptions.HTTPError as e:
        return f"ERROR: HTTP error occurred: {e.response.status_code}"
    except Exception as e:
        return f"ERROR: Unexpected error: {type(e).__name__}"

# Simulated flaky service for demo
@tool
def flaky_database_query(query: str) -> str:
    """
    Query the database. This service is sometimes unreliable.
    Use when looking up data from the database.
    """
    # Simulate flaky behavior (30% failure rate)
    if random.random() < 0.3:
        # NOW RAISING AN EXCEPTION (so it shows RED in LangSmith)
        raise ConnectionError("Database connection failed. Please retry.")
    
    # Simulate processing time
    time.sleep(0.2)
    
    return f"Query result for '{query}': [Sample data returned successfully]"

print("\n[Step 1] Testing flaky tool...")
for i in range(5):
    try:
        result = flaky_database_query.invoke({"query": "SELECT * FROM users"})
        status = "✓"
        print(f"  Attempt {i+1}: {status} {result[:50]}...")
    except Exception as e:
        status = "✗"
        print(f"  Attempt {i+1}: {status} ERROR: {e}")

# ============================================================================
# PART 3: Retry Logic with Backoff
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Retry Logic with Exponential Backoff")
print("=" * 70)

print("""
For transient errors, retry with increasing delays.
This handles temporary network issues and rate limits.
""")

def retry_with_backoff(
    func,
    args: dict,
    max_retries: int = 3,
    base_delay: float = 1.0
) -> str:
    """Retry a tool with exponential backoff."""
    last_error = None
    
    for attempt in range(max_retries):
        try:
            # Try to invoke the function
            return func.invoke(args)
        except Exception as e:
            # Catch the exception (shows as failure in trace, but handled here)
            last_error = str(e)
            
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 1s, 2s, 4s
                print(f"    Retry {attempt + 1}/{max_retries} in {delay}s... (Error: {last_error})")
                time.sleep(delay)
    
    return f"FAILED after {max_retries} attempts. Last error: {last_error}"

print("\n[Step 2] Testing retry logic...")
result = retry_with_backoff(flaky_database_query, {"query": "SELECT * FROM orders"})
print(f"  Final result: {result[:80]}...")

# ============================================================================
# PART 4: Fallback Mechanisms
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Fallback Mechanisms")
print("=" * 70)

print("""
When primary method fails, fall back to alternative.
""")

@tool
def primary_search(query: str) -> str:
    """Search using the primary (fast) search engine."""
    # Simulated failure
    if random.random() < 0.5:
        return "ERROR: Primary search unavailable."
    return f"Primary search results for '{query}': Fast, accurate results here."

@tool
def backup_search(query: str) -> str:
    """Search using the backup (slower but reliable) search engine."""
    time.sleep(0.5)  # Simulate slower service
    return f"Backup search results for '{query}': Reliable results from backup system."

def search_with_fallback(query: str) -> str:
    """Try primary search, fall back to backup on failure."""
    # Try primary
    result = primary_search.invoke({"query": query})
    if not result.startswith("ERROR:"):
        return f"[Primary] {result}"
    
    print(f"    Primary failed, trying backup...")
    
    # Fall back to backup
    result = backup_search.invoke({"query": query})
    return f"[Backup] {result}"

print("\n[Step 3] Testing fallback mechanism...")
for i in range(3):
    print(f"\n  Attempt {i+1}:")
    result = search_with_fallback("machine learning tutorials")
    print(f"    {result[:60]}...")

# ============================================================================
# PART 5: Agent-Level Error Handling
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Agent with Robust Tools")
print("=" * 70)

print("""
Build agents with error-handling tools for production.
""")

@tool
def reliable_product_lookup(product_id: str) -> str:
    """
    Look up product information reliably.
    Handles errors gracefully and provides helpful messages.
    """
    # Validate input
    if not product_id or len(product_id) < 2:
        return "ERROR: Invalid product ID. Please provide a valid ID (e.g., 'P001')."
    
    # Simulated product database
    products = {
        "P001": {"name": "Laptop Pro", "price": 999.99, "stock": 42},
        "P002": {"name": "Wireless Mouse", "price": 29.99, "stock": 156},
        "P003": {"name": "USB-C Hub", "price": 49.99, "stock": 0}
    }
    
    product = products.get(product_id.upper())
    if not product:
        return f"ERROR: Product '{product_id}' not found. Available: {list(products.keys())}"
    
    stock_status = "In Stock" if product["stock"] > 0 else "Out of Stock"
    return f"{product['name']} - ${product['price']:.2f} - {stock_status} ({product['stock']} units)"

@tool
def safe_calculation(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Only handles basic arithmetic for safety.
    """
    # Whitelist allowed characters
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "ERROR: Invalid characters in expression. Only numbers and basic operators allowed."
    
    try:
        # Use eval with restrictions (in production, use a proper parser)
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "ERROR: Division by zero is not allowed."
    except Exception as e:
        return f"ERROR: Could not evaluate expression: {type(e).__name__}"

robust_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[reliable_product_lookup, safe_calculation],
    system_prompt="""You are a helpful shopping assistant.
    Use the available tools to help customers.
    If a tool returns an ERROR, explain it to the user clearly and suggest alternatives.""",
    checkpointer=InMemorySaver(),
    name="robust_shopping_agent"
)

print("\n[Step 4] Testing robust agent with various inputs...")
config = {"configurable": {"thread_id": "error_demo_session"}}

test_queries = [
    "What's the price of P001?",           # Valid
    "What's the price of INVALID?",         # Invalid product
    "Calculate 100 * 0.15",                 # Valid calculation
    "Calculate 100 / 0",                    # Division by zero
]

for query in test_queries:
    print(f"\n  Query: {query}")
    result = robust_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config
    )
    response = result['messages'][-1].content
    print(f"  Agent: {response[:150]}...")

# ============================================================================
# PART 6: Error Handling Best Practices
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: Error Handling Best Practices")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│ ERROR HANDLING BEST PRACTICES                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 1. VALIDATE EARLY                                                   │
│    Check inputs at the start of tools                               │
│    Return clear error messages for invalid input                    │
│                                                                     │
│ 2. FAIL GRACEFULLY                                                  │
│    Return error strings, don't raise exceptions                     │
│    Let the agent explain errors to users                            │
│                                                                     │
│ 3. IMPLEMENT RETRIES                                                │
│    Use exponential backoff for transient errors                     │
│    Set reasonable max retries (3-5)                                 │
│                                                                     │
│ 4. PROVIDE FALLBACKS                                                │
│    Have backup options for critical functionality                   │
│    Cache previous results when possible                             │
│                                                                     │
│ 5. LOG ERRORS                                                       │
│    Record errors for debugging (LangSmith helps!)                   │
│    Include context: tool name, inputs, timestamp                    │
│                                                                     │
│ 6. NEVER EXPOSE SECRETS                                             │
│    Sanitize error messages before showing users                     │
│    Don't include API keys, paths, or internal details               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Error Handling Patterns")
print("=" * 70)

print("""
Key Takeaways:

1. Handle errors IN tools - return messages, don't crash
2. Use retry with exponential backoff for transient errors
3. Implement fallback mechanisms for critical operations
4. Validate inputs early and return helpful error messages
5. Never expose internal details in user-facing errors
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The difference between crashing and graceful failure
2. How retry logic handles flaky services
3. Fallback patterns for high availability

Live Demo Tips:
- Show the flaky tool failing and retrying
- Demonstrate how agent explains errors to users
- Run same query multiple times to show retry behavior

Discussion Questions:
- "What's the right number of retries?"
- "When should you fail fast vs retry?"
- "How do you balance user experience with robustness?"

Common Mistakes:
- Letting exceptions crash the agent
- Too many retries (slow experience)
- Exposing technical errors to end users
""")

print("=" * 70)
