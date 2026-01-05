# Exercise 02: RAG Agent

## Overview

This capstone exercise combines everything from Weeks 3-5: vector databases, embeddings, and LangChain v1.0 agents. You'll build a complete RAG (Retrieval-Augmented Generation) agent that can search a document collection and answer questions.

## Learning Objectives

- Create retrieval tools that wrap vector store queries
- Build agents that use RAG in their decision-making
- Implement both 2-Step RAG and Agentic RAG patterns
- Ground agent responses in retrieved context

## The Scenario

You're building a documentation assistant for a software product:
1. Load and index documentation into a vector store
2. Create a search tool for the agent
3. Build an agent that retrieves relevant docs before answering
4. Compare different RAG strategies

## Your Tasks

### Task 1: Vector Store Setup (25 min)

Implement `setup_vector_store()`:
- Initialize ChromaDB with persistent storage
- Use `text-embedding-3-small` for embeddings
- Index the provided sample documents

> **Hint**: Reuse your Week 3-4 knowledge of ChromaDB setup.

### Task 2: Retrieval Tool (20 min)

Implement `create_search_tool()`:
- Create a `@tool` decorated function
- Perform similarity search on the vector store
- Return formatted results with context

### Task 3: RAG Agent (30 min)

Implement `create_rag_agent()`:
- Use `create_agent()` with your search tool
- Write a system prompt that encourages document search
- Include memory for multi-turn conversations

### Task 4: RAG Strategy Comparison (25 min)

Implement two RAG patterns:

**2-Step RAG**: Agent ALWAYS searches before answering
```python
system_prompt = """You MUST use search_documents for ANY question.
1. First, search for relevant information
2. Then, synthesize an answer from the results"""
```

**Agentic RAG**: Agent decides when to search
```python
system_prompt = """You have access to a document search tool.
Use it when you need specific information from the docs.
For general questions, you may answer directly."""
```

Compare the behavior and effectiveness of each approach.

## Definition of Done

- [_] Vector store created with sample documents
- [_] Search tool works and returns relevant results
- [_] RAG agent answers questions using retrieved context
- [_] Both RAG strategies implemented and compared
- [_] Agent handles questions where no docs are relevant

## Testing Your Solution

```bash
cd exercises/5-Friday/starter_code
python exercise_02_starter.py
```

Expected output:
```
=== RAG Agent Test ===

[INFO] Setting up vector store...
[OK] Indexed 10 documents

[INFO] Creating search tool...
[OK] Search tool ready

[INFO] Creating RAG agent...
[OK] Agent 'rag_assistant' created

=== Testing RAG Agent ===

Question: "How do I configure authentication?"
[TOOL] search_documents called
[RETRIEVED] 3 relevant documents
Agent: Based on the documentation, you can configure authentication by...

Question: "What's the weather like?"
[INFO] Agent answered without search (not in docs)
Agent: I'm a documentation assistant and don't have weather information...

=== RAG Strategy Comparison ===
2-Step RAG: Always searched (5/5 queries)
Agentic RAG: Selective search (3/5 queries)

=== Test Complete ===
```

## Sample Documents

```python
SAMPLE_DOCS = [
    {
        "content": "Authentication can be configured using OAuth 2.0. Set the AUTH_PROVIDER environment variable to 'oauth' and provide CLIENT_ID and CLIENT_SECRET.",
        "metadata": {"topic": "authentication", "section": "setup"}
    },
    {
        "content": "Rate limiting is enabled by default. Configure RATE_LIMIT_PER_MINUTE to adjust the limit. Default is 100 requests per minute.",
        "metadata": {"topic": "rate-limiting", "section": "config"}
    },
    # ... more documents
]
```

## Key Patterns

```python
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langgraph.checkpoint.memory import InMemorySaver

# Setup embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Create search tool
@tool
def search_documents(query: str) -> str:
    """Search documentation for relevant information.
    
    Use for questions about configuration, setup, features, or troubleshooting.
    """
    docs = vectorstore.similarity_search(query, k=3)
    if not docs:
        return "No relevant documents found."
    return "\n\n---\n\n".join(
        f"Source: {d.metadata.get('topic', 'unknown')}\n{d.page_content}"
        for d in docs
    )

# Create RAG agent
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_documents],
    checkpointer=InMemorySaver(),
    system_prompt="You are a documentation assistant. Search for relevant docs before answering.",
    name="rag_assistant"
)
```

## RAG Best Practices

| Practice | Why |
|----------|-----|
| Always return sources | Helps users verify information |
| Limit to 3-5 docs | Too many overwhelms context |
| Include metadata | Helps agent understand relevance |
| Handle no results | Graceful fallback when docs don't help |
| Use descriptive tool description | Helps agent know when to search |

## Stretch Goals (Optional)

1. Implement MMR (Maximum Marginal Relevance) for diverse results
2. Add source citations to agent responses
3. Create multiple specialized search tools (by topic)
4. Implement hybrid search (keyword + semantic)
5. Add relevance score filtering
