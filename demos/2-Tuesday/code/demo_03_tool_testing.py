"""
Demo 03: Testing Tools Independently

This demo shows trainees how to:
1. Test tools before integrating with agents
2. Handle edge cases in tools
3. Debug tool errors effectively
4. Create robust, production-ready tools

Learning Objectives:
- Develop a tool testing workflow
- Handle errors gracefully in tools
- Validate tool behavior before agent integration

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/tools
Last Verified: January 2026

References:
- Written Content: readings/2-Tuesday/05-testing-tools-independently.md
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent

# ============================================================================
# PART 1: Direct Tool Invocation
# ============================================================================

print("=" * 70)
print("PART 1: Testing Tools Directly")
print("=" * 70)

print("""
ALWAYS test tools before integrating with agents!

Why?
1. Tools should work correctly in isolation
2. Easier to debug tool logic without agent complexity
3. Catches errors before they confuse agents
""")

# Create a tool to test
@tool
def calculate_discount(original_price: float, discount_percent: float) -> str:
    """
    Calculate the discounted price.
    
    Use when asked to apply a discount, calculate savings, or find sale prices.
    """
    discounted = original_price * (1 - discount_percent / 100)
    savings = original_price - discounted
    return f"Original: ${original_price:.2f}, Discount: {discount_percent}%, Final: ${discounted:.2f}, You save: ${savings:.2f}"

print("\n[Step 1] Direct tool invocation for testing:")

# Test with normal inputs
print("\n  Test 1: Normal input (100, 20%)")
result = calculate_discount.invoke({"original_price": 100.0, "discount_percent": 20.0})
print(f"    Result: {result}")

print("\n  Test 2: Different values (49.99, 15%)")
result = calculate_discount.invoke({"original_price": 49.99, "discount_percent": 15.0})
print(f"    Result: {result}")

# ============================================================================
# PART 2: Edge Case Testing
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Edge Case Testing")
print("=" * 70)

print("""
Edge cases your tools should handle:
- Zero values
- Negative numbers
- Very large numbers
- Empty strings
- Special characters
- Invalid input types
""")

print("\n[Step 2] Testing edge cases...")

# Test zero discount
print("\n  Test: 0% discount")
result = calculate_discount.invoke({"original_price": 100.0, "discount_percent": 0.0})
print(f"    Result: {result}")

# Test 100% discount
print("\n  Test: 100% discount (free)")
result = calculate_discount.invoke({"original_price": 100.0, "discount_percent": 100.0})
print(f"    Result: {result}")

# Test negative discount (markup)
print("\n  Test: Negative discount (price increase)")
result = calculate_discount.invoke({"original_price": 100.0, "discount_percent": -20.0})
print(f"    Result: {result}")
print("    ⚠️ Note: Negative discount resulted in higher price - is this expected?")

# ============================================================================
# PART 3: Error Handling in Tools
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Error Handling in Tools")
print("=" * 70)

print("""
Tools should NEVER crash when given bad input!
Instead:
1. Validate inputs
2. Return helpful error messages
3. Let the agent try again or ask for clarification
""")

# BAD: Tool without error handling
@tool
def bad_divide(a: float, b: float) -> float:
    """Divide two numbers. BAD: No error handling!"""
    return a / b  # Will crash on b=0!

# GOOD: Tool with error handling
@tool
def good_divide(a: float, b: float) -> str:
    """
    Divide two numbers safely.
    
    Use for division calculations. Returns error message if division is not possible.
    """
    if b == 0:
        return "Error: Cannot divide by zero. Please provide a non-zero divisor."
    result = a / b
    return f"{a} / {b} = {result:.4f}"

print("\n[Step 3] Comparing error handling...")

print("\n  Testing good_divide with valid input:")
result = good_divide.invoke({"a": 10.0, "b": 3.0})
print(f"    Result: {result}")

print("\n  Testing good_divide with zero divisor:")
result = good_divide.invoke({"a": 10.0, "b": 0.0})
print(f"    Result: {result}")
print("    ✓ Returned helpful error instead of crashing!")

# ============================================================================
# PART 4: Comprehensive Tool with Validation
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Building a Robust Tool")
print("=" * 70)

@tool
def search_products(
    query: str,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None
) -> str:
    """
    Search for products in the catalog.
    
    Use when asked to find, search, or look for products.
    Can filter by category, maximum price, and minimum rating.
    """
    # Input validation
    errors = []
    
    if not query or len(query.strip()) == 0:
        errors.append("Query cannot be empty")
    
    if max_price is not None and max_price < 0:
        errors.append("Max price cannot be negative")
    
    if min_rating is not None:
        if min_rating < 0 or min_rating > 5:
            errors.append("Rating must be between 0 and 5")
    
    if errors:
        return f"Validation errors: {'; '.join(errors)}"
    
    # Simulated search results
    results = [
        f"Searching for: '{query.strip()}'",
    ]
    if category:
        results.append(f"Category filter: {category}")
    if max_price is not None:
        results.append(f"Max price: ${max_price:.2f}")
    if min_rating is not None:
        results.append(f"Min rating: {min_rating}+ stars")
    
    results.append("Found 15 products matching your criteria.")
    
    return " | ".join(results)

print("\n[Step 4] Testing robust tool with various inputs...")

# Valid search
print("\n  Test 1: Valid search")
result = search_products.invoke({
    "query": "laptop",
    "category": "electronics",
    "max_price": 1000.0,
    "min_rating": 4.0
})
print(f"    {result}")

# Empty query
print("\n  Test 2: Empty query (should fail validation)")
result = search_products.invoke({"query": ""})
print(f"    {result}")

# Invalid price
print("\n  Test 3: Negative price (should fail validation)")
result = search_products.invoke({"query": "laptop", "max_price": -50.0})
print(f"    {result}")

# Invalid rating
print("\n  Test 4: Invalid rating (should fail validation)")
result = search_products.invoke({"query": "laptop", "min_rating": 10.0})
print(f"    {result}")

# ============================================================================
# PART 5: Testing Workflow Checklist
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Tool Testing Checklist")
print("=" * 70)

print("""
Before integrating a tool with an agent, verify:

