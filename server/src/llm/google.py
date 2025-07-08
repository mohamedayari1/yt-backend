import google.generativeai as genai
from app.llm.base import BaseLLM
from app.core.config import google_settings

class GoogleLLM(BaseLLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genai.configure(api_key=google_settings.GOOGLE_API_KEY)
        self.client = genai.GenerativeModel("gemini-1.5-flash-latest")
        
    def _raw_gen(self, messages, *args, **kwargs):
        # Convert messages to Gemini format
        formatted_messages = ""
        for message in messages:
            role = message.get('role', '')
            content = message.get('content', '')
            if role == 'system':
                formatted_messages += f"System: {content}\n"
            elif role == 'user':
                formatted_messages += f"User: {content}\n"
            elif role == 'assistant':
                formatted_messages += f"Assistant: {content}\n"
        
        response = self.client.generate_content(formatted_messages)
        return response.text

