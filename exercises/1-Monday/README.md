# Monday: AWS Bedrock & LangChain v1.0 Orientation

## Exercise Schedule

| Exercise | Type | Duration | Prerequisites |
|----------|------|----------|---------------|
| 01: Bedrock Connection | Implementation | 45-60 min | Reading 01, 05, Demo 02 |
| 02: Model Exploration | Implementation | 60-75 min | Reading 04-06, Demo 03 |

## Learning Objectives

By completing these exercises, you will:
- Configure AWS Bedrock credentials for LangChain integration
- Use `init_chat_model()` to initialize models from different providers
- Compare model behaviors using `.invoke()`, `.batch()`, and `.stream()` methods
- Understand the LangChain v1.0 model abstraction layer

## Before You Begin

1. **Complete the readings** in `readings/1-Monday/`
2. **Watch/run demos** in `demos/1-Monday/code/`
3. **AWS Setup**: Ensure you have:
   - AWS account with Bedrock access
   - IAM credentials configured (`~/.aws/credentials`)
   - Model access enabled in AWS Bedrock console
4. Install dependencies:
   ```bash
   pip install langchain langchain-aws langchain-openai langchain-anthropic
   ```

## Exercises

### Exercise 01: Bedrock Connection (Implementation)
See [exercise_01_bedrock_connection.md](exercise_01_bedrock_connection.md)
Starter code: `starter_code/exercise_01_starter.py`

Configure AWS Bedrock credentials and verify model access using `init_chat_model()`.

### Exercise 02: Model Exploration (Implementation)
See [exercise_02_model_exploration.md](exercise_02_model_exploration.md)
Starter code: `starter_code/exercise_02_starter.py`

Explore different model providers, compare their responses, and experiment with invocation patterns.

## Estimated Time
**Total: 2-2.5 hours**

## Key v1.0 Patterns to Practice

```python
# Model initialization (v1.0 way)
from langchain import init_chat_model
model = init_chat_model("openai:gpt-4o-mini")

# Invocation patterns
result = model.invoke("Hello")           # Single message
results = model.batch(["Hi", "Hello"])   # Multiple messages
for chunk in model.stream("Hello"):      # Streaming
    print(chunk.content, end="")
```

> **Warning**: Do NOT use LCEL pipe operators (`|`) - they are deprecated in v1.0.
