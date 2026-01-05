"""
Exercise 01: AWS Bedrock Connection - Starter Code

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain

Configure AWS Bedrock credentials and verify model connectivity.

Instructions:
1. Implement each TODO function
2. Run this file to test your implementations
3. Check the expected output in the exercise guide
"""

import os
import time
from typing import Optional, Dict, Any

# ============================================================================
# IMPORTS - Add any additional imports you need
# ============================================================================

# TODO: Import boto3 for AWS credential verification
# import boto3

# TODO: Import init_chat_model from langchain
# from langchain import init_chat_model


# ============================================================================
# CONFIGURATION
# ============================================================================

# Default Bedrock model to test
# Format: bedrock:anthropic.claude-3-haiku-20240307-v1:0
DEFAULT_MODEL = "bedrock:anthropic.claude-3-haiku-20240307-v1:0"

# Expected AWS region for Bedrock
EXPECTED_REGION = "us-east-1"


# ============================================================================
# TODO: IMPLEMENT THESE FUNCTIONS
# ============================================================================

def verify_aws_credentials() -> Dict[str, Any]:
    """
    Verify that AWS credentials are properly configured.
    
    Tasks:
    - Check that AWS credentials are available
    - Verify the region is set correctly for Bedrock
    - Return status information
    
    Returns:
        Dict with keys:
        - 'success': bool
        - 'region': str or None
        - 'message': str describing the status
        
    Example:
        {'success': True, 'region': 'us-east-1', 'message': 'Credentials found'}
    """
    # TODO: Implement this function
    # Hint: Use boto3.Session() to check credentials
    # session = boto3.Session()
    # credentials = session.get_credentials()
    
    pass  # Remove this and add your implementation


def initialize_bedrock_model(model_string: str = DEFAULT_MODEL):
    """
    Initialize a Bedrock model using init_chat_model().
    
    Tasks:
    - Use init_chat_model() with the provided model string
    - Handle any initialization errors
    - Return the model instance or None on failure
    
    Args:
        model_string: Provider string in format "bedrock:model-id"
        
    Returns:
        Initialized model instance or None if initialization fails
        
    Example:
        model = initialize_bedrock_model("bedrock:anthropic.claude-3-haiku-20240307-v1:0")
    """
    # TODO: Implement this function
    # Hint: from langchain import init_chat_model
    # model = init_chat_model(model_string)
    
    pass  # Remove this and add your implementation


def test_model_connection(model) -> Dict[str, Any]:
    """
    Test the model connection with a simple invocation.
    
    Tasks:
    - Send a simple test message to the model
    - Measure the response time
    - Return the result and timing information
    
    Args:
        model: Initialized LangChain model instance
        
    Returns:
        Dict with keys:
        - 'success': bool
        - 'response': str (the model's response)
        - 'response_time': float (seconds)
        - 'message': str (status message)
    """
    # TODO: Implement this function
    # Hint: Use model.invoke() with a simple message
    # Hint: Use time.perf_counter() for timing
    
    test_message = "Say 'Hello, connection successful!' and nothing else."
    
    pass  # Remove this and add your implementation


def diagnose_connection_issues() -> None:
    """
    Diagnose common connection issues and provide guidance.
    
    Tasks:
    - Check for missing environment variables
    - Verify AWS CLI configuration
    - Test network connectivity to AWS
    - Print helpful error messages with remediation steps
    
    This function should print diagnostic information directly.
    """
    # TODO: Implement this function
    # Hint: Check for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    # Hint: Check for ~/.aws/credentials file
    
    pass  # Remove this and add your implementation


# ============================================================================
# TEST HARNESS (DO NOT MODIFY)
# ============================================================================

def run_connection_test():
    """Run the complete Bedrock connection test suite."""
    print("=" * 50)
    print("AWS Bedrock Connection Test")
    print("=" * 50)
    print()
    
    all_passed = True
    
    # Step 1: Verify AWS credentials
    print("[INFO] Checking AWS credentials...")
    cred_result = verify_aws_credentials()
    
    if cred_result is None:
        print("[ERROR] verify_aws_credentials() returned None - not implemented")
        all_passed = False
    elif cred_result.get('success'):
        print(f"[OK] {cred_result.get('message')} (region: {cred_result.get('region')})")
    else:
        print(f"[ERROR] {cred_result.get('message')}")
        print("[INFO] Running diagnostics...")
        diagnose_connection_issues()
        all_passed = False
    
    print()
    
    # Step 2: Initialize model
    print("[INFO] Initializing Bedrock model...")
    model = initialize_bedrock_model()
    
    if model is None:
        print("[ERROR] Model initialization failed - not implemented or error occurred")
        all_passed = False
    else:
        print(f"[OK] Model initialized: {DEFAULT_MODEL}")
    
    print()
    
    # Step 3: Test connection
    if model is not None:
        print("[INFO] Testing model connection...")
        test_result = test_model_connection(model)
        
        if test_result is None:
            print("[ERROR] test_model_connection() returned None - not implemented")
            all_passed = False
        elif test_result.get('success'):
            print(f"[OK] Response received in {test_result.get('response_time', 0):.2f}s")
            print(f"Response: {test_result.get('response', 'N/A')}")
        else:
            print(f"[ERROR] {test_result.get('message')}")
            all_passed = False
    
    print()
    print("=" * 50)
    if all_passed:
        print("[OK] Connection Test Complete - All checks passed!")
    else:
        print("[INFO] Some checks failed. Review the errors above.")
    print("=" * 50)


if __name__ == "__main__":
    run_connection_test()
