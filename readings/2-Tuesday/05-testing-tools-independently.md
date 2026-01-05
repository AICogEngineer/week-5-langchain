# Testing Tools Independently

## Learning Objectives
- Understand why tools should be tested before agent integration
- Execute tools directly without an agent
- Debug common tool errors
- Write reliable tools that handle edge cases

## Why This Matters

When your agent isn't working correctly, is the problem in the tool or the agent's reasoning? If you haven't tested your tools independently, you can't answer this question confidently.

Independent tool testing:
- Isolates bugs to tool logic vs. agent reasoning
- Catches errors before they surface in production
- Enables rapid iteration on tool behavior
- Gives confidence when debugging agent behavior

## The Concept

### The Testing Hierarchy

Before integrating tools with agents, test them in isolation:

```
Level 1: Direct Function Call
    ↓
Level 2: Tool Invocation (via .invoke())
    ↓
Level 3: Integration with Agent
```

Problems at Level 1 will cascade up. Test from the bottom.

### Level 1: Test the Raw Function

Tools are just Python functions. Test them as functions first:

```python
from langchain_core.tools import tool

@tool
def calculate_discount(price: float, discount_percent: float) -> str:
    """Calculate the discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        return "Error: Discount must be between 0 and 100"
    
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return f"Original: ${price:.2f}, Discount: ${discount_amount:.2f}, Final: ${final_price:.2f}"

# Test the underlying function logic
print(calculate_discount.func(100, 20))
# "Original: $100.00, Discount: $20.00, Final: $80.00"

print(calculate_discount.func(100, -5))
# "Error: Discount must be between 0 and 100"
```

### Level 2: Test the Tool Interface

Use `.invoke()` to test the tool as LangChain sees it:

```python
# Test via the tool interface
result = calculate_discount.invoke({"price": 100, "discount_percent": 20})
print(result)
# "Original: $100.00, Discount: $20.00, Final: $80.00"

# Test with invalid input
result = calculate_discount.invoke({"price": 100, "discount_percent": 150})
print(result)
# "Error: Discount must be between 0 and 100"
```

### Common Tool Errors

#### 1. Missing Type Hints

```python
# ❌ BAD - No type hints
@tool
def bad_tool(x, y):
    """Add two numbers."""
    return x + y
# Error: Schema cannot be inferred

# ✅ GOOD - Proper type hints
@tool
def good_tool(x: int, y: int) -> str:
    """Add two numbers."""
    return f"{x} + {y} = {x + y}"
```

#### 2. Non-String Returns

```python
# ❌ BAD - Returns dict (can confuse agents)
@tool
def get_user(user_id: str) -> dict:
    """Get user details."""
    return {"name": "Alice", "age": 30}

# ✅ GOOD - Returns string
@tool
def get_user(user_id: str) -> str:
    """Get user details."""
    user = {"name": "Alice", "age": 30}
    return f"User: {user['name']}, Age: {user['age']}"
```

#### 3. Unhandled Exceptions

```python
# ❌ BAD - Exception crashes the agent
@tool
def risky_divide(a: float, b: float) -> str:
    """Divide two numbers."""
    return str(a / b)  # Crashes on b=0!

# ✅ GOOD - Graceful error handling
@tool
def safe_divide(a: float, b: float) -> str:
    """Divide two numbers."""
    if b == 0:
        return "Error: Cannot divide by zero"
    return f"{a} ÷ {b} = {a / b}"
```

#### 4. Missing or Poor Docstrings

```python
# ❌ BAD - No docstring (agents can't understand it)
@tool
def mystery(x: str) -> str:
    return x.upper()

# ✅ GOOD - Clear docstring
@tool
def convert_to_uppercase(text: str) -> str:
    """
    Convert text to uppercase.
    Use when the user wants text in all capital letters.
    """
    return text.upper()
```

### Writing Test Cases

Create systematic test cases for your tools:

```python
from langchain_core.tools import tool

@tool
def temperature_converter(temp: float, from_unit: str, to_unit: str) -> str:
    """
    Convert temperature between Celsius and Fahrenheit.
    
    Args:
        temp: The temperature value
        from_unit: Either 'C' or 'F'
        to_unit: Either 'C' or 'F'
    """
    if from_unit == to_unit:
        return f"{temp}°{to_unit}"
    
    if from_unit == 'C' and to_unit == 'F':
        result = (temp * 9/5) + 32
    elif from_unit == 'F' and to_unit == 'C':
        result = (temp - 32) * 5/9
    else:
        return f"Error: Invalid units. Use 'C' or 'F'"
    
    return f"{temp}°{from_unit} = {result:.1f}°{to_unit}"

# Test cases
def test_temperature_converter():
    # Normal cases
    assert "32.0°F" in temperature_converter.invoke({
        "temp": 0, "from_unit": "C", "to_unit": "F"
    })
    
    assert "0.0°C" in temperature_converter.invoke({
        "temp": 32, "from_unit": "F", "to_unit": "C"
    })
    
    # Same unit (no conversion)
    assert "100°C" in temperature_converter.invoke({
        "temp": 100, "from_unit": "C", "to_unit": "C"
    })
    
    # Error case
    assert "Error" in temperature_converter.invoke({
        "temp": 100, "from_unit": "X", "to_unit": "Y"
    })
    
    print("All tests passed!")

test_temperature_converter()
```

### Debugging Tool Errors

When a tool isn't working:

