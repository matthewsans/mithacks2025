# Build Semantic RAG Queries

Converts company questions into structured queries for RAG systems.

## Usage

```python
from break_into_questions import build_semantic_rag_queries

queries = build_semantic_rag_queries("Compare Apple and Google revenue", API_KEY)
```

Takes 1 question about companies → Returns 5+ specific queries for each company.

## Dependencies
- `requests`
- `typing` (built-in)
