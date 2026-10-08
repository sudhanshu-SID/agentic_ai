import os 
from dotenv import load_dotenv, find_dotenv
from google import genai

load_dotenv(find_dotenv())

client = genai.Client(api_key = os.environ.get("GEMINI_API_KEY"))

def get_embedding(text: str):
    """
    Convert the text into a vector (list of numbers) using Gemini.

    """
    response  = client.models.embed_content(
    model = "gemini-embedding-2",
    contents = text
    )

    return response.embeddings[0].values

if __name__ == "__main__":
    text_to_embed = "Hello sir, how are you, Is there a holiday for tomorrow."

    print(f"original text: `{text_to_embed}`\n")

    vector = get_embedding(text_to_embed)

    print(f"vector dimension: {len(vector)}")

    # print(f"first 5 numbers: {vector[:5]}")

    