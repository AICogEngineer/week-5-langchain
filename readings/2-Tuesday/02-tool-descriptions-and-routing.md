# Tool Descriptions and Routing

## Learning Objectives
- Understand how agents use tool descriptions to make routing decisions
- Write tool descriptions that maximize correct tool selection
- Differentiate tool use cases to prevent overlap confusion
- Debug and improve tool routing through description refinement

## Why This Matters

Your agent might have 10 tools available, but for any given user request, it needs to pick the right one—or decide to use no tools at all. The quality of your tool descriptions directly determines how often your agent makes the *correct* choice.

Poor descriptions lead to tool misuse, hallucinated tool calls, or agents ignoring tools they should use. In production, this is the difference between a helpful assistant and a frustrating one.

## The Concept

### How Agents Choose Tools

When an agent receives a message, it goes through a decision process:

```
User Message → LLM analyzes message + tool descriptions → Choose action
                                                              │
                    ┌─────────────────────────────────────────┼──────────────┐
                    │                                         │              │
               No tool needed                          Use Tool A       Use Tool B
               (respond directly)                   (with arguments)  (with arguments)
```

The LLM uses the tool descriptions as its **only information** about what tools can do. It doesn't see the implementation—just the name and docstring.

### What Makes a Good Tool Description

A good description answers:
1. **What does this tool do?** (Capability)
2. **When should I use it?** (Trigger conditions)
3. **When should I NOT use it?** (Exclusions)
4. **What should I pass to it?** (Parameter guidance)

```python
@tool
def search_product_catalog(query: str, category: Optional[str] = None) -> str:
    """
    Search our company's product catalog for items.
    
    USE THIS WHEN:
    - User asks about products we sell
    - User wants to find a specific item
    - User asks about pricing or availability
    
    DO NOT USE THIS FOR:
    - General knowledge questions
    - Questions about competitors' products
    - Order status inquiries (use check_order_status instead)
    
    Args:
        query: What to search for (product name, description, or keyword)
        category: Optional category filter (e.g., "electronics", "clothing")
    
    Returns:
        Matching products with names, prices, and availability
    """
    ...
```

### Common Description Mistakes

#### 1. Too Vague
```python
# ❌ BAD - When should I use this?
@tool
def search(q: str) -> str:
    """Search for things."""
    ...

# ✅ GOOD - Clear purpose and trigger
@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the internal knowledge base for policy and procedure documents.
    Use when users ask about company policies, HR procedures, or internal guidelines.
    """
    ...
```

#### 2. Overlapping Descriptions
```python
# ❌ BAD - Agent can't distinguish between these
@tool
def tool_a(query: str) -> str:
    """Search for information."""
    ...

@tool
def tool_b(query: str) -> str:
    """Find information about topics."""
    ...

# ✅ GOOD - Clear differentiation
@tool
def search_public_web(query: str) -> str:
    """Search the public internet for general information."""
    ...

@tool
def search_internal_docs(query: str) -> str:
    """Search internal company documents (not public internet)."""
    ...
```

#### 3. Missing Parameter Guidance
```python
# ❌ BAD - What format should time be?
@tool
def schedule_meeting(time: str) -> str:
    """Schedule a meeting."""
    ...

# ✅ GOOD - Clear format requirements
@tool
def schedule_meeting(time: str) -> str:
    """
    Schedule a calendar meeting.
    
    Args:
        time: Meeting datetime in ISO format (e.g., "2024-03-15T14:30:00")
    """
    ...
```

### Tool Differentiation Strategies

When you have similar tools, use **explicit differentiation**:

```python
@tool
def search_current_inventory(product_name: str) -> str:
    """
    Check CURRENT stock levels for a product.
    Use for: "Do we have X in stock?", "How many X are available?"
    Returns: Current quantity available for immediate purchase.
    """
    ...

@tool
def search_product_history(product_name: str) -> str:
    """
    Look up HISTORICAL sales data for a product.
    Use for: "How did X sell last month?", "What's the sales trend for X?"
    Returns: Past sales figures, trends, and performance data.
    NOT for current stock levels - use search_current_inventory instead.
    """
    ...
```

### Negative Constraints

Sometimes what a tool **shouldn't** be used for is as important as what it should:

```python
@tool
def execute_sql(query: str) -> str:
    """
    Execute a read-only SQL query against the database.
    
    CAPABILITIES:
    - SELECT queries to retrieve data
    - Aggregate functions (COUNT, SUM, AVG)
    
    LIMITATIONS:
    - Cannot INSERT, UPDATE, or DELETE data
    - Cannot modify schema (CREATE, DROP, ALTER)
    - Maximum 1000 rows returned
    
    Args:
        query: A valid SELECT SQL query
    """
    ...
```

