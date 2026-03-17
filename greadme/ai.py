from google import genai
from openai import OpenAI

def ai_api(provider: str, prompt: str, model: str, api_key: str) -> str:

    return

def gemini(prompt: str, model: str, api_key: str) -> str:
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    
    return response.text.strip(), response.usage_metadata.total_token_count