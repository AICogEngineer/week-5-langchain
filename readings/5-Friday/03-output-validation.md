# Output Validation

## Learning Objectives
- Validate model outputs against Pydantic schemas
- Handle validation errors gracefully
- Implement fallback strategies for invalid outputs
- Build robust pipelines that don't crash on bad data

## Why This Matters

Models don't always follow instructions perfectly. Even with structured output enabled, edge cases, ambiguous prompts, or complex schemas can lead to validation failures. Building validation handling into your system prevents crashes and enables graceful degradation.

## The Concept

### Why Validation Can Fail

Even with structured output, issues can occur:

1. **Ambiguous prompts**: Model unsure what to return
2. **Complex schemas**: Many required fields with strict types
3. **Edge case inputs**: Unusual data the model hasn't seen
4. **Model limitations**: Smaller models may struggle with complex schemas
5. **Provider issues**: Temporary API problems

### Pydantic Validation Basics

Pydantic automatically validates data:

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

# Valid
user = User(name="Alice", age=30)  # ✓ Works

# Invalid
try:
    user = User(name="Bob", age="thirty")  # ✗ 'age' must be int
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### Handling Validation Errors

Wrap structured output calls in try/except:

```python
from langchain import init_chat_model
from pydantic import BaseModel, ValidationError

class ProductInfo(BaseModel):
    name: str
    price: float
    in_stock: bool

model = init_chat_model("openai:gpt-4o-mini")

def get_product_info(product_name: str) -> ProductInfo | None:
    """Get product info with validation handling."""
    try:
        result = model.with_structured_output(ProductInfo).invoke([
            {"role": "user", "content": f"Get info about {product_name}"}
        ])
        return result
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None
    except Exception as e:
        print(f"Other error: {e}")
        return None
```

### Fallback Strategies

When validation fails, you have options:

```python
def robust_extraction(text: str) -> dict:
    """Extract data with multiple fallback strategies."""
    
    # Strategy 1: Structured output (preferred)
    try:
        result = model.with_structured_output(DetailedSchema).invoke([
            {"role": "user", "content": text}
        ])
        return result.model_dump()
    except ValidationError:
        pass  # Try next strategy
    
    # Strategy 2: Simpler schema
    try:
        result = model.with_structured_output(SimpleSchema).invoke([
            {"role": "user", "content": text}
        ])
        return result.model_dump()
    except ValidationError:
        pass
    
    # Strategy 3: JSON mode (less strict)
    try:
        json_model = init_chat_model(
            "openai:gpt-4o-mini",
            response_format={"type": "json_object"}
        )
        result = json_model.invoke([
            {"role": "system", "content": "Extract data as JSON"},
            {"role": "user", "content": text}
        ])
        return json.loads(result.content)
    except Exception:
        pass
    
    # Strategy 4: Return minimal/default data
    return {"error": "Could not extract data", "raw": text}
```

### Graceful Degradation

Design systems that handle partial failures:

```python
from typing import Optional
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    summary: str
    confidence: float
    
    # Optional fields allow partial success
    key_points: Optional[list[str]] = None
    sentiment: Optional[str] = None
    entities: Optional[list[str]] = None

# Even if some fields fail, you get something usable
```

### Retry Logic

For transient failures, implement retries:

```python
import time
from pydantic import ValidationError

def get_with_retry(prompt: str, schema, max_retries: int = 3):
    """Retry on validation failures."""
    model = init_chat_model("openai:gpt-4o-mini")
    
    for attempt in range(max_retries):
        try:
            result = model.with_structured_output(schema).invoke([
                {"role": "user", "content": prompt}
            ])
            return result
        except ValidationError as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(1)  # Brief delay before retry
            else:
                raise e  # Exhausted retries
```

### Validation with Custom Logic

Add custom validation beyond type checking:

```python
from pydantic import BaseModel, field_validator

class Order(BaseModel):
    product_name: str
    quantity: int
    price_per_unit: float
    
    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v
    
    @field_validator('price_per_unit')
    @classmethod
    def price_must_be_reasonable(cls, v):
        if v <= 0 or v > 1_000_000:
            raise ValueError('Price must be between 0 and 1,000,000')
        return v
```

### Logging Validation Failures

Track failures for debugging and improvement:

