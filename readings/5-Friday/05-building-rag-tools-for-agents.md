# Building RAG Tools for Agents

## Learning Objectives
- Create retrieval tools that agents can use
- Connect vector stores to agent workflows
- Understand agentic RAG patterns
- Build agents that decide when to retrieve

## Why This Matters

RAG (Retrieval Augmented Generation) connects agents to your knowledge base. Instead of relying solely on training data, agents can search and retrieve relevant information before responding. This enables agents that answer questions about your specific documents, products, or domain.

This reading brings together concepts from Weeks 3-4 (vector databases) with Week 5's agent architecture.

## The Concept

### What is Agentic RAG?

In traditional RAG, retrieval happens on every query. In **agentic RAG**, the agent decides when to retrieve:

```
Traditional RAG:
User Query → ALWAYS Retrieve → Generate Response

Agentic RAG:
User Query → Agent Decides → Maybe Retrieve → Generate Response
                            → Or Just Respond (no retrieval needed)
```

This is more efficient—simple greetings don't need knowledge base searches.

### Creating a RAG Tool

A RAG tool wraps your vector store in a function the agent can call:

```python
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Set up vector store (assuming it's already populated)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the company knowledge base for relevant information.
    
    Use this when users ask about:
    - Company policies and procedures
    - Product information
    - Technical documentation
    
    DO NOT use for general knowledge questions.
    
    Args:
        query: The search query describing what information to find
    
    Returns:
        Relevant passages from the knowledge base
    """
    docs = vectorstore.similarity_search(query, k=3)
    
    if not docs:
        return "No relevant documents found."
    
    # Format results for the agent
    results = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content[:500]  # Limit content length
        results.append(f"[{i}] ({source})\n{content}")
    
    return "\n\n".join(results)
```

### Creating a RAG Agent

Combine the RAG tool with `create_agent()`:

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_knowledge_base],
    checkpointer=InMemorySaver(),
    system_prompt="""You are a helpful assistant with access to a knowledge base.

When users ask about company-specific information:
1. First, search the knowledge base
2. Use the retrieved information to answer
3. If information isn't found, acknowledge the limitation

For general questions, respond directly without searching.""",
    name="rag_agent"
)
```

### 2-Step RAG vs. Agentic RAG

**2-Step RAG**: Fixed retrieve-then-generate
```python
# Tool that ALWAYS searches (deterministic)
@tool
def mandatory_search(query: str) -> str:
    """Search is called on every user query."""
    # System prompt tells agent to always use this
    ...
```

**Agentic RAG**: Agent chooses when to search
```python
# Tool the agent MAY use (autonomous)
@tool
def optional_search(query: str) -> str:
    """Search only when query requires knowledge base info."""
    # Agent decides based on query if search is needed
    ...
```

Choose based on your needs:
- Use 2-Step RAG when every query needs specific knowledge
- Use Agentic RAG when queries vary (some need KB, some don't)

### Improving Retrieval Quality

**Better Tool Description:**
```python
@tool
def search_product_docs(query: str) -> str:
    """
    Search product documentation for technical specifications,
    installation guides, troubleshooting steps, and feature descriptions.
    
    SEARCH TIPS:
    - Be specific: "wifi setup" not "how to connect"
    - Include product name: "Model X battery replacement"
    
    Returns up to 3 most relevant document sections.
    """
    ...
```

**Metadata Filtering:**
```python
@tool
def search_by_category(query: str, category: str) -> str:
    """
    Search documents in a specific category.
    
    Args:
        query: What to search for
        category: Document category (policies, products, technical)
    """
    docs = vectorstore.similarity_search(
        query,
        k=3,
        filter={"category": category}
    )
    ...
```

**Score Thresholding:**
```python
@tool
def search_with_confidence(query: str) -> str:
    """Search and include confidence scores."""
    # Use similarity_search_with_score for scores
    results = vectorstore.similarity_search_with_score(query, k=5)
    
    # Filter by score (lower is better for distance metrics)
    relevant = [(doc, score) for doc, score in results if score < 0.5]
    
    if not relevant:
        return "No highly relevant documents found."
    
    # Format with confidence
    formatted = []
    for doc, score in relevant:
        confidence = "High" if score < 0.3 else "Medium"
        formatted.append(f"[{confidence}] {doc.page_content[:300]}")
    
    return "\n\n".join(formatted)
```

### Multi-Source RAG

Agents can use multiple retrieval tools:

```python
@tool
def search_policies(query: str) -> str:
    """Search HR and company policies."""
    docs = policy_vectorstore.similarity_search(query, k=2)
    return format_docs(docs)

@tool
def search_products(query: str) -> str:
    """Search product catalog and specifications."""
    docs = product_vectorstore.similarity_search(query, k=3)
    return format_docs(docs)

