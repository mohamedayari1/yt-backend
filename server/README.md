# YouTube Backend Service

A FastAPI-based backend service for YouTube chatbot functionality with RAG (Retrieval-Augmented Generation) capabilities.

## Setup

### Prerequisites
- Python 3.11+
- UV package manager

### Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Fill in your Azure OpenAI credentials in the `.env` file:
```bash
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_ENDPOINT=your_actual_endpoint_here
AZURE_EMBDEDDINGS_API_KEY=your_actual_embeddings_key_here
AZURE_EMBDEDDINGS_ENDPOINT=your_actual_embeddings_endpoint_here
```

### Installation

1. Install dependencies using UV:
```bash
uv sync
```

2. Run the development server:
```bash
uv run python src/main.py
```

The server will start on `http://127.0.0.1:8000` by default.

## Project Structure

- `src/core/` - Core configuration and database clients
- `src/llm/` - Language model implementations (Azure OpenAI, Google)
- `src/routers/` - FastAPI route handlers
- `src/schemas/` - Pydantic schemas for request/response models
- `src/services/` - Business logic services
- `src/utils/` - Utility functions and helpers
- `src/vectorstore/` - Vector database implementations

## Features

- RAG-based question answering
- Multiple LLM provider support (Azure OpenAI, Google)
- Vector database integration (MongoDB, Qdrant)
- Structured logging
- Environment-based configuration

## Security

This project uses environment variables for sensitive configuration. Never commit API keys or other secrets to the repository. Use the `.env.example` file as a template for required environment variables.
