"""
Demo 02: init_chat_model() - The LangChain v1.0 Standard

This demo shows trainees how to:
1. Initialize models using the init_chat_model() helper
2. Use the provider string format (provider:model-name)
3. Configure model parameters
4. Switch between providers with minimal code changes

Learning Objectives:
- Understand init_chat_model() as the v1.0 standard
- Master the provider string format
- Learn common configuration options

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/models
Last Verified: January 2026

References:
- Written Content: readings/1-Monday/05-init-chat-model-helper.md
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# PART 1: Basic Model Initialization
# ============================================================================

print("=" * 70)
print("PART 1: Basic Model Initialization with init_chat_model()")
print("=" * 70)

from langchain import init_chat_model

# v1.0 Standard: Use init_chat_model() with provider string
print("\n[Step 1] Initializing model with provider string...")

# The provider string format: "provider:model-name"
model = init_chat_model("openai:gpt-4o-mini")

print("Model initialized successfully!")
print(f"  Type: {type(model).__name__}")

# Simple invocation
print("\n[Step 2] Testing basic invocation...")
response = model.invoke("Say 'Hello, LangChain v1.0!' in one sentence.")
print(f"  Response: {response.content}")

# ============================================================================
# PART 2: Provider String Format Examples
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Provider String Format Examples")
print("=" * 70)

print("""
Provider String Format: "provider:model-name"

Examples:
  OpenAI:     "openai:gpt-4o-mini"
              "openai:gpt-4o"
              "openai:gpt-3.5-turbo"
  
  Anthropic:  "anthropic:claude-3-5-sonnet-20241022"
              "anthropic:claude-3-haiku-20240307"
  
  Bedrock:    "bedrock:anthropic.claude-3-sonnet-20240229-v1:0"
              "bedrock:amazon.titan-text-express-v1"
  
  Google:     "google_genai:gemini-1.5-flash"
              "google_genai:gemini-1.5-pro"
""")

# Demonstrate switching providers
print("[Step 3] Demonstrating provider switching...")

providers_to_try = [
    ("openai:gpt-4o-mini", "OpenAI GPT-4o Mini"),
    # Uncomment if you have Anthropic credentials:
    # ("anthropic:claude-3-haiku-20240307", "Anthropic Claude 3 Haiku"),
]

for provider_string, display_name in providers_to_try:
    try:
        print(f"\n  Testing {display_name}...")
        test_model = init_chat_model(provider_string)
        test_response = test_model.invoke("What's 2+2? Answer in one word.")
        print(f"    ✓ Response: {test_response.content.strip()}")
    except Exception as e:
        print(f"    ✗ Error: {e}")

# ============================================================================
# PART 3: Configuration Options
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Configuration Options")
print("=" * 70)

print("\n[Step 4] Configuring model parameters...")

# Temperature controls randomness (0 = deterministic, 1 = creative)
model_deterministic = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.0  # Deterministic responses
)

model_creative = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=1.0  # More creative/random
)

prompt = "Give me a one-word color."

print("\n  Temperature = 0.0 (deterministic):")
for i in range(3):
    resp = model_deterministic.invoke(prompt)
    print(f"    Run {i+1}: {resp.content.strip()}")

print("\n  Temperature = 1.0 (creative):")
for i in range(3):
    resp = model_creative.invoke(prompt)
    print(f"    Run {i+1}: {resp.content.strip()}")

# ============================================================================
# PART 4: Max Tokens Configuration
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Max Tokens Configuration")
print("=" * 70)

print("\n[Step 5] Limiting response length with max_tokens...")

model_short = init_chat_model(
    "openai:gpt-4o-mini",
    max_tokens=20  # Limit response to ~20 tokens
)

model_long = init_chat_model(
    "openai:gpt-4o-mini",
    max_tokens=100  # Allow longer responses
)

prompt = "Explain what machine learning is."

print(f"\n  max_tokens=20:")
short_response = model_short.invoke(prompt)
print(f"    {short_response.content}")

print(f"\n  max_tokens=100:")
long_response = model_long.invoke(prompt)
print(f"    {long_response.content}")

# ============================================================================
# PART 5: What NOT to Do (Deprecated Patterns)
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: Deprecated Patterns to AVOID")
print("=" * 70)

print("""
❌ WRONG - Direct class instantiation (deprecated in v1.0):
   from langchain_openai import ChatOpenAI
   model = ChatOpenAI(model="gpt-4o-mini")

❌ WRONG - LCEL chains (deprecated and removed):
   chain = prompt | model | output_parser

✅ CORRECT - init_chat_model() with provider string:
   from langchain import init_chat_model
   model = init_chat_model("openai:gpt-4o-mini")

Why init_chat_model() is better:
1. Unified interface across all providers
2. Simpler syntax - one function for everything
3. Consistent parameter handling
4. Future-proof for new providers
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: init_chat_model()")
print("=" * 70)

print("""
Key Takeaways:

1. Use init_chat_model() for all model initialization in v1.0
2. Provider string format: "provider:model-name"
3. Common parameters:
   - temperature: 0.0 (deterministic) to 1.0 (creative)
   - max_tokens: Limit response length
4. Easy to switch providers - just change the string!
5. Avoid deprecated patterns (direct imports, LCEL)
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The simplicity of one-line initialization
2. How temperature affects response variety
3. Run the deterministic test multiple times - same answer!
4. Emphasize provider string format memorization

Discussion Questions:
- "When would you use temperature=0 vs temperature=1?"
- "Why is a unified interface valuable for production code?"

If API errors occur:
- Check OPENAI_API_KEY environment variable
- Verify API quota hasn't been exceeded
- Try a different provider if available
""")

print("=" * 70)
