# Introduction to Models (LLMs)

## Learning Objectives
- Understand what LLMs are and how they work at a high level
- Distinguish between chat models and completion models
- Identify key model capabilities and how to choose the right model
- Understand the LangChain model abstraction

## Why This Matters

Models are the "brains" of every AI application. Choosing the right model—and understanding its capabilities and limitations—is fundamental to building effective agents. In our **"From Basics to Production"** journey, models are the core component that enables reasoning, tool calling, and natural language understanding.

## The Concept

### What is a Large Language Model (LLM)?

A Large Language Model is a neural network trained on massive text datasets to predict the next token (word or word-piece) in a sequence. Through this simple objective, LLMs develop emergent capabilities:

- **Language understanding**: Parsing meaning from text
- **Language generation**: Producing coherent, contextual responses
- **Reasoning**: Following logical steps to solve problems
- **In-context learning**: Adapting behavior based on examples in the prompt

```
Input Tokens → [LLM] → Output Tokens
"What is 2+2?"  →  "The answer is 4."
```

### Chat Models vs. Completion Models

LangChain distinguishes between two types of language models:

#### Completion Models (Legacy)
- Take raw text as input
- Return raw text as output
- Example: Original GPT-3 (`text-davinci-003`)

```python
# Completion model (legacy)
input_text = "The capital of France is"
output = "Paris, which is known for..."
```

#### Chat Models (Modern)
- Take a list of messages with roles
- Return a message with role and content
- Support system prompts, multi-turn conversations
- Example: GPT-4o, Claude 3.5 Sonnet

```python
# Chat model (current standard)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
response = {"role": "assistant", "content": "The capital of France is Paris."}
```

**For LangChain v1.0**: Always use chat models. Completion models are deprecated.

### Model Capabilities

Different models have different capabilities. Key factors to consider:

| Capability | Description | Examples |
|------------|-------------|----------|
| **Context Window** | Maximum tokens in input + output | 4K, 128K, 200K tokens |
| **Tool Calling** | Native support for function calling | GPT-4, Claude 3, Llama 3.1 |
| **Vision** | Ability to process images | GPT-4o, Claude 3.5, Llama 3.2 Vision |
| **Reasoning** | Complex multi-step problem solving | o1, Claude 3.5 Sonnet |
| **Speed** | Response latency | Haiku (fast) vs Opus (slower) |
| **Cost** | Price per token | Varies by 100x between models |

### Choosing the Right Model

A decision framework:

```
                   Is speed critical?
                         │
              ┌──────────┴──────────┐
              ▼                      ▼
             Yes                    No
              │                      │
        Use smaller/faster     Is reasoning complex?
         (Haiku, GPT-4o-mini)       │
                           ┌────────┴────────┐
                           ▼                  ▼
                          Yes                No
                           │                  │
                     Use powerful         Use balanced
                  (Claude 3.5 Sonnet,    (GPT-4o-mini,
                       o1-mini)         Claude 3 Haiku)
```

**General Recommendations:**
- **Development/Testing**: GPT-4o-mini or Claude 3 Haiku (fast, cheap)
- **Production (standard)**: GPT-4o or Claude 3.5 Sonnet (balanced)
- **Complex reasoning**: Claude 3.5 Sonnet or o1-mini (most capable)
- **Cost-sensitive at scale**: Llama 3.1 70B via Bedrock (good value)

### LangChain Model Abstraction

LangChain provides a unified interface across all model providers:

```python
from langchain.chat_models import init_chat_model

# All models have the same interface
openai_model = init_chat_model("openai:gpt-4o-mini")
anthropic_model = init_chat_model("anthropic:claude-3-5-sonnet-20241022")
bedrock_model = init_chat_model("bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0")

# Same methods work for all:
result = openai_model.invoke([{"role": "user", "content": "Hello"}])
result = anthropic_model.invoke([{"role": "user", "content": "Hello"}])
result = bedrock_model.invoke([{"role": "user", "content": "Hello"}])
```

This abstraction means you can:
- Switch providers without changing code
- A/B test different models
- Fall back to alternative providers if one fails

### Message Types

Chat models work with structured messages:

| Role | Purpose | Example |
|------|---------|---------|
| `system` | Set behavior, provide context | "You are a helpful coding assistant." |
| `user` | User input | "Write a Python function..." |
| `assistant` | Model's previous responses | "Here's a function that..." |
| `tool` | Tool execution results | "The weather is 72°F" |

```python
messages = [
    {"role": "system", "content": "You are a math tutor."},
    {"role": "user", "content": "What is 15% of 80?"},
    {"role": "assistant", "content": "15% of 80 is 12."},
    {"role": "user", "content": "How did you calculate that?"},
]
```

### Temperature and Generation Parameters

Models have configuration options that affect output:

| Parameter | Effect | Range |
|-----------|--------|-------|
| `temperature` | Randomness/creativity | 0.0 (deterministic) to 2.0 (very random) |
| `max_tokens` | Maximum output length | Depends on model |
| `top_p` | Nucleus sampling (alternative to temperature) | 0.0 to 1.0 |

```python
from langchain import init_chat_model

model = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.0,  # Deterministic output
    max_tokens=500    # Limit response length
)
```

**Guidelines:**
- `temperature=0`: Best for factual/structured output
- `temperature=0.7`: Good balance for creative tasks
- `temperature=1.0+`: For brainstorming, varied outputs

## Code Example

```python
"""
Exploring Models in LangChain v1.0
LangChain Version: v1.0+
"""
from langchain import init_chat_model

# Initialize a model with configuration
model = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.0  # Deterministic for consistent results
)

# Simple invocation with messages
response = model.invoke([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are the three primary colors?"}
])

# Access the response content
print(f"Response: {response.content}")
print(f"Model: {response.response_metadata.get('model_name', 'Unknown')}")

# Multi-turn conversation
conversation = [
    {"role": "system", "content": "You are a history teacher."},
    {"role": "user", "content": "When did World War 2 end?"},
]

response1 = model.invoke(conversation)
print(f"\nFirst response: {response1.content}")

# Add the response and ask a follow-up
conversation.append({"role": "assistant", "content": response1.content})
conversation.append({"role": "user", "content": "What treaty was signed?"})

response2 = model.invoke(conversation)
print(f"Follow-up response: {response2.content}")
```

## Key Takeaways

- **LLMs predict tokens** but develop emergent reasoning capabilities
- **Use chat models** (not completion models) in LangChain v1.0
- **Models vary in capabilities**: context size, speed, reasoning, cost
- **LangChain abstracts providers**: Same interface for OpenAI, Anthropic, Bedrock
- **Messages have roles**: system, user, assistant, tool
- **Temperature controls randomness**: 0 for factual, higher for creative

## Additional Resources

- [LangChain Chat Models](https://docs.langchain.com/oss/python/langchain/concepts/chat_models)
- [OpenAI Model Overview](https://platform.openai.com/docs/models)
- [Anthropic Claude Models](https://docs.anthropic.com/en/docs/about-claude/models)
