from google import genai
from openai import OpenAI

def ai_api(provider: str, prompt: str, model: str, api_key: str) -> str:
    if provider == "gemini":
        response_text, total_token = gemini(prompt, model, api_key)
    elif provider == "groq":
        response_text, total_token = openai(prompt, model, api_key, base_url="https://api.groq.com/openai/v1")
    elif provider == "openai":
        response_text, total_token = openai(prompt, model, api_key)
    return response_text, total_token

def gemini(prompt: str, model: str, api_key: str) -> str:
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    
    return response.text.strip(), response.usage_metadata.total_token_count

def openai(prompt: str, model: str, api_key: str, base_url = None) -> str:
    client = OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content, response.usage.total_tokens

