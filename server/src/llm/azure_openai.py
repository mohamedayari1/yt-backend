import sys
sys.path.insert(0, "/home/mohamed-ayari/projects/youtube-chatbot/server")  # Adjust the path to import from app.llm.base

from openai import AzureOpenAI
from typing import Iterator

from src.llm.base import BaseLLM
from src.core.config import llm_settings

class OpenAILLM(BaseLLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.client = AzureOpenAI(
            api_version=llm_settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=llm_settings.AZURE_OPENAI_ENDPOINT,
            api_key=llm_settings.AZURE_OPENAI_API_KEY
        )
    
    def _raw_gen(
        self,
        messages,
        **kwargs
    ): 
        response = self.client.chat.completions.create(
            model=kwargs.get('model', "chat"),
            messages=messages,
            stream=kwargs.get('stream', False)
        )
        return response.choices[0].message.content
    
    def _stream_gen(
        self,
        messages,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream response from Azure OpenAI
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional parameters
            
        Yields:
            str: Chunks of the response as they arrive
        """
        response = self.client.chat.completions.create(
            model=kwargs.get('model', "gpt-4o"),
            messages=messages,
            stream=True,
            **{k: v for k, v in kwargs.items() if k not in ['model', 'stream']}
        )
        
        for chunk in response:
            # Check if chunk has choices and the first choice has content
            if (chunk.choices and 
                len(chunk.choices) > 0 and 
                chunk.choices[0].delta and 
                chunk.choices[0].delta.content is not None):
                yield chunk.choices[0].delta.content
   
    def answer_query(self, query: str):
        answer = self._raw_gen(
            messages=[{"role": "user", "content": f"{query}"}],
            model="gpt-4o"
        )
        return answer
    
    def stream_answer_query(self, query: str) -> Iterator[str]:
        """
        Stream answer for a query
        
        Args:
            query: The user's question
            
        Yields:
            str: Chunks of the response as they arrive
        """
        for chunk in self._stream_gen(
            messages=[{"role": "user", "content": f"{query}"}],
            model="gpt-4o"
        ):
            yield chunk

if __name__ == "__main__":
    llm = OpenAILLM()
    
    # # Regular response
    # answer = llm._raw_gen(
    #     messages=[{"role": "user", "content": "What are the key features of the law?"}],
    #     model="gpt-4o"
    # )
    # print("Regular response:", answer)
    
    # Streaming response
    print("\nStreaming response:")
    for chunk in llm.stream_answer_query("What are the key features of the law?"):
        print(chunk, end='', flush=True)
    print()  # New line at the end