1. **Test the function directly**: `tool.func(arg1, arg2)`
2. **Test via invoke**: `tool.invoke({"arg1": val1, "arg2": val2})`
3. **Check the schema**: `print(tool.args_schema.schema())`
4. **Check the description**: `print(tool.description)`
5. **Run with agent and inspect trace**: Use LangSmith (covered Wednesday)

```python
# Inspect tool metadata
print(f"Name: {calculate_discount.name}")
print(f"Description: {calculate_discount.description}")
print(f"Args Schema: {calculate_discount.args_schema.schema()}")
```

### Best Practices for Testable Tools

1. **Return informative error messages** instead of raising exceptions
2. **Validate inputs** at the start of the function
3. **Return strings** for consistent agent handling
4. **Handle edge cases** (empty strings, zeros, nulls)
5. **Keep tools focused** (one job per tool)
6. **Log internally** for debugging complex tools

```python
import logging

@tool
def complex_search(query: str, limit: int = 10) -> str:
    """Search with logging for debugging."""
    logging.debug(f"Search called: query='{query}', limit={limit}")
    
    # Validate
    if not query.strip():
        logging.warning("Empty query provided")
        return "Error: Query cannot be empty"
    
    if limit < 1:
        logging.warning(f"Invalid limit: {limit}")
        return "Error: Limit must be at least 1"
    
    # Execute
    try:
        results = perform_search(query, limit)
        logging.info(f"Found {len(results)} results")
        return format_results(results)
    except Exception as e:
        logging.error(f"Search failed: {e}")
        return f"Error: Search failed - {str(e)}"
```

## Code Example

```python
"""
Testing Tools Independently - Complete Example
LangChain Version: v1.0+
"""
from langchain_core.tools import tool
from langchain.agents import create_agent
from typing import Optional

# Define a tool with proper error handling
@tool
def search_inventory(
    product_name: str,
    warehouse: Optional[str] = None
) -> str:
    """
    Search for products in inventory.
    
    Args:
        product_name: Name of the product to search
        warehouse: Optional warehouse code (e.g., 'WH-1', 'WH-2')
    
    Returns:
        Inventory status for matching products
    """
    # Input validation
    if not product_name.strip():
        return "Error: Product name cannot be empty"
    
    if warehouse and not warehouse.startswith("WH-"):
        return f"Error: Invalid warehouse code '{warehouse}'. Use format 'WH-X'"
    
    # Simulated search
    mock_data = {
        "widget": {"WH-1": 50, "WH-2": 30},
        "gadget": {"WH-1": 0, "WH-2": 15},
    }
    
    product_key = product_name.lower()
    if product_key not in mock_data:
        return f"No products found matching '{product_name}'"
    
    inventory = mock_data[product_key]
    
    if warehouse:
        if warehouse in inventory:
            return f"{product_name} in {warehouse}: {inventory[warehouse]} units"
        return f"{product_name} not found in {warehouse}"
    
    # Return all warehouses
    report = f"Inventory for {product_name}:\n"
    for wh, qty in inventory.items():
        status = f"{qty} units" if qty > 0 else "Out of stock"
        report += f"  {wh}: {status}\n"
    return report.strip()

# ========================================
# TESTING PHASE 1: Direct function calls
# ========================================
print("=== Phase 1: Direct Function Testing ===")

# Test normal case
result = search_inventory.func("widget", None)
print(f"Normal search:\n{result}\n")

# Test with warehouse filter
result = search_inventory.func("gadget", "WH-2")
print(f"Filtered search:\n{result}\n")

# Test error cases
result = search_inventory.func("", None)
print(f"Empty name: {result}\n")

result = search_inventory.func("widget", "INVALID")
print(f"Bad warehouse: {result}\n")

result = search_inventory.func("nonexistent", None)
print(f"Not found: {result}\n")

# ========================================
# TESTING PHASE 2: Tool interface
# ========================================
print("=== Phase 2: Tool Interface Testing ===")

# Test via .invoke() - same as agent will call it
result = search_inventory.invoke({
    "product_name": "widget",
    "warehouse": "WH-1"
})
print(f"Invoke result: {result}\n")

# Inspect tool metadata
print(f"Tool name: {search_inventory.name}")
print(f"Tool description: {search_inventory.description[:100]}...")
print(f"Tool schema: {search_inventory.args_schema.schema()}\n")

# ========================================
# TESTING PHASE 3: Agent integration
# ========================================
print("=== Phase 3: Agent Integration ===")

# Now that tool is tested, integrate with agent
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_inventory],
    system_prompt="You help check product inventory. Use the search tool for inventory questions.",
    name="inventory_agent"
)

# Test the agent uses the tool correctly
result = agent.invoke({
    "messages": [{"role": "user", "content": "Do we have any widgets in WH-1?"}]
})
print(f"Agent response: {result['messages'][-1].content}")
```

## Key Takeaways

- **Test tools before integration**: Isolate problems early
- **Use `.func()` for direct testing**: Access the underlying function
- **Use `.invoke()` for interface testing**: Test as LangChain will call it
- **Handle errors gracefully**: Return error strings, don't raise exceptions
- **Validate inputs early**: Check for invalid/empty inputs
- **Return strings**: Consistent format for agents to process
- **Check metadata**: `tool.name`, `tool.description`, `tool.args_schema`

## Additional Resources

- [LangChain Tool Testing Guide](https://docs.langchain.com/oss/python/langchain/how-to/custom_tools)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [pytest for Python Testing](https://docs.pytest.org/)
