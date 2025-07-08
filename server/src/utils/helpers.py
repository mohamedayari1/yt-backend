import json
from typing import List, Tuple
from typing import Dict, Any, Set, List

from src.llm.azure_openai import OpenAILLM
_encoding = None




def process_history(history) -> List[Tuple[str, str]]:
    """
    Processes the history JSON string or list and returns a list of (prompt, response) tuples.

    Args:
        history: A JSON string containing the history of prompts and responses, or already a list of tuples.

    Returns:
        List[Tuple[str, str]]: A list of tuples, where each tuple is (prompt, response).
    """
    try:
        # If it's already a list, return it directly
        if isinstance(history, list):
            return history
            
        # Parse the JSON string into a Python list
        history_list = json.loads(history)
        
        # Extract the prompt-response pairs
        prompt_response_pairs = [
            (entry.get("prompt", ""), entry.get("response", ""))
            for entry in history_list
        ]
        
        return prompt_response_pairs
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"Error decoding JSON: {e}")
        return []




def get_last_n_questions_from_history(history, n: int = 10) -> List[str]:
    """
    Extracts the last n questions from the history JSON string or list.

    Args:
        history: A JSON string containing the history of prompts and responses, or already a list of tuples.
        n (int): Number of last questions to retrieve (default: 3).

    Returns:
        List[str]: A list of the last n questions/prompts.
    """
    try:
        # Use the existing process_history function
        prompt_response_pairs = process_history(history)
        
        # Extract only the prompts (questions) and get the last n
        questions = [prompt for prompt, response in prompt_response_pairs]
        
        # Return the last n questions
        return questions[-n:] if len(questions) >= n else questions
    except Exception as e:
        print(f"Error extracting questions from history: {e}")
        return []


def flatten(nested_list: list) -> list:
    """Flatten a list of lists into a single list."""

    return [item for sublist in nested_list for item in sublist]

def is_follow_up(user_message: str) -> bool:
    question = f"""
            Classify the following user message as either 'follow-up' or 'standalone':\n\n"
            User message: \{user_message}\n\n"
            Answer with just 'follow-up' or 'standalone'.
    """
    llm = OpenAILLM()

    messages_combine = [{
        "role": "system",
        "content": """
            You're a helpful assistant that classifies whether a user message in a conversation 
            is a follow-up question that refers to previous context, or a standalone question.
    """
}]
    messages_combine.append({"role": "user", "content": question})
    
    completion = llm.gen(model="chat", messages=messages_combine)
    
    return completion.strip().lower() == "follow-up"
    
    

def query_expansion(question: str,
                    to_expand_to_n: int,
                    is_follow_up: bool = False,
                    questions_history: List[str]= None,
                    target_language: str = "English") -> list[str]:
    
    llm = OpenAILLM()
    
    # Build context for follow-up questions
    context_prompt = ""
    if is_follow_up and questions_history:
        history_text = "\n".join([f"- {q}" for q in questions_history])
        context_prompt = f"""
        
        IMPORTANT: This is a follow-up question in an ongoing conversation. 
        Previous questions in this conversation:
        {history_text}
        
        When generating the expanded queries, consider the context from previous questions to ensure the keywords and terminology used will help retrieve relevant chunks that build upon the conversation history.
        """
    
    messages_combine = [{"role": "system", 
                         "content": f"""You are a Professional Astronomie expert like Joni Patry.
                         You will receive a user query and you will generate {to_expand_to_n} different versions  of the received query .
                         In the generated queries, you should use different words and phrases to express the same meaning as the original query.
                        You should not change the meaning of the original query.
                        You should not add any new information or change the context of the original query.
                         
                        YOU MUST PROVIDE THE GENERATED QUERIES IN ENGLIHSH.
                        
                        Provide these alternative questions seperated by |||.
                                    """}]
    messages_combine.append({"role": "user", "content": question})
    
    completion = llm.gen(model="chat", messages=messages_combine)
    list_output = completion.split('|||')
    return list_output



def deduplicate_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate documents based on their text content.
    
    :param docs: List of document dictionaries
    :return: Deduplicated list of documents
    """
    seen_texts: Set[str] = set()
    deduplicated_docs = []
    
    for doc in docs:
        # Create a normalized version of the text for comparison
        text = doc["text"].strip()
        if not text or text in seen_texts:
            continue
            
        seen_texts.add(text)
        deduplicated_docs.append(doc)
        
    return deduplicated_docs

# # Example usage
# history = '[{"prompt": "Who invented the telephone?", "response": "Alexander Graham Bell is credited with inventing the telephone."}, {"prompt": "What is the capital of France?", "response": "The capital of France is Paris."}]'

# pairs = process_history(history)
# print(pairs)
