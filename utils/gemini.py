# app/utils/gemini.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
# Set your Gemini API key

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")



# Initialize the Gemini client
client = genai.Client()

def query_gemini(prompt: str) -> str:
    """Send a prompt to Gemini LLM and return text."""
    if not prompt.strip():
        return ""  # Don't send empty queries

    # Generate response using the model
    response = genai.models.generate(
        model="gemini-2.5",
        temperature=0.7,
        candidate_count=1,
        prompt=prompt
    )

    # Return the text output
    return response.candidates[0].content