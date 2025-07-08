from typing import Annotated, Optional

from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict



def toListField(listField: str | list[str]):
    if isinstance(listField, str):
        return listField.split(",")
    return listField


CorsField = Annotated[list[str] | str, BeforeValidator(toListField)]



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        missing="ignore",
    )

class LLMSettings(Settings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str = "2025-01-01-preview"


class AzureEmbeddingsSettings(Settings):
    AZURE_EMBDEDDINGS_API_KEY: str
    AZURE_EMBDEDDINGS_ENDPOINT: str
    AZURE_EMBDEDDINGS_API_VERSION: str = "2023-05-15"
    AZURE_EMBDEDDINGS_DEPLOYMENT: str = "text-embedding-3-large"





class AppSettings(Settings):
    host: str = "127.0.0.1"
    port: str = "8000"
    version: str = "0.0.1"
    name: str = "oratio-svc"
    env: str = "local"

    cors_allow_origins: CorsField = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: CorsField = ["*"]
    cors_allow_headers: CorsField = ["*"]

class MongoDBSettings(Settings):
    MONGODB_URL: str = "mongodb+srv://zoldyck:zoldyck@cluster0.kjantw5.mongodb.net/"
    # MONGODB_DB_NAME: str = "oratio_prod"
    # MONGODB_COLLECTION_NAME: Optional[str] = "prod_conversations"
    MONGODB_DB_NAME: str = "beta-testing-db"
    MONGODB_COLLECTION_NAME: Optional[str] = "conversations_collection"
    
    # This DB and collections are for law data
    LAW_DB_NAME: str = "test_german_law_database"
    LABOR_LAW_COLLECTION_NAME: Optional[str] = "labor_law_sections"
    IMMIGRATION_LAW_COLLECTION_NAME: Optional[str] = "immigration_law_sections"
    
class MonogoVectorSettings:
    MONGO_VECTORDATABASE_NAME: str = "youtube_vector_database"
    MONGO_DATABASE_HOST: str = (
        "mongodb+srv://zoldyck:zoldyck@cluster0.kjantw5.mongodb.net/"
    )
    LABOR_LAW_COLLECTION_NAME: Optional[str] = "youtube_transcripts_vectors"
    IMMIGRATION_LAW_COLLECTION_NAME: Optional[str] = "new_IMMIGRATION_LAW_COLLECTION_NAME"
class QdrantSettings(Settings):
    USE_QDRANT_CLOUD: bool = False    
    QDRANT_DATABASE_HOST: str = "131.189.152.101"
    QDRANT_DATABASE_PORT: int = 6333
    QDRANT_CLOUD_URL: Optional[str] = None
    QDRANT_APIKEY: Optional[str] = None
    EMBEDDING_SIZE: int = 384

class GoogleSettings(Settings):
    GOOGLE_API_KEY: str = "AIzaSyATj8Clioh6EYXoTzy5WwNVHW5mbLxHw0s"

class SupabaseSettings(Settings):
    SUPABASE_URL: str = "https://cmqmloclnvesqovcdhvy.supabase.co"
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNtcW1sb2NsbnZlc3FvdmNkaHZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc2NDYxODcsImV4cCI6MjA1MzIyMjE4N30.Q_mlFr5eMy4Dtp2oRPuCFIrlRb4jiPVep4e0-HkzMF0"

class TokenSettings(Settings):
    DAILY_INPUT_LIMIT: int = 20000  # Daily input token limit
    DAILY_OUTPUT_LIMIT: int = 5000   # Daily output token limit
    DAILY_MESSAGE_LIMIT: int = 1000  # Daily message count limit
    USER_URL: str = "mongodb+srv://zoldyck:zoldyck@cluster0.kjantw5.mongodb.net/"
    USER_DB_NAME: str = "beta-testing-db"
    USER_COLLECTION_NAME: Optional[str] = "users_collection"

class ClassifierSettings:
    PREDICT_ENDPOINT: str = "http://131.189.208.33:8000/predict"


# Create instances
llm_settings = LLMSettings()
app_settings = AppSettings()
mongodb_settings = MongoDBSettings()
monogo_vector_settings = MonogoVectorSettings()
qdrant_settings = QdrantSettings()
google_settings = GoogleSettings()
supabase_settings = SupabaseSettings()
token_settings = TokenSettings()
classifier_settings = ClassifierSettings()
azure_embeddings_settings = AzureEmbeddingsSettings()