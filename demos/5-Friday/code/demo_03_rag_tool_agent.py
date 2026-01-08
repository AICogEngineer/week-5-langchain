"""
Demo 03: RAG Tool Agent - Combining Vector Stores with Agents

This demo shows trainees how to:
1. Create a RAG tool using @tool decorator
2. Integrate vector stores with agents
3. Implement agentic RAG patterns
4. Build production-ready RAG agents

Learning Objectives:
- Build RAG tools for agent integration
- Understand 2-step vs agentic RAG
- Create agents with knowledge base access

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: January 2026

References:
- Written Content: readings/5-Friday/05-building-rag-tools-for-agents.md

Prerequisites (Week 3-4):
- Vector store concepts
- Embeddings
- Similarity search
"""

import os
import time
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec

# ============================================================================
# PART 1: Setting Up the Knowledge Base (Pinecone)
# ============================================================================

print("=" * 70)
print("PART 1: Creating a Knowledge Base (Vector Store)")
print("=" * 70)

print("""
First, we need a knowledge base to search.
We will use Pinecone as our vector database.
""")

# Check for API Keys
if not os.getenv("PINECONE_API_KEY"):
    raise ValueError("PINECONE_API_KEY environment variable is not set")

# 1. Prepare Data
# ------------------------------------------------------------------
raw_data = {
    "refund_policy": {
        "content": """REFUND POLICY: Customers can request a full refund within 30 days 
        of purchase for any unused product. Used products may be eligible for partial 
        refund at management discretion. Digital products are non-refundable after 
        download. Refunds are processed within 5-7 business days to the original 
        payment method.""",
        "metadata": {"category": "policies", "last_updated": "2025-01-01"}
    },
    "shipping_info": {
        "content": """SHIPPING INFORMATION: Standard shipping takes 5-7 business days. 
        Express shipping (2-3 days) available for $12.99. Free shipping on orders 
        over $50. International shipping available to select countries with 
        additional customs fees. All orders include tracking number via email.""",
        "metadata": {"category": "logistics", "last_updated": "2025-01-01"}
    },
    "product_warranty": {
        "content": """WARRANTY COVERAGE: All electronics carry a 1-year manufacturer 
        warranty. Extended warranty available for purchase (2 or 3 year options). 
        Warranty covers defects in materials and workmanship. Does not cover 
        accidental damage, water damage, or misuse. Warranty claims require proof 
        of purchase.""",
        "metadata": {"category": "policies", "last_updated": "2025-01-01"}
    },
    "account_management": {
        "content": """ACCOUNT MANAGEMENT: Users can update profile information in 
        Settings > Profile. Password reset available via email verification. 
        Two-factor authentication recommended for security. Account deletion 
        requests processed within 48 hours. Contact support for account recovery.""",
        "metadata": {"category": "support", "last_updated": "2025-01-01"}
    },
    "payment_methods": {
        "content": """PAYMENT OPTIONS: We accept Visa, Mastercard, American Express, 
        and PayPal. Apple Pay and Google Pay available on mobile. Monthly payment 
        plans available for orders over $200 through Affirm. Gift cards accepted 
        both online and in-store.""",
        "metadata": {"category": "payments", "last_updated": "2025-01-01"}
    }
}

documents = []
for key, data in raw_data.items():
    documents.append(
        Document(
            page_content=data["content"].replace("    ", "").strip(),
            metadata=data["metadata"]
        )
    )

print(f"Created {len(documents)} documents for indexing.")

# 2. Initialize Embeddings and Vector Store
# ------------------------------------------------------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
index_name = os.getenv("PINECONE_INDEX_NAME", "langchain-demo-index")

print(f"Connecting to Pinecone index: {index_name}")

# Initialize Pinecone client to check/create index
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Check if index exists
existing_indexes = pc.list_indexes().names()

