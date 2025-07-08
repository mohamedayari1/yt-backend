import sys
sys.path.insert(0, "/home/mohamed-ayari/projects/youtube-chatbot/server")  # Adjust the path to import from app.llm.base
 
from pymongo.operations import SearchIndexModel
import time

from src.core.config import monogo_vector_settings
from src.core.mongo_client import connection

from src.vectorstore.base import BaseVectorStore
from src.utils.embeddings import get_embedding_3_large_simple
from src.utils.logging import get_logger


logger = get_logger(__name__)

_database = connection.get_database(monogo_vector_settings.MONGO_VECTORDATABASE_NAME)
collection = _database[monogo_vector_settings.LABOR_LAW_COLLECTION_NAME]

class MongoVectorRetriever(BaseVectorStore):

    def __init__(self, law_type) -> None:
        self._client = connection.get_database(monogo_vector_settings.MONGO_VECTORDATABASE_NAME)
        self.law_type = law_type
        
    def search(self, query: str, k: int) -> list:
        if self.law_type == "youtube_data":
            logger.info("Similarity Search on  labor law collection")
            collection = self._client[monogo_vector_settings.LABOR_LAW_COLLECTION_NAME]
            
        
        elif self.law_type == "immigration_law":
            logger.info("Similarity Search on  immigration law collection")
            collection = self._client[monogo_vector_settings.IMMIGRATION_LAW_COLLECTION_NAME]
            
        return self._search_single_query(query, k, collection)
        
    
    def _search_single_query(self, question, k=2, collection=None):
            query_vector = get_embedding_3_large_simple(question)
            

            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "queryVector": query_vector,
                        "path": "embedding",
                        "exact": True,
                        "limit": k,
                    }
                }, {
            "$project": {
              "_id": 1,
              "chunk_content": 1,
              "score": { "$meta": "vectorSearchScore" }
         }
      }
            ]

            cursor = collection.aggregate(pipeline)

            results = []
            for doc in cursor:

                results.append(doc)
            logger.info("All documents retrieved successfully from MongoVectorDB.", num_documents=len(results))

            return results
        
if __name__ == "__main__":

    retriever = MongoVectorRetriever("youtube_data")
    collection = retriever._client[monogo_vector_settings.LABOR_LAW_COLLECTION_NAME]
    doc_count = collection.count_documents({})
    print(f"Number of documents in labor_law_vectors collection: {doc_count}")
    

    start_time = time.time()
    results = retriever.search("What family relationships are primarily governed by the fourth house?", 1)
    end_time = time.time()
    
    print(results)
