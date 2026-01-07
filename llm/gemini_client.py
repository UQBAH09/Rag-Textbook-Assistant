import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# Load .env once
load_dotenv()

# Initialize client once
_API_KEY = os.getenv("GEMINI_API_KEY")
if not _API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

_client = genai.Client(api_key=_API_KEY)

_MODEL_NAME = "models/gemini-flash-latest"


def generate_text(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated text.
    """
    try:
        response = _client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
        )
        return response.text.strip()

    except ClientError as e:
        # Graceful error handling
        return f"[Gemini Error] {e}"
