# Structured Output with Pydantic

## Learning Objectives
- Understand why structured output matters for reliable agents
- Define output schemas using Pydantic models
- Configure agents to produce structured responses
- Parse and validate structured agent outputs

## Why This Matters

Free-form text is great for human conversation but terrible for programmatic use. If your agent needs to return data that your code will process—like JSON objects, lists, or structured records—you need **structured output**.

Pydantic integration ensures agents return exactly the shape of data you expect, every time.

## The Concept

### The Problem with Free-Form Output

Without structured output:

```python
# Agent returns: "The product is Widget Pro, it costs $49.99, and it's in stock."
# Your code must somehow extract: name, price, stock status
# This is fragile and error-prone!
```

With structured output:

```python
# Agent returns:
{
    "name": "Widget Pro",
    "price": 49.99,
    "in_stock": True
}
# Your code gets exactly what it needs, guaranteed.
```

### Pydantic Models Define the Schema

Pydantic models describe the structure you want:

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class ProductInfo(BaseModel):
    """Information about a product."""
    name: str = Field(description="The product name")
    price: float = Field(description="The price in USD")
    in_stock: bool = Field(description="Whether the product is available")
    categories: List[str] = Field(description="Product categories")
    description: Optional[str] = Field(None, description="Product description")
```

**Key elements:**
- `BaseModel`: Base class for Pydantic models
- `Field`: Provides descriptions that help the model understand each field
- Type hints: Define the data type (str, float, bool, List, etc.)
- Optional: Fields that might not be present

### Using Structured Output with Models

With `init_chat_model`, you can request structured output:

```python
from langchain import init_chat_model
from pydantic import BaseModel

class Sentiment(BaseModel):
    """Analysis of text sentiment."""
    score: float  # -1 to 1
    label: str    # positive, negative, neutral
    confidence: float

model = init_chat_model("openai:gpt-4o-mini")

# Request structured output
result = model.with_structured_output(Sentiment).invoke(
    [{"role": "user", "content": "Analyze: I love this product!"}]
)

print(result)  # Sentiment(score=0.9, label='positive', confidence=0.95)
print(type(result))  # <class 'Sentiment'>
```

### Schema Design Best Practices

**Be explicit with descriptions:**
```python
# ❌ Vague - model may interpret incorrectly
class Order(BaseModel):
    amount: float
    date: str

# ✅ Clear - model knows exactly what to provide
class Order(BaseModel):
    total_amount_usd: float = Field(description="Total order amount in US dollars")
    order_date: str = Field(description="Date in ISO format: YYYY-MM-DD")
    status: str = Field(description="One of: pending, processing, shipped, delivered")
```

**Use appropriate types:**
```python
from typing import List, Optional, Literal
from datetime import date

class Response(BaseModel):
    # Use Literal for enumerated values
    sentiment: Literal["positive", "negative", "neutral"]
    
    # Use List for collections
    keywords: List[str]
    
    # Use Optional for fields that might be missing
    notes: Optional[str] = None
```

### Nested Structures

Pydantic supports complex nested schemas:

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    email: str
    addresses: List[Address]

# Model will return properly nested structure
result = model.with_structured_output(Person).invoke(...)
print(result.addresses[0].city)  # Fully typed access!
```

### Structured Output in Tools

Tools can also return structured data:

```python
from langchain_core.tools import tool
from pydantic import BaseModel

class WeatherData(BaseModel):
    city: str
    temperature_f: float
    condition: str
    humidity_percent: int

@tool
def get_weather(city: str) -> str:
    """Get weather data for a city."""
    # In a real implementation, this would call an API
    data = WeatherData(
        city=city,
        temperature_f=72.5,
        condition="sunny",
        humidity_percent=45
    )
    # Return as JSON string for agent consumption
    return data.model_dump_json()
```

### Handling Validation Errors

Pydantic validates data automatically:

```python
from pydantic import ValidationError

try:
    result = model.with_structured_output(ProductInfo).invoke(...)
    print(f"Valid result: {result}")
except ValidationError as e:
    print(f"Validation failed: {e}")
    # Model output didn't match schema
```

