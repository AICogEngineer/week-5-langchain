# Tool Creation with the `@tool` Decorator

## Learning Objectives
- Understand the purpose of tools in LangChain agents
- Create custom tools using the `@tool` decorator
- Write effective docstrings that enable proper agent routing
- Handle different parameter and return types in tools

## Why This Matters

Tools are what make agents *useful*. Without tools, an agent is just a chatbot—it can only respond with text. With tools, an agent can search databases, call APIs, perform calculations, read files, and interact with the real world.

In our **"From Basics to Production"** journey, mastering tool creation is essential because your agents will only be as capable as the tools you give them.

## The Concept

### What is a Tool?

A tool is a Python function wrapped in a way that:
1. The agent can understand what it does (via the docstring)
2. The agent knows what inputs it needs (via type hints)
3. LangChain can serialize calls to it (via the decorator)

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city. Use when users ask about weather."""
    # Implementation here
    return f"The weather in {city} is sunny."
```

### The `@tool` Decorator

The `@tool` decorator from `langchain_core.tools` transforms any Python function into an agent-callable tool:

```python
from langchain_core.tools import tool

@tool
def my_function(param: str) -> str:
    """Description of what this tool does."""
    return "result"
```

**What the decorator does:**
- Extracts the function name as the tool name
- Parses the docstring as the tool description
- Infers the parameter schema from type hints
- Makes the function callable by LangChain agents

### Anatomy of a Good Tool

```python
from langchain_core.tools import tool

@tool
def calculate_tip(bill_amount: float, tip_percentage: float) -> str:
    """
    Calculate the tip for a restaurant bill.
    
    Use this tool when a user wants to know how much to tip.
    The tip_percentage should be a number like 15, 18, or 20 (not 0.15).
    
    Args:
        bill_amount: The total bill amount in dollars
        tip_percentage: The tip percentage (e.g., 15 for 15%)
    
    Returns:
        A string describing the tip amount and total
    """
    tip = bill_amount * (tip_percentage / 100)
    total = bill_amount + tip
    return f"Tip: ${tip:.2f}, Total: ${total:.2f}"
```

**Key elements:**
1. **Type hints on all parameters**: `bill_amount: float`
2. **Return type hint**: `-> str`
3. **Descriptive docstring**: What it does and when to use it
4. **Clear parameter documentation**: What each parameter means

### Docstrings Are Critical

The docstring is the **primary way agents understand your tool**. A poor docstring leads to misuse:

```python
# ❌ BAD - Agent won't know when to use this
@tool
def search(q: str) -> str:
    """Search."""
    return search_database(q)

# ✅ GOOD - Agent understands purpose and usage
@tool
def search_knowledge_base(query: str) -> str:
    """
    Search our product knowledge base for information.
    
    Use this tool when users ask questions about our products,
    pricing, features, or technical specifications.
    Do NOT use for general knowledge questions.
    
    Args:
        query: The search query describing what information to find
    
    Returns:
        Relevant information from the knowledge base, or a message
        if nothing was found.
    """
    return search_database(query)
```

### Parameter Types

Tools support various Python types:

```python
from langchain_core.tools import tool
from typing import List, Optional

# String parameter
@tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

# Numeric parameters
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers together."""
    return a + b

# Optional parameters
@tool
def search(query: str, max_results: Optional[int] = 5) -> str:
    """Search with optional result limit."""
    return f"Found results for '{query}' (max: {max_results})"

# List parameters
@tool
def summarize_texts(texts: List[str]) -> str:
    """Summarize multiple text passages."""
    return f"Summarized {len(texts)} texts"
```

### Return Types

Always return strings for best agent compatibility:

```python
# ✅ PREFERRED - String return
@tool
def get_count(category: str) -> str:
    """Count items in a category."""
    count = database.count(category)
    return f"There are {count} items in {category}."

# ❌ AVOID - Non-string returns can confuse agents
@tool
def get_count_bad(category: str) -> int:
    """Count items in a category."""
    return database.count(category)  # Agent may not interpret correctly
```

### Multiple Tools Example

Agents typically have multiple tools:

```python
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool
def get_current_time() -> str:
    """Get the current time. Use when users ask what time it is."""
    from datetime import datetime
    return datetime.now().strftime("%I:%M %p")

@tool
def get_current_date() -> str:
    """Get today's date. Use when users ask about the date."""
    from datetime import date
    return date.today().strftime("%B %d, %Y")

@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    Use for calculations like "2 + 2" or "sqrt(16)".
    """
    try:
        result = eval(expression)  # Note: Use safer evaluation in production!
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

# Create agent with all tools
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_current_time, get_current_date, calculate],
    system_prompt="You are a helpful assistant with access to time and calculation tools.",
    name="utility_agent"
)
```

### Tool Naming Conventions

The function name becomes the tool name:

```python
# Tool name: "search_products"
@tool
def search_products(query: str) -> str:
    """Search the product catalog."""
    ...

# Tool name: "send_email"
@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    ...
```

**Best practices:**
- Use snake_case: `search_products`, not `searchProducts`
- Be descriptive: `search_knowledge_base`, not `search`
- Use verbs: `get_weather`, `calculate_total`, `send_notification`

## Code Example

```python
"""
Creating Custom Tools with @tool Decorator
LangChain Version: v1.0+
Documentation: https://docs.langchain.com/oss/python/langchain
"""
from langchain_core.tools import tool
from langchain.agents import create_agent
from typing import Optional

# Example 1: Simple tool with one parameter
@tool
def reverse_string(text: str) -> str:
    """
    Reverse a string of text.
    Use when users want to reverse words or sentences.
    """
    return text[::-1]

# Example 2: Tool with multiple parameters
@tool
def format_name(first_name: str, last_name: str, formal: bool = True) -> str:
    """
    Format a person's name.
    
    Args:
        first_name: The person's first name
        last_name: The person's last name  
        formal: If True, use "Mr./Ms. LastName", otherwise "FirstName LastName"
    """
    if formal:
        return f"Mr./Ms. {last_name}"
    return f"{first_name} {last_name}"

# Example 3: Tool that might fail
@tool
def divide_numbers(numerator: float, denominator: float) -> str:
    """
    Divide two numbers.
    Use for division calculations.
    """
    if denominator == 0:
        return "Error: Cannot divide by zero"
    result = numerator / denominator
    return f"{numerator} ÷ {denominator} = {result}"

# Create an agent with our custom tools
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[reverse_string, format_name, divide_numbers],
    system_prompt="You are a helpful assistant. Use your tools when appropriate.",
    name="custom_tools_agent"
)

# Test the agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "Reverse the word 'hello'"}]
})
print(result["messages"][-1].content)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 100 divided by 4?"}]
})
print(result["messages"][-1].content)
```

## Key Takeaways

- **`@tool` decorator** transforms functions into agent-callable tools
- **Docstrings are critical**: They tell agents when and how to use tools
- **Type hints are required**: They define the parameter schema
- **Return strings**: Best compatibility with agent responses
- **Be descriptive**: Good names and documentation prevent misuse
- **Tools enable actions**: Without them, agents can only generate text

## Additional Resources

- [LangChain Tools Documentation](https://docs.langchain.com/oss/python/langchain/concepts/tools)
- [Creating Custom Tools](https://docs.langchain.com/oss/python/langchain/how-to/custom_tools)
- [Tool Best Practices](https://docs.langchain.com/oss/python/langchain/concepts/tool_calling)
