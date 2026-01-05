# Model Invocation Patterns

## Learning Objectives
- Understand and use `.invoke()` for single requests
- Use `.batch()` for processing multiple inputs efficiently
- Implement `.stream()` for real-time response streaming
- Apply async methods (`.ainvoke()`, `.abatch()`) for concurrent operations
- Choose the right invocation pattern for each use case

## Why This Matters

How you call a model matters just as much as which model you choose. The wrong invocation pattern can make your application feel sluggish to users or waste resources processing requests sequentially when they could run in parallel.

In our **"From Basics to Production"** journey, mastering these patterns ensures your agents are responsive, efficient, and scalable.

## The Concept

### The Four Invocation Methods

LangChain models support four core methods:

| Method | Use Case | Blocks? | Returns |
|--------|----------|---------|---------|
| `.invoke()` | Single synchronous request | Yes | Complete response |
| `.batch()` | Multiple requests in parallel | Yes | List of responses |
| `.stream()` | Real-time token streaming | No* | Iterator of chunks |
| `.ainvoke()` | Async single request | No | Awaitable response |

*`.stream()` blocks until iteration begins, then yields chunks

### `.invoke()` - Single Requests

The most common pattern. Send a request, wait for the complete response:

```python
from langchain import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

# Invoke with a list of messages
response = model.invoke([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
])

print(response.content)  # "The capital of France is Paris."
```

**When to use:**
- Simple Q&A interactions
- Single-turn operations
- When you need the complete response before proceeding

### `.batch()` - Parallel Processing

Process multiple independent requests efficiently:

```python
from langchain import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

# Multiple questions to process
questions = [
    [{"role": "user", "content": "What is 2+2?"}],
    [{"role": "user", "content": "What is 3+3?"}],
    [{"role": "user", "content": "What is 4+4?"}],
]

# Process all at once - much faster than sequential invoke()
responses = model.batch(questions)

for q, r in zip(questions, responses):
    print(f"Q: {q[0]['content']} -> A: {r.content}")
```

**When to use:**
- Processing lists of items (e.g., summarizing multiple documents)
- Generating multiple variations
- Any scenario with independent, parallelizable requests

**Configuration:**
```python
# Control parallelism
responses = model.batch(
    questions,
    config={"max_concurrency": 5}  # Limit concurrent requests
)
```

### `.stream()` - Real-Time Streaming

Get response tokens as they're generated, enabling responsive UIs:

```python
from langchain import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

# Stream the response
print("Response: ", end="")
for chunk in model.stream([{"role": "user", "content": "Tell me a short story."}]):
    print(chunk.content, end="", flush=True)
print()  # Newline at end
```

**Output appears progressively:**
```
Response: Once upon a time, in a small village...
```

**When to use:**
- Chat interfaces where users see text appear in real-time
- Long-form generation where waiting feels too slow
- Any user-facing application where perceived speed matters

### `.ainvoke()` and `.abatch()` - Async Operations

For async/await code patterns:

```python
import asyncio
from langchain import init_chat_model

async def main():
    model = init_chat_model("openai:gpt-4o-mini")
    
    # Async single request
    response = await model.ainvoke([
        {"role": "user", "content": "Hello!"}
    ])
    print(f"Single: {response.content}")
    
    # Async batch
    questions = [
        [{"role": "user", "content": "What is 1+1?"}],
        [{"role": "user", "content": "What is 2+2?"}],
    ]
    responses = await model.abatch(questions)
    for r in responses:
        print(f"Batch: {r.content}")

# Run the async function
asyncio.run(main())
```

**When to use:**
- FastAPI, aiohttp, or other async frameworks
- When you need non-blocking I/O
- High-concurrency applications

### `.astream()` - Async Streaming

```python
import asyncio
from langchain import init_chat_model

async def stream_response():
    model = init_chat_model("openai:gpt-4o-mini")
    
    async for chunk in model.astream([
        {"role": "user", "content": "Count from 1 to 5 slowly."}
    ]):
        print(chunk.content, end="", flush=True)
    print()

asyncio.run(stream_response())
```