if index_name not in existing_indexes:
    print(f"Index '{index_name}' not found. Creating it...")
    try:
        pc.create_index(
            name=index_name,
            dimension=1536,  # text-embedding-3-small dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Waiting for index to be ready...")
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
        print("Index created and ready!")
    except Exception as e:
        print(f"Error creating index: {e}")
        print("Attempting to proceed (index might be creating)...")

# Connect to the index
vectorstore = PineconeVectorStore.from_documents(
    documents=documents,
    embedding=embeddings,
    index_name=index_name
)

print("\n[Step 1] Testing vector store retrieval...")
test_results = vectorstore.similarity_search("refund policy", k=2)
print(f"  Found {len(test_results)} relevant documents for 'refund policy'")
for i, doc in enumerate(test_results):
    print(f"    Doc {i+1}: {doc.page_content[:60]}...")

# ============================================================================
# PART 2: Creating RAG Tool
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: Creating the RAG Tool")
print("=" * 70)

print("""
The RAG tool wraps the vector store search.
The docstring tells the agent WHEN to use it.
""")

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the company knowledge base for relevant information.
    
    Use this tool when the user asks about:
    - Refund or return policies
    - Shipping information and delivery times
    - Warranty coverage and claims
    - Account settings and management
    - Payment methods and options
    
    Returns relevant documentation to answer customer questions.
    """
    # Use the global vectorstore
    results = vectorstore.similarity_search(query, k=2)
    
    if not results:
        return "No relevant information found in the knowledge base for this query."
    
    # Format results for the agent
    formatted = []
    for i, doc in enumerate(results, 1):
        formatted.append(f"Document {i}:\n{doc.page_content}")
    
    return "\n\n---\n\n".join(formatted)

print("\n[Step 2] Testing RAG tool directly...")
try:
    result = search_knowledge_base.invoke({"query": "how do I get a refund?"})
    print(f"  Tool output:\n    {result[:200]}...")
except Exception as e:
    print(f"  Error testing tool: {e}")

# ============================================================================
# PART 3: Building the RAG Agent
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: Building the RAG Agent")
print("=" * 70)

print("""
Now we combine the RAG tool with an agent.
The agent decides when to search and synthesizes answers.
""")

rag_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_knowledge_base],
    system_prompt="""You are a helpful customer support agent for an e-commerce company.
    
    When customers ask questions about policies, shipping, warranties, accounts, or payments:
    1. Use the search_knowledge_base tool to find relevant information
    2. Synthesize the information into a helpful, conversational response
    3. Cite the source when providing policy details
    
    If the knowledge base doesn't have the answer, be honest and offer to connect 
    them with a human agent.
    
    Be friendly, professional, and concise.""",
    checkpointer=InMemorySaver(),
    name="rag_support_agent"
)

print("  ✓ RAG agent created: rag_support_agent")

config = {"configurable": {"thread_id": "customer_support_session_001"}}

# ============================================================================
# PART 4: Testing the RAG Agent
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: Testing the RAG Agent")
print("=" * 70)

test_questions = [
    "Can I get a refund if I opened the product?",
    "How long does shipping take?",
    "What does the warranty cover?",
]

for question in test_questions:
    print(f"\n  Customer: {question}")
    try:
        result = rag_agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config
        )
        response = result['messages'][-1].content
        print(f"  Agent: {response[:200]}...")
    except Exception as e:
        print(f"  Error invoking agent: {e}")

# ============================================================================
# PART 5: 2-Step RAG vs Agentic RAG
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: 2-Step RAG vs Agentic RAG")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│                    2-STEP RAG vs AGENTIC RAG                        │
├──────────────────────┬──────────────────────────────────────────────┤
│ 2-STEP RAG           │ AGENTIC RAG                                  │
├──────────────────────┼──────────────────────────────────────────────┤
│ ALWAYS retrieves     │ Agent DECIDES when to retrieve               │
│                      │                                              │
│ Fixed k documents    │ Can adapt based on initial results           │
│                      │                                              │
│ Single query         │ Can reformulate or follow-up                 │
│                      │                                              │
│ Retrieve → Generate  │ Think → Retrieve? → Generate → Repeat?       │
│                      │                                              │
│ Simpler              │ More flexible                                │
│                      │                                              │
│ Lower latency        │ Potentially higher latency                   │
│                      │                                              │
│ Better for simple QA │ Better for complex interactions              │
└──────────────────────┴──────────────────────────────────────────────┘

When to use which:
- 2-Step: FAQ lookup, simple document QA, low latency needs
- Agentic: Multi-turn conversations, complex queries, when retrieval 
          is sometimes unnecessary
""")

# Demonstrate agentic behavior - agent decides NOT to search
print("\n[Step 5] Agent deciding when NOT to search...")

