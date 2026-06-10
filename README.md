# PDF RAG System with Qdrant and Qwen

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline for question answering over PDF documents.

The system extracts text from PDF files, preprocesses and chunks the content, generates embeddings, stores them in Qdrant, retrieves the most relevant passages for a user query, and uses a Large Language Model (LLM) to generate a final answer based on the retrieved context.

---

## Architecture

```text
PDF Documents
      │
      ▼
Text Extraction
      │
      ▼
Preprocessing & Cleaning
      │
      ▼
Chunking
      │
      ▼
Embeddings (USER-bge-m3)
      │
      ▼
Qdrant Vector Database
      │
      ▼
Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
Qwen3.5-35B-A3B
      │
      ▼
Generated Answer
      │
      ▼
Sources + Screenshot References
```

---

## Features

* PDF text extraction
* Text preprocessing and cleaning
* Semantic chunking
* Embedding generation using `deepvk/USER-bge-m3`
* Vector storage in Qdrant
* Semantic similarity search
* Answer generation using `Qwen3.5-35B-A3B`
* Source attribution
* PDF page screenshot generation
* Local execution

---

## Components

### PDF Processing

Responsible for:

* Reading PDF files
* Extracting text
* Cleaning formatting artifacts
* Preparing text for chunking

### Chunking

Documents are split into smaller chunks suitable for embedding generation and retrieval.

### Embedding Generation

Embeddings are generated using:

```text
deepvk/USER-bge-m3
```

Embedding endpoint:

```text
http://dgx-spark.waveaccess.ru:2347/embed
```

Each text chunk is converted into a dense vector representation.

### Vector Database

The project uses Qdrant to store:

* embeddings
* chunk text
* metadata
* source information

Example metadata:

```json
{
  "source": "16_4.pdf",
  "page": 147,
  "text": "..."
}
```

### Retrieval

For each user query:

1. Generate query embedding
2. Search Qdrant
3. Retrieve top-k relevant chunks
4. Build context for the LLM

### Answer Generation

Retrieved chunks are combined into a context prompt and sent to:

```text
Qwen3.5-35B-A3B
```

The model synthesizes an answer based only on the retrieved information.

---

## Retrieval-Augmented Generation (RAG)

The system follows a standard RAG workflow:

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Qdrant Search
      │
      ▼
Relevant Chunks
      │
      ▼
LLM Prompt Construction
      │
      ▼
Qwen Generation
      │
      ▼
Final Answer
```

Unlike a retrieval-only system, the LLM generates a new answer by combining information from multiple retrieved chunks.

---

## Example Workflow

### User Question

```text
Какие препараты рекомендуются при панкреатите?
```

### Retrieval

Qdrant returns the most relevant document fragments.

### Generation

Qwen receives:

* the user question
* retrieved context

and generates a synthesized answer.

### Output

```text
Answer:
...

Sources:
- 16_4.pdf | page 147
- 874_1.pdf | page 107
...
```

---

## Running the Project

### Index Documents

```bash
python run.py
```

The indexing stage:

1. Reads PDFs
2. Generates embeddings
3. Stores vectors in Qdrant

### Ask Questions

```bash
python run.py
```

Example:

```text
Type question here:
```

Enter a natural language question and receive:

* generated answer
* source references
* screenshot location

---

## Technologies

* Python
* Qdrant
* USER-bge-m3
* Qwen3.5-35B-A3B
* OpenAI-compatible API
* PDF processing libraries

---

## Future Improvements

* Hybrid search (BM25 + Vector Search)
* Metadata filtering
* Re-ranking stage
* Conversation memory
* Evaluation pipeline
* Web interface
* Streaming responses
* Multi-document citation support

---

## Author

Personal RAG project for semantic search and question answering over PDF documents using Qdrant and Qwen.