□ Normal inputs work correctly
□ Edge cases are handled (zero, negative, empty, max values)
□ Invalid inputs return helpful error messages (don't crash!)
□ Return values are clear and useful
□ Docstring accurately describes when to use the tool

Testing command:
  result = my_tool.invoke({"param": value})
  print(result)
""")

# ============================================================================
# PART 6: Integration Test
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: Integration Test with Agent")
print("=" * 70)

print("\n[Step 5] Now that tools are tested, integrate with agent...")

test_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[calculate_discount, good_divide, search_products],
    system_prompt="""You are a helpful shopping assistant.
    Use the available tools to help users with calculations and product searches.
    If a tool returns an error, explain it to the user and ask for correct input.""",
    name="shopping_assistant_agent"
)

print("  Agent created with tested tools!")

# Test the agent
print("\n[Step 6] Testing agent with tools...")

queries = [
    "What's the price of a $80 item after a 25% discount?",
    "Search for laptops under $500 with at least 4 stars",
]

for query in queries:
    print(f"\n  User: {query}")
    result = test_agent.invoke({"messages": [{"role": "user", "content": query}]})
    response = result["messages"][-1].content
    print(f"  Agent: {response[:200]}...")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Testing Tools Independently")
print("=" * 70)

print("""
Key Takeaways:

1. ALWAYS test tools with .invoke() before agent integration
2. Test edge cases: zero, negative, empty, max values
3. Handle errors gracefully - return messages, don't crash
4. Validate inputs and provide helpful error messages
5. Only integrate with agents after thorough testing
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The difference between crashing and returning an error
2. How to use .invoke() for direct testing
3. The validation pattern with error collection

Live Demo Tips:
- Intentionally trigger an error in bad_divide
- Show how good_divide handles the same case
- Have trainees suggest edge cases to test

Discussion Questions:
- "What edge cases should you test for a date parsing tool?"
- "How should a tool respond when it can't find data?"
- "When should a tool raise an exception vs return an error message?"

Common Mistakes:
- Not testing before integration
- Forgetting edge cases
- Letting exceptions crash instead of returning errors
- Vague error messages that don't help the user
""")

print("=" * 70)