### Common Schema Patterns

**Command/Action schemas:**
```python
class UserCommand(BaseModel):
    action: Literal["create", "update", "delete"]
    resource: str
    parameters: dict
```

**Analysis results:**
```python
class AnalysisResult(BaseModel):
    summary: str
    key_points: List[str]
    confidence: float
    requires_review: bool
```

**Extraction tasks:**
```python
class ExtractedEntities(BaseModel):
    people: List[str]
    organizations: List[str]
    dates: List[str]
    locations: List[str]
```

## Code Example

```python
"""
Structured Output with Pydantic Demo
LangChain Version: v1.0+
"""
from langchain import init_chat_model
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# Define structured output schemas

class MovieReview(BaseModel):
    """A structured movie review analysis."""
    title: str = Field(description="The movie title")
    sentiment: Literal["positive", "negative", "mixed"] = Field(
        description="Overall sentiment of the review"
    )
    rating: float = Field(description="Rating from 0-10")
    pros: List[str] = Field(description="Positive aspects mentioned")
    cons: List[str] = Field(description="Negative aspects mentioned")
    recommended: bool = Field(description="Whether the reviewer recommends the movie")

class TaskExtraction(BaseModel):
    """Extracted tasks from a text."""
    tasks: List[str] = Field(description="List of specific tasks to complete")
    priority_task: Optional[str] = Field(
        None, description="The most important task, if identifiable"
    )
    estimated_duration: Optional[str] = Field(
        None, description="Estimated total time to complete all tasks"
    )

# Create model
model = init_chat_model("openai:gpt-4o-mini", temperature=0)

# Example 1: Movie review analysis
print("=== Movie Review Analysis ===\n")

review_text = """
I watched "The Matrix" last night and it blew my mind! The action sequences 
are incredible and Keanu Reeves is perfect as Neo. The philosophical themes 
about reality are thought-provoking. However, the pacing in the middle was 
a bit slow and some of the dialogue felt wooden. Overall, a must-watch 
classic that holds up after all these years.
"""

review_analysis = model.with_structured_output(MovieReview).invoke([
    {"role": "user", "content": f"Analyze this review:\n\n{review_text}"}
])

print(f"Title: {review_analysis.title}")
print(f"Sentiment: {review_analysis.sentiment}")
print(f"Rating: {review_analysis.rating}/10")
print(f"Pros: {', '.join(review_analysis.pros)}")
print(f"Cons: {', '.join(review_analysis.cons)}")
print(f"Recommended: {'Yes' if review_analysis.recommended else 'No'}")
print()

# Example 2: Task extraction
print("=== Task Extraction ===\n")

email_text = """
Hi,

After our meeting, here's what we need to do:
- Update the proposal with Q4 projections by Friday
- Schedule a follow-up call with the client
- Review the competitor analysis Sarah shared
- Send the contract to legal for review

The proposal update is urgent since the client is waiting.

Thanks!
"""

extracted = model.with_structured_output(TaskExtraction).invoke([
    {"role": "user", "content": f"Extract tasks from this email:\n\n{email_text}"}
])

print(f"Tasks found: {len(extracted.tasks)}")
for i, task in enumerate(extracted.tasks, 1):
    print(f"  {i}. {task}")
print(f"\nPriority task: {extracted.priority_task}")
print(f"Estimated duration: {extracted.estimated_duration}")
```

## Key Takeaways

- **Pydantic defines schemas**: Use `BaseModel` to specify structure
- **Field descriptions help**: Guide the model with clear descriptions
- **Type hints matter**: Use correct types (str, int, List, Literal)
- **`.with_structured_output()`**: Attach schema to model
- **Automatic validation**: Pydantic validates the output
- **Nested structures work**: Build complex, nested schemas
- **Reliable data**: Get exactly the shape you need, guaranteed

## Additional Resources

- [LangChain Structured Output](https://docs.langchain.com/oss/python/langchain/how-to/structured_output)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
- [Type Hints in Python](https://docs.python.org/3/library/typing.html)
