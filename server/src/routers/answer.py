from fastapi import APIRouter, HTTPException, Request
import traceback
import time
import os

from src.schemas.answer import AnswerRequest, AnswerResponse, Source
from src.llm.azure_openai import OpenAILLM
from src.utils.logging import get_logger
from src.services.naive_rag import NaiveRAG


llm = OpenAILLM()


# Load prompt template
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(CURRENT_DIR, "../prompts")

try:
    with open(os.path.join(PROMPTS_DIR, "chat_combine_default.txt"), "r") as file:
        CHAT_COMBINE = file.read()
except FileNotFoundError as e:
    raise FileNotFoundError("Prompt file is missing. Please ensure it is in the 'prompts' directory.")


# Initialize logger
logger = get_logger("youtube-chatbot-logger")

answer_router = APIRouter()

mock_sources = [
    Source(
        title="Introduction to Constitutional Law",
        text="Constitutional law establishes the fundamental principles and framework of government, defining the structure, powers, and limitations of governmental institutions.",
        source="constitutional_law_basics.pdf"
    ),
    Source(
        title="Criminal Law Principles",
        text="Criminal law defines offenses against the state and prescribes punishments for violations. It encompasses both substantive criminal law and criminal procedure.",
        source="criminal_law_handbook.md"
    ),
    Source(
        title="Contract Law Fundamentals", 
        text="A contract is a legally binding agreement between two or more parties. For a contract to be valid, it must have offer, acceptance, consideration, and legal capacity.",
        source="contracts_guide.txt"
    )]

# Log router initialization
logger.info("Answer router initialized successfully")
logger.info(f"Mock sources count: {len(mock_sources)}")

@answer_router.post("/api/answer", response_model=AnswerResponse)
async def answer_endpoint(
    request: Request,
    answer_request: AnswerRequest,
):
    question = answer_request.question
            

    retriever = NaiveRAG(
                question=question,
                chat_history=answer_request.history,
                prompt=CHAT_COMBINE)
    try:
   
   
   
   
        # answer = llm.answer_query(answer_request.question)
        answer, docs = await retriever.gen()

        # Create response
        response = AnswerResponse(
            answer=answer,
            sources=docs,
            conversation_id=answer_request.conversation_id
        )
        

        return response
        
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": str(e),
            }
        )

# Add a health check endpoint for debugging
@answer_router.get("/api/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "service": "answer-router"}

# Log all registered routes
logger.info("Available routes in answer router:")
for route in answer_router.routes:
    logger.info(f"  {route.methods} {route.path}")
