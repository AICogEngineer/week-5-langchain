"""
Demo 01: Structured Output with Pydantic

This demo shows trainees how to:
1. Define Pydantic models for structured LLM output
2. Use response_format parameter for type-safe responses
3. Validate and handle output structure
4. Integrate structured output with agents

Learning Objectives:
- Create Pydantic schemas for LLM output
- Use structured output for predictable responses
- Handle validation errors gracefully

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/structured-output
Last Verified: January 2026

References:
- Written Content: readings/5-Friday/01-structured-output-with-pydantic.md
"""

import os
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

# Load environment variables
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# PART 1: The Problem with Unstructured Output
# ============================================================================

print("=" * 70)
print("PART 1: Unstructured Output (The Problem)")
print("=" * 70)

print("""
Without structured output, LLM responses are just text.
Parsing that text is fragile and error-prone.
""")

model = init_chat_model("openai:gpt-4o-mini")

# Unstructured request
print("\n[Step 1] Unstructured response (just text)...")
response = model.invoke(
    "Analyze this product review: 'Great laptop, fast shipping, but battery life is poor.'"
)
print(f"\n  Response (raw text):")
print(f"    {response.content[:200]}...")

print("\n  ❌ Problem: How do we extract specific fields from this?")

# ============================================================================
# PART 2: Define Pydantic Schema
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Defining Pydantic Schemas")
print("=" * 70)

print("""
Pydantic models define the exact structure we want.
The LLM will output JSON matching this schema.
""")

# Define sentiment enum
class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"
    NEUTRAL = "neutral"

# Define structured output schema
class ReviewAnalysis(BaseModel):
    """Analysis of a product review."""
    sentiment: Sentiment = Field(description="Overall sentiment of the review")
    rating_estimate: int = Field(ge=1, le=5, description="Estimated star rating (1-5)")
    pros: List[str] = Field(description="Positive aspects mentioned")
    cons: List[str] = Field(description="Negative aspects mentioned")
    summary: str = Field(description="Brief one-sentence summary")

print("\n[Step 2] Defined ReviewAnalysis schema:")
print(f"  Fields: {list(ReviewAnalysis.model_fields.keys())}")

# ============================================================================
# PART 3: Using Structured Output
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Structured Output with response_format")
print("=" * 70)

print("""
Use the with_structured_output() method to get typed responses.
""")

# Create model with structured output
structured_model = model.with_structured_output(ReviewAnalysis)

print("\n[Step 3] Getting structured response...")
review_text = "Great laptop, fast shipping, but battery life is poor. Screen is amazing!"

result = structured_model.invoke(
    f"Analyze this product review: '{review_text}'"
)

print(f"\n  Structured Response:")
print(f"    Type: {type(result).__name__}")
print(f"    Sentiment: {result.sentiment}")
print(f"    Rating Estimate: {result.rating_estimate}/5")
print(f"    Pros: {result.pros}")
print(f"    Cons: {result.cons}")
print(f"    Summary: {result.summary}")

print("\n  ✓ Clean, typed, validated output!")

# ============================================================================
# PART 4: Complex Nested Schemas
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Complex Nested Schemas")
print("=" * 70)

class ContactInfo(BaseModel):
    """Contact information extracted from text."""
    name: Optional[str] = Field(default=None, description="Person's name")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    company: Optional[str] = Field(default=None, description="Company name")

class MeetingRequest(BaseModel):
    """Structured meeting request information."""
    attendees: List[ContactInfo] = Field(description="People to attend the meeting")
    proposed_date: Optional[str] = Field(default=None, description="Suggested date")
    proposed_time: Optional[str] = Field(default=None, description="Suggested time")
    topic: str = Field(description="Meeting topic or purpose")
    priority: str = Field(description="Priority level: low, medium, or high")

structured_meeting_model = model.with_structured_output(MeetingRequest)

