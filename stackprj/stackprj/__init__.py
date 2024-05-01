import os
from dotenv import load_dotenv

load_dotenv()
# Access your API key
OPENAAI_API_KEY = os.getenv("OPENAI_API_KEY")