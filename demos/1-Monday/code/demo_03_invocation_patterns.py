"""
Demo 03: Invocation Patterns - invoke, batch, stream

This demo shows trainees how to:
1. Use .invoke() for single synchronous requests
2. Use .batch() for parallel processing
3. Use .stream() for real-time output
4. Understand async methods for non-blocking operations

Learning Objectives:
- Master the three core invocation patterns
- Know when to use each pattern
- Understand performance implications

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/models
Last Verified: January 2026

References:
- Written Content: readings/1-Monday/06-model-invocation-patterns.md
"""

import os
import time
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain import init_chat_model

# Initialize model for all demos
model = init_chat_model("openai:gpt-4o-mini")

# ============================================================================
# PART 1: .invoke() - Single Synchronous Request
# ============================================================================

print("=" * 70)
print("PART 1: .invoke() - Single Synchronous Request")
print("=" * 70)

print("""
.invoke() is the basic building block:
- Sends one request
- Waits for complete response
- Returns full result

Use when:
- You need the complete response before continuing
- Processing single user inputs
- Building simple Q&A interfaces
""")

print("\n[Step 1] Basic invoke usage...")

# Simple string invoke
start_time = time.time()
response = model.invoke("What is the capital of France? Answer in one sentence.")
elapsed = time.time() - start_time

print(f"  Response: {response.content}")
print(f"  Time: {elapsed:.2f} seconds")

# Invoke with message format
print("\n[Step 2] Invoke with message format...")

messages = [
    {"role": "system", "content": "You are a helpful geography assistant."},
    {"role": "user", "content": "What is the capital of Japan?"}
]

response = model.invoke(messages)
print(f"  Response: {response.content}")

# ============================================================================
# PART 2: .batch() - Parallel Processing
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: .batch() - Parallel Processing")
print("=" * 70)

print("""
.batch() processes multiple inputs in parallel:
- Sends multiple requests concurrently
- Returns list of responses
- Much faster than sequential .invoke() calls

Use when:
- Processing multiple independent requests
- Document analysis pipelines
- Bulk data processing
""")

print("\n[Step 3] Compare sequential vs batch processing...")

questions = [
    "What is the capital of France?",
    "What is the capital of Germany?",
    "What is the capital of Italy?",
    "What is the capital of Spain?",
    "What is the capital of Portugal?"
]

# Sequential approach (slow)
print("\n  Sequential .invoke() calls:")
start_time = time.time()
sequential_results = []
for q in questions:
    r = model.invoke(q)
    sequential_results.append(r.content)
sequential_time = time.time() - start_time
print(f"    Time: {sequential_time:.2f} seconds")

# Batch approach (fast)
print("\n  Single .batch() call:")
start_time = time.time()
batch_results = model.batch(questions)
batch_time = time.time() - start_time
print(f"    Time: {batch_time:.2f} seconds")

print(f"\n  Speedup: {sequential_time/batch_time:.1f}x faster with batch!")

# Show results
print("\n  Results:")
for q, r in zip(questions, batch_results):
    answer = r.content.split(".")[0] if "." in r.content else r.content[:50]
    print(f"    Q: {q}")
    print(f"    A: {answer}")
    print()

# ============================================================================
# PART 3: .stream() - Real-Time Output
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: .stream() - Real-Time Output")
print("=" * 70)

print("""
.stream() yields tokens as they're generated:
- Returns an iterator of chunks
- Shows output in real-time
- Great for chatbot UX

Use when:
- Building chat interfaces
- Long responses where users want progress
- Creating "typing" effects
""")

print("\n[Step 4] Streaming output demonstration...")
print("\n  Streaming response:")
print("  ", end="", flush=True)

for chunk in model.stream("Tell me a very short story about a robot. Keep it under 50 words."):
    print(chunk.content, end="", flush=True)

print("\n")

# Compare with invoke for the same prompt
print("\n[Step 5] Time to first token comparison...")

