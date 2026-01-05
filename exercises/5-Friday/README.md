# Friday: Structured Output & RAG Tools

## Exercise Schedule

| Exercise | Type | Duration | Prerequisites |
|----------|------|----------|---------------|
| 01: Structured Responses | Implementation | 60-75 min | Reading 01-03, Demo 01-02 |
| 02: RAG Agent | Implementation | 90-120 min | Reading 04-05, Demo 03, Week 3-4 knowledge |

## Learning Objectives

By completing these exercises, you will:
- Implement structured output using Pydantic models
- Configure the `response_format` parameter for reliable output
- Handle validation errors gracefully
- Build a RAG agent that integrates vector stores with LangChain v1.0
- Create retrieval tools for agent use

## Before You Begin

1. **Complete the readings** in `readings/5-Friday/`
2. **Watch/run demos** in `demos/5-Friday/code/`
3. **Review Week 3-4**: Vector database concepts (ChromaDB, embeddings)
4. Install dependencies:
   ```bash
   pip install langchain langchain-openai chromadb pydantic
   ```

## Exercises

### Exercise 01: Structured Responses (Implementation)
See [exercise_01_structured_responses.md](exercise_01_structured_responses.md)
Starter code: `starter_code/exercise_01_starter.py`

Implement agents that return structured, validated output using Pydantic models.

### Exercise 02: RAG Agent (Implementation)
See [exercise_02_rag_agent.md](exercise_02_rag_agent.md)
Starter code: `starter_code/exercise_02_starter.py`

Build a complete RAG agent with vector store integration, combining your Week 3-4 knowledge with LangChain v1.0 agents.

## Estimated Time
**Total: 2.5-3.5 hours**

## Key v1.0 Patterns

### Structured Output with Pydantic
```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent

class TaskAnalysis(BaseModel):
    """Structured output for task analysis."""
    complexity: str = Field(description="low, medium, or high")
    estimated_hours: float = Field(description="Estimated hours to complete")
    risks: list[str] = Field(description="Potential risks")

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    response_format=TaskAnalysis,  # Enforce structured output
    name="analysis_agent"
)
```

### RAG Tool for Agents
```python
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma

vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

@tool
def search_documents(query: str) -> str:
    """Search the knowledge base for relevant information."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join(doc.page_content for doc in docs)
```

> **Tip**: The RAG exercise integrates everything from Weeks 3-5. Take your time to build a solid solution.
