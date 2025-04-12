import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_text_with_gpt(text: str) -> dict:
    """Analyze text for snarkiness using GPT-4"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """
                You are a snark detection system. Analyze the given text for snarkiness and respond ONLY with a JSON object in this exact format:
                {
                    "score": <number between 0-100>,
                    "phrases": [
                        {
                            "phrase": "<detected snarky phrase>",
                            "context": "<explanation of why it's snarky>",
                            "score": <number between 0-10>
                        }
                    ]
                }
                
                If no snarky phrases are detected, return an empty array for "phrases".
                """},
                {"role": "user", "content": text}
            ]
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "score": 0,
                "phrases": []
            }
            
    except Exception as e:
        raise Exception(f"GPT analysis failed: {str(e)}") 