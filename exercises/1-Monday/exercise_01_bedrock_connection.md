# Exercise 01: AWS Bedrock Connection

## Overview

You're joining a team that uses AWS Bedrock for their LLM infrastructure. Your first task is to verify that your development environment can connect to Bedrock models and make successful API calls using LangChain v1.0.

## Learning Objectives

- Configure AWS credentials for Bedrock access
- Use `init_chat_model()` with the Bedrock provider
- Verify model connectivity with basic invocations
- Handle common connection errors gracefully

## The Scenario

The team uses Claude models through AWS Bedrock. Before you can contribute to the codebase, you need to:

1. Set up your AWS credentials
2. Verify Bedrock model access
3. Test the connection with LangChain's `init_chat_model()`

## Your Tasks

### Task 1: Credential Verification (15 min)

Implement `verify_aws_credentials()` in the starter code:
- Check that AWS credentials are properly configured
- Verify the correct region is set for Bedrock
- Return a status message indicating success or failure

> **Hint**: Use `boto3.Session()` to check credential availability.

### Task 2: Model Initialization (15 min)

Implement `initialize_bedrock_model()`:
- Use `init_chat_model()` with the Bedrock provider string
- Configure the model with appropriate parameters
- Handle initialization errors gracefully

> **Hint**: The provider string format is `"bedrock:anthropic.claude-3-haiku-20240307-v1:0"`

### Task 3: Connection Test (15 min)

Implement `test_model_connection()`:
- Send a simple test message to the model
- Verify the response is received
- Measure and report the response time

### Task 4: Error Handling (15 min)

Implement `diagnose_connection_issues()`:
- Test for common failure scenarios
- Provide helpful error messages for each case
- Suggest remediation steps

## Definition of Done

- [_] AWS credentials verified successfully
- [_] Bedrock model initializes without errors
- [_] Test invocation returns valid response
- [_] Error handling provides actionable feedback
- [_] Console shows connection status summary

## Testing Your Solution

```bash
cd exercises/1-Monday/starter_code
python exercise_01_starter.py
```

Expected output format:
```
=== AWS Bedrock Connection Test ===

[INFO] Checking AWS credentials...
[OK] AWS credentials found (region: us-east-1)

[INFO] Initializing Bedrock model...
[OK] Model initialized: bedrock:anthropic.claude-3-haiku-20240307-v1:0

[INFO] Testing model connection...
[OK] Response received in 1.23s
Response: Hello! How can I help you today?

=== Connection Test Complete ===
```

## Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Missing credentials | `NoCredentialsError` | Run `aws configure` |
| Wrong region | `EndpointConnectionError` | Check Bedrock availability in region |
| Model not enabled | `AccessDeniedException` | Enable model in Bedrock console |
| Invalid model ID | `ValidationException` | Verify model ID format |

## Stretch Goals (Optional)

1. Add support for multiple AWS profiles
2. Implement automatic region detection
3. Create a connection health dashboard
