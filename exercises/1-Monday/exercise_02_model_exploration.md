# Exercise 02: Model Exploration

## Overview

Now that you have AWS Bedrock connected, it's time to explore LangChain's unified model interface. You'll learn how `init_chat_model()` provides a consistent API across different providers, making it easy to switch between models.

## Learning Objectives

- Initialize models from multiple providers using `init_chat_model()`
- Understand the provider string format (`provider:model-name`)
- Compare `.invoke()`, `.batch()`, and `.stream()` methods
- Analyze differences in model responses and behavior

## The Scenario

Your team is evaluating different LLM providers for a new project. They need you to:

1. Set up connections to OpenAI, Anthropic (via Bedrock), and other available models
2. Compare response quality and speed
3. Document the differences for the team's decision-making

## Your Tasks

### Task 1: Multi-Provider Setup (20 min)

Implement `setup_models()` in the starter code:
- Initialize at least 3 different models using `init_chat_model()`
- Use the provider string format: `"provider:model-name"`
- Return a dictionary of model instances

Provider string examples:
- `"openai:gpt-4o-mini"`
- `"anthropic:claude-3-haiku-20240307"`
- `"bedrock:anthropic.claude-3-haiku-20240307-v1:0"`

### Task 2: Invoke Comparison (20 min)

Implement `compare_invoke()`:
- Send the same prompt to each model using `.invoke()`
- Measure response time for each
- Format and display results side-by-side

> **Hint**: Use `time.perf_counter()` for precise timing.

### Task 3: Batch Processing (20 min)

Implement `test_batch_processing()`:
- Create a list of 3-5 prompts
- Process them using `.batch()` on each model
- Compare throughput (prompts/second)

### Task 4: Streaming Comparison (15 min)

Implement `compare_streaming()`:
- Stream a response from each model using `.stream()`
- Measure time-to-first-token
- Display streaming output in real-time

## Definition of Done

- [_] At least 3 models initialized successfully
- [_] Invoke comparison shows response times
- [_] Batch processing reports throughput metrics
- [_] Streaming demonstrates real-time output
- [_] Summary table compares all methods

## Testing Your Solution

```bash
cd exercises/1-Monday/starter_code
python exercise_02_starter.py
```

Expected output format:
```
=== Model Exploration ===

[INFO] Initializing models...
[OK] 3 models ready

=== Invoke Comparison ===
Prompt: "Explain what an API is in one sentence."

| Model              | Time   | Response                              |
|--------------------|--------|---------------------------------------|
| openai:gpt-4o-mini | 0.82s  | An API is a set of rules that...      |
| anthropic:claude   | 1.14s  | An API (Application Programming...    |
| bedrock:claude     | 1.23s  | An API is the interface through...    |

=== Batch Processing ===
Processing 5 prompts...

| Model              | Total Time | Throughput      |
|--------------------|------------|-----------------|
| openai:gpt-4o-mini | 2.34s      | 2.14 prompts/s  |
| anthropic:claude   | 3.12s      | 1.60 prompts/s  |

=== Streaming Test ===
Model: openai:gpt-4o-mini
Time to first token: 0.23s
[streaming output...]

=== Exploration Complete ===
```

## Key Patterns

```python
from langchain import init_chat_model

# Provider string format
model = init_chat_model("provider:model-name")

# Invoke - single message
response = model.invoke("Hello")
print(response.content)

# Batch - multiple messages
responses = model.batch(["Hi", "Hello", "Hey"])
for r in responses:
    print(r.content)

# Stream - real-time output
for chunk in model.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

## Stretch Goals (Optional)

1. Add async versions using `.ainvoke()` and `.abatch()`
2. Compare token usage across providers
3. Test with different temperature settings
4. Create a cost comparison based on pricing
