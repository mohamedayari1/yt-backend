
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.routers.answer import answer_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    app = FastAPI(
        title="LawGPT API",
        description="API for LawGPT - A Legal Question Answering System",
        version="1.0.0",
    )
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Restrict this in production
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(answer_router)
    
    return app

app = create_app()