```python
import logging

logger = logging.getLogger(__name__)

def get_structured_data(prompt: str, schema):
    """Get structured data with logging."""
    model = init_chat_model("openai:gpt-4o-mini")
    
    try:
        result = model.with_structured_output(schema).invoke([
            {"role": "user", "content": prompt}
        ])
        logger.info(f"Successfully extracted {schema.__name__}")
        return result
        
    except ValidationError as e:
        logger.warning(
            f"Validation failed for {schema.__name__}: {e}",
            extra={
                "prompt": prompt[:200],
                "schema": schema.__name__,
                "errors": e.errors()
            }
        )
        return None
```

## Code Example

```python
"""
Output Validation Demo
LangChain Version: v1.0+
"""
from langchain import init_chat_model
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, List
import json

# Schema with validation rules
class EventInfo(BaseModel):
    """Information about an event."""
    name: str = Field(min_length=1)
    date: str = Field(pattern=r'\d{4}-\d{2}-\d{2}')  # YYYY-MM-DD
    location: str
    attendee_count: int = Field(ge=0)  # Must be >= 0
    is_virtual: bool
    topics: Optional[List[str]] = None
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v):
        # Additional validation logic
        parts = v.split('-')
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        if month < 1 or month > 12 or day < 1 or day > 31:
            raise ValueError('Invalid date')
        return v

model = init_chat_model("openai:gpt-4o-mini")

def extract_event_info(text: str) -> EventInfo | dict:
    """Extract event info with validation and fallback."""
    
    print(f"Extracting from: '{text[:50]}...'")
    
    # Try structured extraction
    try:
        result = model.with_structured_output(EventInfo).invoke([
            {"role": "user", "content": f"Extract event details from: {text}"}
        ])
        print("✓ Validation passed")
        return result
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e.error_count()} errors")
        
        # Show specific errors
        for error in e.errors():
            print(f"  - {error['loc']}: {error['msg']}")
        
        # Fallback: Return partial data
        return {
            "error": "Validation failed",
            "details": [str(err) for err in e.errors()],
            "raw_input": text
        }
    
    except Exception as e:
        print(f"✗ Other error: {e}")
        return {"error": str(e)}

# Test cases
print("=== Test 1: Well-formed input ===")
result1 = extract_event_info(
    "The Annual Tech Conference 2024 will be held on 2024-06-15 at "
    "the Convention Center. Expected 500 attendees. Topics include AI and Cloud."
)
print(f"Result: {result1}\n")

print("=== Test 2: Ambiguous input ===")
result2 = extract_event_info(
    "Party next week! Everyone's invited!"
)
print(f"Result: {result2}\n")

print("=== Test 3: Invalid date format (might fail validation) ===")
# This tests if the model produces valid data even with tricky prompts
result3 = extract_event_info(
    "Meeting scheduled for 32/13/2024"  # Invalid date
)
print(f"Result: {result3}\n")

# Demonstrate robust pipeline
print("=== Robust Pipeline ===")

def robust_pipeline(text: str) -> dict:
    """Pipeline that always returns something useful."""
    
    # Try full extraction
    result = extract_event_info(text)
    
    if isinstance(result, EventInfo):
        return {
            "status": "success",
            "data": result.model_dump(),
            "confidence": "high"
        }
    elif "error" in result:
        return {
            "status": "partial",
            "data": None,
            "confidence": "low",
            "fallback_message": "Could not fully parse event details"
        }
    
    return {"status": "failed"}

pipeline_result = robust_pipeline("Tech meetup on 2024-03-20 at Downtown Hub")
print(f"Pipeline result: {json.dumps(pipeline_result, indent=2)}")
```

## Key Takeaways

- **Validation can fail**: Even with structured output, handle errors
- **Use try/except**: Wrap structured output calls
- **Implement fallbacks**: Simpler schemas, JSON mode, defaults
- **Log failures**: Track issues for improvement
- **Custom validators**: Add business logic validation in Pydantic
- **Graceful degradation**: Return partial data when possible
- **Retry for transient issues**: Some failures are temporary

## Additional Resources

- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Error Handling Best Practices](https://docs.langchain.com/oss/python/langchain/how-to/error_handling)
- [Fallback Patterns](https://docs.langchain.com/oss/python/langchain/how-to/fallbacks)