# Question that doesn't need knowledge base
general_question = "Hello! How are you today?"
print(f"\n  Customer: {general_question}")
try:
    result = rag_agent.invoke(
        {"messages": [{"role": "user", "content": general_question}]},
        {"configurable": {"thread_id": "agentic_demo"}}
    )
    response = result['messages'][-1].content
    print(f"  Agent: {response}")
    print("  (Notice: Agent didn't use the search tool for this greeting)")
except Exception as e:
    print(f"  Error invoking agent: {e}")

# ============================================================================
# PART 6: Enhanced RAG Tool with Metadata
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: Enhanced RAG with Source Citations")
print("=" * 70)

@tool
def search_with_sources(query: str) -> str:
    """
    Search knowledge base and return results with source citations.
    
    Use for any customer question about company policies, products, or services.
    Results include source document information for citation.
    """
    # Use the global vectorstore
    results = vectorstore.similarity_search(query, k=2)
    
    if not results:
        return "No relevant information found."
    
    formatted = []
    for i, doc in enumerate(results, 1):
        # Access metadata from the Document object
        metadata = doc.metadata
        source_info = f"[Source: {metadata.get('category', 'unknown').upper()}, Updated: {metadata.get('last_updated', 'unknown')}]"
        formatted.append(f"{doc.page_content}\n{source_info}")
    
    return "\n\n---\n\n".join(formatted)

print("\n[Step 6] Testing RAG with source citations...")
try:
    result = search_with_sources.invoke({"query": "warranty information"})
    print(f"  {result[:300]}...")
except Exception as e:
    print(f"  Error testing tool: {e}")

# ============================================================================
# PART 7: Production Considerations
# ============================================================================

print("\n" + "=" * 70)
print("PART 7: Production RAG Agent Checklist")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│ PRODUCTION RAG AGENT CHECKLIST                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ☐ REAL VECTOR STORE                                                 │
│   (Implemented!) Pinecone, ChromaDB, etc.                           │
│   Ensure proper indexing pipelines.                                 │
│                                                                     │
│ ☐ QUALITY EMBEDDINGS                                                │
│   Use text-embedding-3-small or better                              │
│   Same model for indexing and querying!                             │
│                                                                     │
│ ☐ APPROPRIATE CHUNK SIZE                                            │
│   800-1200 characters typical                                       │
│   ~200 character overlap                                            │
│                                                                     │
│ ☐ RETRIEVAL TUNING                                                  │
│   Adjust k based on use case (3-5 typical)                          │
│   Consider MMR for diversity                                        │
│   Score thresholding for quality                                    │
│                                                                     │
│ ☐ ERROR HANDLING                                                    │
│   Handle empty results                                              │
│   Timeout for vector store queries                                  │
│   Fallback responses                                                │
│                                                                     │
│ ☐ MONITORING                                                        │
│   Log retrieval quality                                             │
│   Track which documents are used                                    │
│   Monitor latency                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
# DEMO SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("DEMO COMPLETE: RAG Tool Agent")
print("=" * 70)

print("""
Key Takeaways:

1. RAG tools wrap vector store search with @tool decorator
2. Tool docstring tells agent when to search
3. Agent synthesizes search results into helpful responses
4. Agentic RAG = agent decides when/if to retrieve
5. Include source citations for trust and accuracy

Week 5 Complete!
You now have all the pieces for production LangChain agents:
- Model initialization (Monday)
- Tools and agents (Tuesday)
- Debugging with LangSmith (Wednesday)
- Memory and state (Thursday)
- Structured output and RAG (Friday)
""")

print("\n" + "=" * 70)
print("INSTRUCTOR NOTES")
print("=" * 70)

print("""
Show trainees:
1. The Pinecone dashboard (if available) to show indexed vectors.
2. How the agent decides to use the RAG tool.
3. The difference when agent doesn't need to search.
4. How to format results for best agent understanding.

Live Demo Tips:
- Ensure PINECONE_API_KEY and PINECONE_INDEX_NAME are set.
- Show traces in LangSmith to see the retrieval steps.
- Try questions that need multiple docs.

Discussion Questions:
- "Why use Pinecone (serverless) vs local ChromaDB?"
- "How do you handle index updates in a live system?"
- "What security implications are there with external vector stores?"

Pair Programming Exercise:
Build a pipeline that continuously ingests new PDFs into Pinecone 
and have the agent answer questions about them.
""")

print("=" * 70)