### Tool Descriptions and System Prompts Work Together

Your system prompt can reinforce tool selection:

```python
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_web, search_docs, calculate],
    system_prompt="""You are a helpful assistant with three tools:

1. search_web: For general internet questions
2. search_docs: For questions about our company/products
3. calculate: For math problems

ALWAYS check if a question is about our company before using search_web.
When users ask about pricing, use search_docs, not search_web.
""",
    name="routing_demo_agent"
)
```

### Debugging Tool Routing

When agents choose the wrong tool:

1. **Check the description**: Is it clear when to use this tool?
2. **Check for overlaps**: Could another tool's description also match?
3. **Add negative constraints**: Explicitly say when NOT to use it
4. **Test with variations**: "What's the weather?" vs "Weather in NYC?"
5. **Use LangSmith**: Inspect the agent's reasoning (covered Wednesday)

### Description Templates

**For retrieval tools:**
```
Search [SOURCE] for [TYPE OF INFORMATION].
Use when users ask about [TOPICS].
Returns: [WHAT IT RETURNS].
```

**For action tools:**
```
[ACTION VERB] a [THING].
Use when users want to [USER INTENT].
Requires: [REQUIRED INFORMATION].
Will: [WHAT IT DOES].
```

**For calculation tools:**
```
Calculate/Compute [WHAT].
Use for [TYPES OF CALCULATIONS].
Input format: [FORMAT REQUIREMENTS].
Returns: [OUTPUT FORMAT].
```

## Code Example

```python
"""
Tool Descriptions and Routing Demo
LangChain Version: v1.0+
"""
from langchain_core.tools import tool
from langchain.agents import create_agent
from typing import Optional

# Well-differentiated tools with clear descriptions
@tool
def get_product_info(product_id: str) -> str:
    """
    Get detailed information about a specific product by its ID.
    
    USE THIS WHEN:
    - User provides a product ID (like "PROD-123")
    - User asks for full details about a known product
    
    NOT FOR: Searching by name (use search_products instead)
    
    Args:
        product_id: The product ID (format: "PROD-XXX")
    """
    return f"Product {product_id}: Widget Pro, $49.99, In Stock"

@tool
def search_products(query: str, category: Optional[str] = None) -> str:
    """
    Search the product catalog by name or description.
    
    USE THIS WHEN:
    - User is looking for products but doesn't have an ID
    - User describes what they want ("I need a blue widget")
    - User asks what products are available
    
    NOT FOR: Looking up a specific product by ID (use get_product_info)
    
    Args:
        query: Search terms (product name, description, features)
        category: Optional filter ("electronics", "household", etc.)
    """
    return f"Found 3 products matching '{query}'"

@tool
def check_order_status(order_id: str) -> str:
    """
    Check the delivery status of an existing order.
    
    USE THIS WHEN:
    - User asks about their order status
    - User wants to know when their order will arrive
    - User has an order number (format: "ORD-XXXXXX")
    
    NOT FOR: 
    - Product information (use get_product_info or search_products)
    - Placing new orders
    
    Args:
        order_id: The order ID (format: "ORD-XXXXXX")
    """
    return f"Order {order_id}: Shipped, arriving Thursday"

# Create agent with clear system prompt
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_product_info, search_products, check_order_status],
    system_prompt="""You are a helpful e-commerce assistant.

Your tools:
- get_product_info: When user has a product ID
- search_products: When user is looking for products  
- check_order_status: When user asks about an order

Always clarify if you're unsure whether to use product search or order lookup.""",
    name="ecommerce_agent"
)

# Test different routing scenarios
test_messages = [
    "Tell me about product PROD-456",  # Should use get_product_info
    "I'm looking for a blue widget",    # Should use search_products
    "Where is my order ORD-123456?",    # Should use check_order_status
]

for msg in test_messages:
    print(f"\nUser: {msg}")
    result = agent.invoke({"messages": [{"role": "user", "content": msg}]})
    print(f"Agent: {result['messages'][-1].content}")
```

## Key Takeaways

- **Descriptions = routing**: Agents choose tools based entirely on descriptions
- **Answer four questions**: What, when, when not, and how
- **Differentiate clearly**: No overlapping descriptions between tools
- **Add negative constraints**: "DO NOT use for..." prevents misuse
- **System prompts reinforce**: Use both descriptions and prompts together
- **Iterate and test**: Refine descriptions based on observed behavior

## Additional Resources

- [LangChain Tool Calling Concepts](https://docs.langchain.com/oss/python/langchain/concepts/tool_calling)
- [Improving Tool Descriptions](https://docs.langchain.com/oss/python/langchain/how-to/tool_calling)
- [Agent Observability with LangSmith](https://docs.smith.langchain.com/)
