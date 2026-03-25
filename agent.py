from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

print("API KEY:", os.getenv("OPENAI_API_KEY")[:20] + "..." if os.getenv("OPENAI_API_KEY") else "Not set")

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Introduce yourself"}]
)

print(response.choices[0].message.content)