### Comparing Performance

For processing 10 questions:

| Approach | Time | Why |
|----------|------|-----|
| 10x `.invoke()` sequentially | ~10 seconds | One at a time |
| 1x `.batch()` | ~2-3 seconds | Parallel processing |
| 10x `.ainvoke()` with `asyncio.gather()` | ~2-3 seconds | Concurrent async |

### Error Handling

```python
from langchain import init_chat_model
from langchain_core.exceptions import OutputParserException

model = init_chat_model("openai:gpt-4o-mini")

try:
    response = model.invoke([{"role": "user", "content": "Hello"}])
    print(response.content)
except Exception as e:
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
```

**Common exceptions:**
- `AuthenticationError`: Invalid API key
- `RateLimitError`: Too many requests
- `APIConnectionError`: Network issues
- `Timeout`: Request took too long

### Choosing the Right Pattern

```
                    How many requests?
                          │
              ┌───────────┴───────────┐
              │                       │
            Single                 Multiple
              │                       │
      Need real-time?           Use .batch()
              │
       ┌──────┴──────┐
      Yes            No
       │              │
   .stream()      .invoke()
   
   
              Are you in async code?
                       │
              ┌────────┴────────┐
             Yes               No
              │                 │
       Use .ainvoke()    Use .invoke()
       or .astream()     or .stream()
```

## Code Example

```python
"""
Model Invocation Patterns Demo
LangChain Version: v1.0+
"""
import asyncio
import time
from langchain import init_chat_model

model = init_chat_model("openai:gpt-4o-mini", temperature=0)

# ========================================
# Pattern 1: invoke() - Simple single call
# ========================================
print("=== invoke() ===")
response = model.invoke([{"role": "user", "content": "What is 5+5?"}])
print(f"Result: {response.content}\n")

# ========================================
# Pattern 2: batch() - Parallel processing
# ========================================
print("=== batch() ===")
questions = [
    [{"role": "user", "content": f"What is {i}+{i}?"}]
    for i in range(1, 6)
]

start = time.time()
responses = model.batch(questions)
print(f"Processed {len(responses)} questions in {time.time()-start:.2f}s")
for i, r in enumerate(responses, 1):
    print(f"  {i}+{i} = {r.content}")
print()

# ========================================
# Pattern 3: stream() - Real-time output
# ========================================
print("=== stream() ===")
print("Streaming: ", end="")
for chunk in model.stream([
    {"role": "user", "content": "Count from 1 to 5, one number per line."}
]):
    print(chunk.content, end="", flush=True)
print("\n")

# ========================================
# Pattern 4: Async patterns
# ========================================
print("=== async patterns ===")

async def demo_async():
    # ainvoke - single async request
    response = await model.ainvoke([{"role": "user", "content": "Hello!"}])
    print(f"ainvoke result: {response.content}")
    
    # Multiple concurrent requests with gather
    tasks = [
        model.ainvoke([{"role": "user", "content": f"Say '{word}'"}])
        for word in ["alpha", "beta", "gamma"]
    ]
    
    start = time.time()
    results = await asyncio.gather(*tasks)
    print(f"3 concurrent calls in {time.time()-start:.2f}s")
    for r in results:
        print(f"  {r.content}")

asyncio.run(demo_async())
```

## Key Takeaways

- **`.invoke()`**: One request, wait for complete response
- **`.batch()`**: Multiple requests in parallel—much faster than sequential
- **`.stream()`**: Real-time token output for responsive UIs
- **Async methods**: Use in async frameworks (FastAPI, etc.)
- **Choose based on use case**: single vs. multiple, blocking vs. non-blocking
- **Batch is your friend**: Always prefer `.batch()` over loops of `.invoke()`

## Additional Resources

- [LangChain Runnable Interface](https://docs.langchain.com/oss/python/langchain/concepts/runnables)
- [Streaming in LangChain](https://docs.langchain.com/oss/python/langchain/how-to/streaming)
- [Async in LangChain](https://docs.langchain.com/oss/python/langchain/how-to/async)
