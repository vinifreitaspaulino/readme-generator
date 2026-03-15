from google import genai

def gemini(prompt: str, model: str, api_key: str) -> str:
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    
    return response.text.strip()