# AWS Bedrock Orientation

## Learning Objectives
- Understand what AWS Bedrock is and its role in AI application development
- Identify the foundation models available through Bedrock
- Configure IAM permissions for Bedrock access
- Set up API credentials for LangChain integration

## Why This Matters

As we transition from foundational AI concepts to production-ready agent development, you'll need access to powerful language models. AWS Bedrock provides a managed service that gives you secure, scalable access to top-tier foundation models from providers like Anthropic (Claude), Amazon (Titan), Meta (Llama), and others—all through a unified API.

This matters for our **"From Basics to Production"** journey because Bedrock eliminates the infrastructure complexity of hosting models yourself. You can focus on building intelligent agents rather than managing GPU clusters and model deployments.

## The Concept

### What is AWS Bedrock?

AWS Bedrock is a fully managed service that makes foundation models (FMs) available through an API. Think of it as a "model marketplace" where you can access various AI models without managing any infrastructure.

**Key Benefits:**
- **No infrastructure management**: Amazon handles the servers, scaling, and availability
- **Multiple model providers**: Access Claude, Titan, Llama, and more from a single API
- **Pay-per-use pricing**: Only pay for the tokens you consume
- **Enterprise security**: Integrates with AWS IAM, VPC, and compliance frameworks

### Available Model Providers

| Provider | Models | Best For |
|----------|--------|----------|
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Haiku | Complex reasoning, long context, agent tasks |
| **Amazon** | Titan Text, Titan Embeddings | General tasks, cost-effective embeddings |
| **Meta** | Llama 3.1, Llama 3.2 | Open-weight flexibility, fine-tuning potential |
| **Mistral** | Mistral Large, Mixtral | Efficient inference, multilingual support |
| **Cohere** | Command R+ | Retrieval-augmented generation, enterprise search |

### IAM Permissions Setup

To use Bedrock, your AWS IAM user or role needs specific permissions. Here's the minimum required policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel"
            ],
            "Resource": "*"
        }
    ]
}
```

**Important**: For production environments, restrict the `Resource` field to specific model ARNs rather than using `"*"`.

### Model Access Requests

Before using a model, you must request access in the AWS Console:

1. Navigate to **AWS Bedrock** in the console
2. Select **Model access** from the left menu
3. Click **Manage model access**
4. Select the models you want to use (e.g., Claude 3.5 Sonnet)
5. Click **Request model access**

Some models require accepting terms and conditions. Access is typically granted within minutes.

### API Configuration for LangChain

LangChain integrates with Bedrock through the `langchain-aws` package. You'll need:

1. **AWS Credentials**: Either environment variables or AWS CLI configuration
2. **Region**: The AWS region where you'll access Bedrock

```bash
# Environment variables approach
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

Or configure via AWS CLI:
```bash
aws configure
# Follow prompts to enter access key, secret key, and region
```

### Supported Regions

Bedrock is available in select AWS regions. Common choices include:
- **us-east-1** (N. Virginia) - Most model availability
- **us-west-2** (Oregon) - Good model availability
- **eu-west-1** (Ireland) - For EU data residency

Check AWS documentation for the latest region and model availability matrix.

## Code Example

Here's how to verify your Bedrock access is working:

```python
"""
Verify AWS Bedrock Access
LangChain Version: v1.0+
"""
import boto3

def verify_bedrock_access():
    """Test that Bedrock is accessible with current credentials."""
    # Create Bedrock client
    bedrock = boto3.client(
        service_name='bedrock',
        region_name='us-east-1'  # Adjust to your region
    )
    
    # List available foundation models
    response = bedrock.list_foundation_models()
    
    print("Available Bedrock Models:")
    print("-" * 50)
    for model in response['modelSummaries']:
        print(f"  {model['modelId']}")
        print(f"    Provider: {model['providerName']}")
        print(f"    Input: {model['inputModalities']}")
        print(f"    Output: {model['outputModalities']}")
        print()

if __name__ == "__main__":
    verify_bedrock_access()
```

## Key Takeaways

- **AWS Bedrock** provides managed access to foundation models without infrastructure overhead
- **IAM permissions** must be configured before accessing models
- **Model access requests** are required for each model you want to use
- **Credentials** can be configured via environment variables or AWS CLI
- **Region selection** affects model availability and latency

## Additional Resources

- [AWS Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- [Bedrock Model Access Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- [LangChain AWS Integration](https://python.langchain.com/docs/integrations/platforms/aws/)