@tool
def search_support(query: str) -> str:
    """Search support tickets and solutions."""
    docs = support_vectorstore.similarity_search(query, k=3)
    return format_docs(docs)

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_policies, search_products, search_support],
    system_prompt="""You have access to three knowledge bases:
    - Policies: HR and company rules
    - Products: Catalog and specs
    - Support: Past tickets and solutions
    
    Choose the right source based on the question.""",
    name="multi_source_rag_agent"
)
```

### RAG Tool Best Practices

| Practice | Why |
|----------|-----|
| Limit chunk size in response | Prevent token overflow |
| Include source metadata | Enables citation |
| Filter by relevance score | Avoid low-quality results |
| Clear tool description | Help agent choose correctly |
| Handle empty results | Graceful "not found" message |
| Multiple specific tools | Better than one generic tool |

## Code Example

```python
"""
Building RAG Tools for Agents
LangChain Version: v1.0+
"""
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import InMemorySaver

# Sample documents (in practice, load from files)
documents = [
    {
        "content": """Widget Pro User Manual
        The Widget Pro is our flagship product. It features a 
        rechargeable battery lasting 12 hours, WiFi connectivity,
        and a 4-inch touchscreen display. To charge, connect the
        included USB-C cable to any standard power adapter.""",
        "source": "widget_pro_manual.pdf"
    },
    {
        "content": """Return Policy
        All products may be returned within 30 days of purchase
        for a full refund. Items must be in original packaging.
        Damaged items can be returned within 90 days for repair
        or replacement under warranty.""",
        "source": "policies/returns.md"
    },
    {
        "content": """Troubleshooting: Widget Won't Turn On
        If your widget doesn't power on, try these steps:
        1. Hold the power button for 10 seconds
        2. Connect to charger for at least 30 minutes
        3. Check for physical damage
        Contact support if issue persists.""",
        "source": "support/troubleshooting.md"
    }
]

# Create embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Split and prepare documents
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = []
for doc in documents:
    splits = splitter.split_text(doc["content"])
    for split in splits:
        chunks.append({
            "content": split,
            "metadata": {"source": doc["source"]}
        })

# Create vector store (in memory for demo)
vectorstore = Chroma.from_texts(
    texts=[c["content"] for c in chunks],
    embedding=embeddings,
    metadatas=[c["metadata"] for c in chunks]
)

# Create RAG tool
@tool
def search_knowledge_base(query: str) -> str:
    """
    Search our product documentation and policies.
    
    Use for questions about:
    - Product features and specifications
    - How-to and troubleshooting
    - Company policies (returns, warranty)
    
    NOT for general knowledge questions.
    """
    docs = vectorstore.similarity_search(query, k=2)
    
    if not docs:
        return "No relevant information found in the knowledge base."
    
    results = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        results.append(f"[Source: {source}]\n{doc.page_content}")
    
    return "\n\n---\n\n".join(results)

# Create RAG agent
checkpointer = InMemorySaver()

rag_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_knowledge_base],
    checkpointer=checkpointer,
    system_prompt="""You are a customer support assistant with access 
to a knowledge base. 

When answering questions:
1. Search the knowledge base for relevant information
2. Cite your sources when using retrieved information
3. If information isn't in the knowledge base, say so clearly
4. For simple greetings or general chat, respond directly

Be helpful, accurate, and concise.""",
    name="customer_support_rag_agent"
)

# Test the RAG agent
config = {"configurable": {"thread_id": "rag_demo"}}

print("=== RAG Agent Demo ===\n")

queries = [
    "Hi there!",  # Should respond without retrieval
    "How long does the Widget Pro battery last?",  # Should search
    "What's your return policy?",  # Should search
    "Can you explain quantum physics?",  # Outside knowledge base
]

for query in queries:
    print(f"User: {query}")
    result = rag_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    }, config)
    print(f"Agent: {result['messages'][-1].content}")
    print("-" * 50)
```

## Key Takeaways

- **RAG tools connect agents to your knowledge**: Use vector stores from Weeks 3-4
- **`@tool` decorator**: Makes retrieval functions agent-callable
- **Tool description guides usage**: Tell agent when to search
- **Agentic RAG is flexible**: Agent decides when to retrieve
- **Format results for agents**: Include metadata, limit size
- **Multiple tools for multiple sources**: Better than one generic search
- **Combines full stack**: Embeddings + Vector DB + Agent = RAG Agent

## Additional Resources

- [LangChain RAG Tutorial](https://docs.langchain.com/oss/python/langchain/tutorials/rag)
- [Vector Stores in LangChain](https://docs.langchain.com/oss/python/langchain/integrations/vectorstores)
- [Agentic RAG Patterns](https://docs.langchain.com/oss/python/langchain/concepts/rag)
