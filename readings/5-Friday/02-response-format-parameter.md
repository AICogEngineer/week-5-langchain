# The `response_format` Parameter

## Learning Objectives
- Understand the `response_format` parameter for structured responses
- Distinguish between JSON mode and structured schemas
- Configure response format in model calls
- Choose the right approach for your use case

## Why This Matters

Different scenarios call for different levels of structure. Sometimes you just need valid JSON; other times you need data matching an exact schema. The `response_format` parameter gives you control over how structured the output is.

## The Concept

### What is `response_format`?

The `response_format` parameter tells the model what format to use for its response. Options include:

| Mode | Description | Guaranteed? |
|------|-------------|-------------|
| Default | Natural text | No structure |
| JSON mode | Valid JSON | Valid JSON, but no schema |
| Structured schema | Matches Pydantic model | Always matches schema |

### JSON Mode vs. Structured Schema

**JSON Mode:**
```python
# Model WILL return valid JSON, but shape isn't guaranteed
{"some_field": "value", "other": 123}
```

**Structured Schema:**
```python
# Model WILL return data matching your exact schema
{"name": "Alice", "age": 30}  # If schema requires name:str, age:int
```

### Using JSON Mode

For simple JSON output without a strict schema:

```python
from langchain import init_chat_model

model = init_chat_model(
    "openai:gpt-4o-mini",
    response_format={"type": "json_object"}  # JSON mode
)

result = model.invoke([
    {"role": "system", "content": "Respond with JSON containing a greeting and time."},
    {"role": "user", "content": "Say hello"}
])

import json
data = json.loads(result.content)
print(data)  # {"greeting": "Hello!", "time": "afternoon"} (shape not guaranteed)
```

**Important**: In JSON mode, you must mention "JSON" in your prompt, or the call may fail.

### Using Structured Schemas (Preferred)

For guaranteed schema compliance, use Pydantic with `.with_structured_output()`:

```python
from langchain import init_chat_model
from pydantic import BaseModel

class Greeting(BaseModel):
    message: str
    formal: bool
    language: str

model = init_chat_model("openai:gpt-4o-mini")

# This guarantees the output matches the schema
result = model.with_structured_output(Greeting).invoke([
    {"role": "user", "content": "Create a formal greeting in Spanish"}
])

print(result)  # Greeting(message="Buenos días", formal=True, language="Spanish")
print(type(result))  # <class 'Greeting'>
```

### When to Use Each

| Situation | Use |
|-----------|-----|
| Need specific fields | Structured schema (Pydantic) |
| Flexible JSON structure | JSON mode |
| Dynamic/unknown fields | JSON mode |
| Programmatic processing | Structured schema |
| Data validation | Structured schema |
| Quick experimentation | JSON mode |

### Provider Differences

Not all providers support `response_format` the same way:

| Provider | JSON Mode | Structured Output |
|----------|-----------|-------------------|
| OpenAI | ✅ `json_object` | ✅ Full support |
| Anthropic | ⚠️ Via prompting | ✅ Via tools |
| Bedrock | Varies by model | Varies by model |

LangChain's `.with_structured_output()` abstracts these differences.

### Combining with System Prompts

Even with structured output, system prompts improve quality:

```python
from pydantic import BaseModel, Field

class Summary(BaseModel):
    main_points: list[str] = Field(description="Key points, max 5")
    word_count: int = Field(description="Original document word count")

result = model.with_structured_output(Summary).invoke([
    {
        "role": "system", 
        "content": "Summarize documents concisely. Focus on key facts, not opinions."
    },
    {"role": "user", "content": f"Summarize: {document}"}
])
```

The system prompt guides content; the schema guarantees structure.

### Error Cases

**JSON mode without "JSON" mention:**
```python
# ❌ May fail
model = init_chat_model("openai:gpt-4o-mini", response_format={"type": "json_object"})
model.invoke([{"role": "user", "content": "Say hello"}])
# Error: Must mention JSON in prompt

# ✅ Works
model.invoke([
    {"role": "system", "content": "Respond in JSON format"},
    {"role": "user", "content": "Say hello"}
])
```

