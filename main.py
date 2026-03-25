from dotenv import load_dotenv
import os
from google import genai

# Load .env file
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Generate response
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain black holes simply"
)

print(response.text)