"""
Demo 01: Tool Creation with @tool Decorator

This demo shows trainees how to:
1. Create tools using the @tool decorator
2. Write effective docstrings for agent routing
3. Handle different parameter and return types
4. Understand how agents interpret tool descriptions

Learning Objectives:
- Master the @tool decorator syntax
- Write clear tool descriptions
- Create tools with various signatures

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/tools
Last Verified: January 2026

References:
- Written Content: readings/2-Tuesday/01-tool-creation-with-decorator.md
"""

import os
from dotenv import load_dotenv
from typing import Optional, List
from pydantic import BaseModel

# Load environment variables
load_dotenv()

from langchain_core.tools import tool

# ============================================================================
# PART 1: Basic Tool Creation
# ============================================================================

print("=" * 70)
print("PART 1: Basic Tool Creation with @tool")
print("=" * 70)

print("""
The @tool decorator transforms any Python function into an agent-callable tool.

Key requirements:
1. Import from langchain_core.tools
2. Add @tool decorator above function
3. Provide a CLEAR docstring (agents read this!)
4. Use type hints for parameters
""")

# Example 1: Simple string tool
@tool
def greet_user(name: str) -> str:
    """Greet a user by name. Use when someone asks to be greeted or says hello."""
    return f"Hello, {name}! Welcome to the LangChain demo."

print("\n[Step 1] Created simple greeting tool:")
print(f"  Name: {greet_user.name}")
print(f"  Description: {greet_user.description}")

# Invoke tool directly (for testing)
print("\n[Step 2] Testing tool directly:")
result = greet_user.invoke({"name": "Alice"})
print(f"  greet_user('Alice') -> {result}")

# Example 2: Calculator tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together. Use for any addition or sum calculation."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers. Use for multiplication or product calculations."""
    return a * b

print("\n[Step 3] Created math tools:")
print(f"  add_numbers: {add_numbers.description}")
print(f"  multiply_numbers: {multiply_numbers.description}")

# Test them
print("\n[Step 4] Testing math tools:")
print(f"  add_numbers(5, 3) -> {add_numbers.invoke({'a': 5, 'b': 3})}")
print(f"  multiply_numbers(5, 3) -> {multiply_numbers.invoke({'a': 5, 'b': 3})}")

# ============================================================================
# PART 2: The Critical Importance of Docstrings
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Why Docstrings Are CRITICAL")
print("=" * 70)

print("""
The docstring IS YOUR TOOL'S IDENTITY to the agent.

❌ BAD docstrings:
   "Does stuff"
   "A useful tool"
   "Processes data"

✅ GOOD docstrings:
   "Search the company database for employee records by name or department."
   "Calculate the total price including tax for an order."
   "Send an email notification to the specified recipient."

The docstring must answer: WHEN should the agent use this tool?
""")

# Demonstrate bad vs good
@tool
def bad_tool(data: str) -> str:
    """Process data."""  # BAD - too vague!
    return data.upper()

@tool
def good_tool(text: str) -> str:
    """Convert text to uppercase. Use when asked to capitalize, shout, or make text all caps."""
    return text.upper()

print("\n[Step 5] Compare tool descriptions:")
print(f"\n  BAD:  '{bad_tool.description}'")
print(f"  GOOD: '{good_tool.description}'")
print("\n  Which would an agent understand better?")

# ============================================================================
# PART 3: Different Parameter Types
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Different Parameter Types")
print("=" * 70)

# Optional parameters
@tool
def search_documents(
    query: str,
    max_results: int = 5,
    category: Optional[str] = None
) -> str:
    """
    Search the document database for relevant content.
    
    Use when asked to find, search, or look up documents.
    Can optionally filter by category (e.g., 'technical', 'legal', 'hr').
    """
    result = f"Searching for '{query}'"
    if category:
        result += f" in category '{category}'"
    result += f" (max {max_results} results)"
    return result

print("\n[Step 6] Tool with optional parameters:")
print(f"  Name: {search_documents.name}")
print(f"  Description: {search_documents.description[:80]}...")

print("\n[Step 7] Testing with different parameter combinations:")
print(f"  Basic: {search_documents.invoke({'query': 'LangChain'})}")
print(f"  With max: {search_documents.invoke({'query': 'LangChain', 'max_results': 10})}")
print(f"  With category: {search_documents.invoke({'query': 'LangChain', 'category': 'technical'})}")

# List parameters
@tool
def analyze_keywords(keywords: List[str]) -> str:
    """
    Analyze a list of keywords for trends and patterns.
    
    Use when asked to analyze, examine, or review multiple keywords or tags.
    """
    return f"Analyzing {len(keywords)} keywords: {', '.join(keywords)}"

print("\n[Step 8] Tool with list parameter:")
result = analyze_keywords.invoke({"keywords": ["python", "ai", "langchain"]})
print(f"  {result}")

# ============================================================================
# PART 4: Structured Input with Pydantic
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Structured Input with Pydantic")
print("=" * 70)

print("""
For complex inputs, use Pydantic models.
This gives you:
1. Automatic validation
2. Clear documentation
3. Type safety
""")

# Define input schema
class OrderDetails(BaseModel):
    """Order information for processing."""
    product_name: str
    quantity: int
    price_per_unit: float

@tool
def calculate_order_total(order: OrderDetails) -> str:
    """
    Calculate the total price for an order.
    
    Use when asked to calculate, compute, or find the total for a product order.
    Requires product name, quantity, and price per unit.
    """
    total = order.quantity * order.price_per_unit
    return f"Order: {order.quantity}x {order.product_name} @ ${order.price_per_unit:.2f} = ${total:.2f}"

print("\n[Step 9] Tool with Pydantic input:")
print(f"  Name: {calculate_order_total.name}")

# Test with structured input
order = {"product_name": "Widget", "quantity": 5, "price_per_unit": 19.99}
result = calculate_order_total.invoke({"order": order})
print(f"  Result: {result}")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Tool Creation with @tool")
print("=" * 70)

print("""
Key Takeaways:

1. @tool decorator from langchain_core.tools creates agent-callable functions
2. DOCSTRINGS ARE CRITICAL - they tell agents when to use your tool
3. Use type hints for all parameters
4. Optional parameters work with defaults
5. Use Pydantic for complex structured inputs
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. Every tool needs a clear, specific docstring
2. Type hints are required for proper agent parsing
3. Test tools directly with .invoke() before using with agents

Live Demo Tips:
- Ask trainees what's wrong with "bad_tool" docstring
- Have them suggest improvements
- Show how tool.name and tool.description are auto-extracted

Common Mistakes:
- Forgetting the docstring (agent won't know when to use it)
- Vague descriptions like "handles data"
- Not using type hints (breaks agent parsing)
- Not testing tools before integration
""")

print("=" * 70)
