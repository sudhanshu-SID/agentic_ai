import os 
import chromadb
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key = os.environ.get("GEMINI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    """
    Helper function to get the vector for a piece of text. 
     """

    response = client.models.embed_content(
        model = "gemini-embedding-2",
        contents = text
     )

    return response.embeddings[0].values

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name = "company_policies")

chunks = [
    "Employee can work remotely 3 days a week. Tuesdays and Thursdays are  mandatory in-office days.",
    "Every employee gets 20 days of paid tie off(PTO) per year. ",
    "Upon joining, you will receive a laptop and a 500 stipend for your home office. "
]

print("Embedding chunks and saving to the databases...")

for i, chunk in enumerate(chunks):
    vector = get_embedding(chunk)

    collection.add(
        documents = [chunk],
        embeddings = [vector],
        ids = [f"Chunk: {i}"]
    )

print("Documents embedded successfully.")

user_question = "Do I get work from home in this job, and for how many days do i have to work from office.? "
print(f"user question: `{user_question}`\n")

question_vector = get_embedding(user_question)

results = collection.query(
    query_embeddings = [question_vector],
    n_results = 1
)

print("Assembling context and asking the Ai, wait for the result....")

retrived_chunk = results["documents"][0][0]
retrived_id = results["ids"][0][0]

prompt = f"""
You are a helpful HR assistant. Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't know based on the company polices.

CRITICAL INSTRUCTION: you MUST cite the source ID at the end of you answer in brackets,
and if you don't find any source simply say, "there is no source for this".

Source ID: {retrived_id}
context: {retrived_chunk}

user question {user_question}
 """

chat = client.chats.create(
    model = "gemini-3.5-flash",
    config = types.GenerateContentConfig(temperature = 0.0)

)
response = chat.send_message(prompt)
print("Final response: ", response.text)