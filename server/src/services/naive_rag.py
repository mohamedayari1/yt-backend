import sys
sys.path.insert(0, "/home/mohamed-ayari/projects/youtube-chatbot/server")  # Adjust the path to import from app.llm.base
 


from typing import List, Dict, Tuple, Any, Set

from src.vectorstore.mongo_vectordb import MongoVectorRetriever

from src.llm.azure_openai import OpenAILLM
from src.utils.helpers import process_history, get_last_n_questions_from_history, is_follow_up, query_expansion, deduplicate_docs
from src.utils.logging import get_logger

import asyncio


logger = get_logger("naive_rag")

class NaiveRAG:
    """
    A retriever class that expands the query, retrieves documents from a 
    vector store and MongoDB, and then reranks the results before generating 
    a final response using an LLM.
    """

    def __init__(
        self,
        question: str,
        chat_history: List[Tuple[str, str]],
        prompt: str,
        chunks: int = 3,
        token_limit: int = 150,
    ):
        """
        Initialize the ClassicRAG retriever.

        :param question: The user's question
        :param selected_language: Language code (e.g. 'en', 'de')
        :param chat_history: Previous user-chatbot interactions
        :param prompt: The system prompt template
        :param chunks: Number of documents to retrieve
        :param token_limit: Token limit for the model
        """
        self.question = question
        self.chat_history = chat_history
        self.prompt = prompt
        self.chunks = chunks
        self.token_limit = token_limit

    async def _get_data(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from the vector store and MongoDB.

        :param query: The expanded query string
        :return: A list of document dictionaries
        """
        if self.chunks == 0:
            return []

        retriever = MongoVectorRetriever(law_type="youtube_data")
        
        youtube_docs = retriever.search(query, k=self.chunks)
   
        # Process retrieved documents based on selected language
        docs = []
        for doc in youtube_docs:
            chunk = doc.get("chunk_content", "")
            

            docs.append({
                "title": "Secrets of the Houses",
                "text": chunk,
                "source": "https://www.youtube.com/watch?v=743J50ACNHM&list=PLE-tFlushJYm8zMsDqHa8grfuFi63W0Sv",
            })

        logger.info(f"Retrieved {len(docs)} documents for query")
        return docs


    async def gen(self) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Generate a response by:
          1. Expanding the query
          2. Retrieving and reranking documents (in parallel)
          3. Combining them into a prompt for the LLM
          4. Returning the completion and the documents

        :return: A tuple of (completion text, list of doc dicts)
        """
        # Expand query
        if is_follow_up(self.question):
            logger.info(f"*******Follow-up question detected; using original question for query expansion: \n: {self.question}")
            last_questions = get_last_n_questions_from_history(self.chat_history, 5)
            list_query_expansion = query_expansion(self.question, 2,  is_follow_up=True, questions_history=last_questions)
        else:
            list_query_expansion = query_expansion(self.question, 2)

        # Retrieve documents for all expanded queries in parallel
        logger.info(f"Retrieving data for {len(list_query_expansion)} queries in parallel")
        
        # Create tasks for parallel execution
        retrieval_tasks = [
            self._get_data(expanded_query) 
            for expanded_query in list_query_expansion
        ]
        
        # Execute all retrieval tasks concurrently
        retrieval_results = await asyncio.gather(*retrieval_tasks, return_exceptions=True)
        
        # Process results and handle any exceptions
        all_docs = []
        for i, result in enumerate(retrieval_results):
            if isinstance(result, Exception):
                logger.error(f"Error retrieving data for query {i}: {result}")
                continue
            
            logger.info(f"Retrieved {len(result)} documents for query {i}: {list_query_expansion[i]}")
            all_docs.extend(result)
        
        # Deduplicate the results from all queries
        deduplicated_docs = deduplicate_docs(all_docs)
        logger.info(f"Original docs count: {len(all_docs)}, after deduplication: {len(deduplicated_docs)}")

        # Extract text for reranking
        docs_text = [doc["text"] for doc in deduplicated_docs]
        

        # Combine docs for the prompt
        docs_together = "\n\n\n".join(docs_text)
        
        final_prompt = self.prompt.replace("{summaries}", docs_together)  
        
        messages_combine = [{"role": "system", "content": final_prompt}]

        # Process history
        processed_history = process_history(self.chat_history)
        if processed_history:
            for user_msg, bot_msg in processed_history:
                messages_combine.extend([
                    {"role": "user", "content": user_msg},
                    {"role": "system", "content": bot_msg},
                ])

        # Add the current question
        messages_combine.append({"role": "user", "content": self.question})
        

        # Generate final response
        llm = OpenAILLM()

        
        completion = llm.gen(model="chat", messages=messages_combine)
        logger.info(f"LLM response: {completion}")




        return completion, deduplicated_docs


if __name__ == "__main__":
    # Example usage
    question = "What are the labor laws in Germany?"
    chat_history = [
        ("What is the minimum wage?", "The minimum wage in Germany is 9.60 EUR per hour."),
        ("Are there any exceptions?", "Yes, there are exceptions for certain industries.")
    ]
    prompt = "You are a legal expert. Answer the question based on the provided summaries:\n\n{summaries}"

    rag = NaiveRAG(question, chat_history, prompt, chunks=3, token_limit=150)
    
    # Run the generator
    asyncio.run(rag.gen())