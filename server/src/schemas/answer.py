# schemas/answer.py
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator
import json

class AnswerRequest(BaseModel):
    question: str = Field(..., description="The question to answer")
    history: str = Field(..., description="Chat history as JSON string")
    conversation_id: Optional[str] = None
    prompt_id: Optional[str] = None
    chunks: str = Field(..., description="Number of chunks as string")
    token_limit: int = Field(..., description="Token limit as number")
    isNoneDoc: bool = Field(default=False)
    active_docs: Optional[str] = None
    retriever: Optional[str] = None
    # Optional fields that might be added by client
    api_key: Optional[str] = None
    locale: Optional[str] = None 
    index: Optional[int] = None  # Used in streaming

    @validator('history')
    def validate_history(cls, v):
        try:
            history_list = json.loads(v)
            # Validate each history item has at least a prompt field
            for item in history_list:
                if not isinstance(item, dict) or 'prompt' not in item:
                    raise ValueError("History items must have at least a prompt field")
            return v
        except json.JSONDecodeError:
            raise ValueError("History must be a valid JSON string")

    class Config:
        schema_extra = {
            "example": {
                "question": "What are the key features?",
                "history": "[{\"prompt\":\"hi\",\"response\":\"Hello!\"}]",
                "conversation_id": None,
                "prompt_id": "default",
                "chunks": "2",
                "token_limit": 2000,
                "isNoneDoc": True,
                "active_docs": None,
                "retriever": None
            }
        }

class Source(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    source: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[Source]
    conversation_id: Optional[str]
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "The key features include...",
                "sources": [
                    {
                        "source": "documentation.md",
                        "text": "Key features section...",
                        "title": "Documentation Title"
                    }
                ],
                "conversation_id": "123456789"
            }
        }