prompt = "Write a haiku about programming."

# With invoke - must wait for complete response
print("\n  With .invoke():")
start_time = time.time()
response = model.invoke(prompt)
total_time = time.time() - start_time
print(f"    Time to complete response: {total_time:.2f}s")
print(f"    Response: {response.content}")

# With stream - first token comes quickly
print("\n  With .stream():")
start_time = time.time()
first_chunk = True
full_response = ""
for chunk in model.stream(prompt):
    if first_chunk:
        first_token_time = time.time() - start_time
        print(f"    Time to first token: {first_token_time:.2f}s")
        first_chunk = False
    full_response += chunk.content
total_stream_time = time.time() - start_time
print(f"    Time to complete: {total_stream_time:.2f}s")
print(f"    Response: {full_response}")

# ============================================================================
# PART 4: Async Methods
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Async Methods (.ainvoke(), .abatch())")
print("=" * 70)

print("""
Async methods for non-blocking operations:
- .ainvoke() - Async single request
- .abatch() - Async batch processing
- .astream() - Async streaming

Use when:
- Building web servers (FastAPI, etc.)
- Need to handle multiple users concurrently
- Want to avoid blocking the event loop
""")

async def async_demo():
    """Demonstrate async invocation patterns."""
    print("\n[Step 6] Async invocation...")
    
    # ainvoke - single async request
    response = await model.ainvoke("What color is the sky? One word.")
    print(f"  ainvoke response: {response.content}")
    
    # abatch - parallel async requests
    print("\n[Step 7] Async batch processing...")
    questions = [
        "What is 2+2?",
        "What is 3+3?",
        "What is 4+4?"
    ]
    
    start_time = time.time()
    responses = await model.abatch(questions)
    elapsed = time.time() - start_time
    
    for q, r in zip(questions, responses):
        print(f"  Q: {q} -> A: {r.content.strip()}")
    print(f"  Time: {elapsed:.2f}s")

# Run async demo
print("\n  Running async examples...")
asyncio.run(async_demo())

# ============================================================================
# PART 5: Pattern Selection Guide
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: When to Use Each Pattern")
print("=" * 70)

print("""
┌────────────────┬─────────────────────────────────────────────────┐
│ Pattern        │ Best For                                        │
├────────────────┼─────────────────────────────────────────────────┤
│ .invoke()      │ Single requests, simple Q&A, need full response │
│ .batch()       │ Multiple independent requests, bulk processing  │
│ .stream()      │ Chat UX, long responses, progress indication    │
│ .ainvoke()     │ Web servers, async applications                 │
│ .abatch()      │ Async + multiple requests                       │
└────────────────┴─────────────────────────────────────────────────┘

Performance Tips:
1. Use .batch() instead of multiple .invoke() calls - 3-5x faster
2. Use .stream() for responses > 100 tokens - better UX
3. Use async methods in FastAPI/async frameworks
4. Start simple with .invoke(), optimize later
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: Invocation Patterns")
print("=" * 70)

print("""
Key Takeaways:

1. .invoke() - Basic synchronous call, waits for full response
2. .batch() - Parallel processing, much faster for multiple inputs
3. .stream() - Real-time output, great for chat interfaces
4. Async methods - For non-blocking web applications

Remember:
- All methods are available on any model from init_chat_model()
- Same interface works across all providers
- Choose based on your use case, not habit!
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The timing difference between sequential and batch
2. How streaming creates a "typing" effect
3. The consistent interface across all patterns

Live Demo Tips:
- Use print() with flush=True for streaming
- Show the terminal during stream - students love watching it type
- Run batch comparison multiple times - results are consistent

Discussion Questions:
- "When building a chatbot, which pattern would you use?"
- "How would you process 1000 documents efficiently?"
- "Why does batch have better performance?"

Common Mistakes to Address:
- Forgetting to iterate over stream results
- Using invoke in a loop instead of batch
- Not handling async properly (forgetting await)
""")

print("=" * 70)
