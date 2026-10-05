import os 
from dotenv import load_dotenv
from tavily import TavilyClient
 
load_dotenv()

tavily_client = TavilyClient(api_key = os.environ.get("TAVILY_API_KEY"))

print("Searching the web for the latest web news")
response = tavily_client.search("What is the latest news from antrophic")

print("---SEARCH RESULTS")
print(response)