print("\n[Step 4] Extracting meeting details from email...")
email_text = """
Hey team,

Can we set up a call to discuss the Q4 roadmap? I'm thinking next Tuesday at 2pm.
Please include John Smith (john@company.com) and Sarah Johnson from marketing.
This is pretty urgent - we need to finalize before the board meeting.

Thanks!
"""

meeting = structured_meeting_model.invoke(
    f"Extract meeting request details from this email:\n\n{email_text}"
)

print(f"\n  Meeting Request:")
print(f"    Topic: {meeting.topic}")
print(f"    Priority: {meeting.priority}")
print(f"    Proposed Date: {meeting.proposed_date}")
print(f"    Proposed Time: {meeting.proposed_time}")
print(f"    Attendees:")
for attendee in meeting.attendees:
    print(f"      - {attendee.name} ({attendee.email}) - {attendee.company}")

# ============================================================================
# PART 5: Structured Output with Agents
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Structured Output with Agents")
print("=" * 70)

print("""
You can combine structured output with agents.
The agent can use tools, then return a structured response.
""")

class Product(BaseModel):
    """Structured task completion result."""
    product_name: str = Field(description="name of product")
    in_stock: int = Field(description="Amount in Stock")
    on_order: int = Field(description="Product on order")

@tool
def lookup_inventory(product_name: str) -> str:
    """Look up product inventory levels."""
    inventory = {
        "laptop": "42 units in stock, 10 on order",
        "monitor": "0 units in stock, 50 on order",
        "keyboard": "128 units in stock"
    }
    return inventory.get(product_name.lower(), f"Product '{product_name}' not found")

# Create structured agent
structured_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_inventory],
    system_prompt="""You are an inventory assistant. 
    Use the lookup_inventory tool to find product information.
    Provide structured responses about inventory status.""",
    checkpointer=InMemorySaver(),
    response_format=Product,
    name="structured_inventory_agent"
)

print("\n[Step 5] Agent with tools returning structured data...")

# Note: Full structured output integration with agents may require
# response_format configuration in v1.0
result = structured_agent.invoke(
    {"messages": [{"role": "user", "content": "Check inventory for laptop and monitor."}]},
    {"configurable": {"thread_id": "inventory_session"}}
)

print(f"\n  Agent Response:")
print(f"    {result['messages'][-1].content}")

# ============================================================================
# PART 6: Validation and Error Handling
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: Handling Validation Errors")
print("=" * 70)

print("""
Pydantic validates output automatically.
Handle validation errors gracefully!
""")

from pydantic import ValidationError

class StrictRating(BaseModel):
    """Rating that must be between 1 and 5."""
    score: int = Field(ge=1, le=5, description="Rating score 1-5")
    reason: str = Field(min_length=10, description="Reason for the rating (min 10 chars)")

print("\n[Step 6] Testing validation...")

# Valid case
try:
    valid = StrictRating(score=4, reason="Great product with fast delivery!")
    print(f"  ✓ Valid input accepted: score={valid.score}")
except ValidationError as e:
    print(f"  ✗ Validation failed: {e}")

# Invalid case - score out of range
try:
    invalid = StrictRating(score=10, reason="Test")
    print(f"  ✓ Input accepted: score={invalid.score}")
except ValidationError as e:
    print(f"  ✗ Validation failed (expected!): score out of range")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Structured Output with Pydantic")
print("=" * 70)

print("""
Key Takeaways:

1. Define Pydantic models for expected output structure
2. Use with_structured_output() for type-safe responses
3. Nested models work for complex data extraction
4. Validation happens automatically
5. Handle ValidationError for robust applications
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The difference between raw text and structured output
2. How to define appropriate field types
3. Nested schemas for complex extraction

Live Demo Tips:
- Show the raw JSON that comes back
- Demonstrate IDE autocomplete with typed responses
- Try different reviews to see consistent structure

Discussion Questions:
- "What should happen if the LLM can't fill a required field?"
- "When would you use Optional vs required fields?"
- "How would you handle partial extraction?"

Common Mistakes:
- Too strict validation for LLM output
- Missing Optional for fields that may not be present
- Not handling validation errors
""")

print("=" * 70)