**Invalid schema for structured output:**
```python
# If model can't produce valid output, you may get validation errors
# Always handle these gracefully
from pydantic import ValidationError

try:
    result = model.with_structured_output(MySchema).invoke(...)
except ValidationError as e:
    # Handle the error
    print(f"Output didn't match schema: {e}")
```

### Strict Mode (OpenAI)

OpenAI offers "strict mode" for guaranteed schema adherence:

```python
# The LangChain abstractions handle this for you
# But it's worth knowing it exists

result = model.with_structured_output(
    MySchema,
    strict=True  # OpenAI strict mode - guarantees exact schema match
).invoke(...)
```

## Code Example

```python
"""
response_format Parameter Demo
LangChain Version: v1.0+
"""
from langchain import init_chat_model
from pydantic import BaseModel, Field
from typing import List
import json

# ============================================
# Example 1: JSON Mode (flexible structure)
# ============================================
print("=== JSON Mode ===\n")

json_model = init_chat_model(
    "openai:gpt-4o-mini",
    response_format={"type": "json_object"}
)

result = json_model.invoke([
    {"role": "system", "content": "Always respond with JSON containing relevant data."},
    {"role": "user", "content": "Describe the weather in New York briefly"}
])

# Must parse JSON manually
data = json.loads(result.content)
print(f"Raw JSON: {result.content}")
print(f"Parsed: {data}")
print(f"Type: {type(data)}")  # dict, not a typed object
print()

# ============================================
# Example 2: Structured Schema (strict type)
# ============================================
print("=== Structured Schema ===\n")

class WeatherReport(BaseModel):
    city: str
    temperature_celsius: float
    condition: str = Field(description="e.g., sunny, cloudy, rainy")
    humidity_percent: int
    forecast: List[str] = Field(description="Next 3 days forecast")

model = init_chat_model("openai:gpt-4o-mini")

weather = model.with_structured_output(WeatherReport).invoke([
    {"role": "user", "content": "Give me weather info for Tokyo"}
])

# Fully typed access
print(f"City: {weather.city}")
print(f"Temperature: {weather.temperature_celsius}°C")
print(f"Condition: {weather.condition}")
print(f"Humidity: {weather.humidity_percent}%")
print(f"Forecast: {', '.join(weather.forecast)}")
print(f"Type: {type(weather)}")  # WeatherReport
print()

# ============================================
# Comparison: Same request, different output
# ============================================
print("=== Comparison ===\n")

prompt = "List 3 programming languages and their typical use cases"

# JSON mode - structure varies
json_result = json_model.invoke([
    {"role": "system", "content": "Respond with JSON data"},
    {"role": "user", "content": prompt}
])
print(f"JSON mode result type: {type(json.loads(json_result.content))}")

# Structured mode - always matches schema
class LanguageInfo(BaseModel):
    languages: List[dict]

structured_result = model.with_structured_output(LanguageInfo).invoke([
    {"role": "user", "content": prompt}
])
print(f"Structured result type: {type(structured_result)}")
print(f"Has 'languages' attr: {hasattr(structured_result, 'languages')}")
```

## Key Takeaways

- **JSON mode**: Guarantees valid JSON, but not specific structure
- **Structured schema**: Guarantees exact structure via Pydantic
- **Use `.with_structured_output()`**: For schema-enforced responses
- **Mention "JSON" in prompts**: Required for JSON mode
- **Provider handling varies**: LangChain abstracts differences
- **Prefer structured schemas**: For reliable programmatic processing

## Additional Resources

- [OpenAI Response Format](https://platform.openai.com/docs/guides/structured-outputs)
- [LangChain Structured Output Guide](https://docs.langchain.com/oss/python/langchain/how-to/structured_output)
- [Pydantic Models](https://docs.pydantic.dev/latest/)
