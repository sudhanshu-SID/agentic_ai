import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

my_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = my_api_key)

response = client.models.generate_content(
    model = "gemini-3.5-flash-lite",

    contents = "hello, how are you, and is someone there"
)

print(response.text)