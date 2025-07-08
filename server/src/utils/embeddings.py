from typing import List
import numpy as np



from src.core.config import azure_embeddings_settings
from openai import AzureOpenAI
from typing import List, Union


def get_embedding_3_large_simple(text: str) -> np.ndarray:
    """
    A simplified version of get_embedding_3_large that generates embeddings using text-embedding-3-large model.
    
    Args:
        text (str): Input text to generate embedding for
        
    Returns:
        np.ndarray: The embedding vector for the input text as a numpy array
    """
    client = AzureOpenAI(
        api_key=azure_embeddings_settings.AZURE_EMBDEDDINGS_API_KEY,
        api_version=azure_embeddings_settings.AZURE_EMBDEDDINGS_API_VERSION,
        azure_endpoint=azure_embeddings_settings.AZURE_EMBDEDDINGS_ENDPOINT,
        azure_deployment=azure_embeddings_settings.AZURE_EMBDEDDINGS_DEPLOYMENT
    )
    
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-large"
    )
    embedding = np.array(response.data[0].embedding)
    return embedding.tolist() 
    

      