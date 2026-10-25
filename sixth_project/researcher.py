import os 
from dotenv import load_dotenv, find_dotenv
from google import genai
from tavily import TavilyClient
from states import AgencyState

load_dotenv(find_dotenv())

tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def research_agent(state: AgencyState) -> dict:
    """
    Worker Agent 1: The Researcher
    Role:
      - Reads the target 'topic' from the shared AgencyState.
      - Gathers fresh, real-world context using Tavily web search.
      - Uses Gemini to filter, synthesize, and structure findings into concise research notes.
      - Returns an update dictionary containing {"research_notes": ...}.
    """
    # Extract only the specific field required by this worker from the shared state
    topic = state.get("topic", "")
    print(f" [Researcher] Gathering web intelligence on: '{topic}'...")

    try:
        # Step 1: Query Tavily for live web search results on the topic
        search_result = tavily_client.search(query=topic)

        # Extract the list of search result items (title, url, snippet/content)
        raw_results = search_result.get("results", [])

        # Step 2: Formulate the prompt for Gemini, establishing persona and injecting raw search context
        prompt = f"""
        You are an expert travel researcher. 
        Topic: {topic}

        Here are raw search results from the web:
        {raw_results}

        Synthesize this information into clear, structured research notes:
        - Top attractions & hidden gems
        - Cultural insights and etiquette
        - Practical tips (transport, best season, food, mistakes, safety, things to avoid)
        """

        # Step 3: Send the prompt and search context to Gemini to synthesize clean notes
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        print("[Researcher] Research notes compiled successfully!")

        # Step 4: Return only the state field this agent is responsible for updating
        return {
            "research_notes": response.text
        }

    except Exception as e:
        # Graceful degradation: Log the exception and return an error message in state so the pipeline doesn't crash
        print(f" [Researcher Error]: {e}")
        return {
            "research_notes": f"Research failed due to an error: {str(e)}"
        }

# Local test runner to verify this agent in isolation before plugging it into the full agency
if __name__ == "__main__":
    # Initialize a mock state mimicking the user's initial input
    test_state: AgencyState = {
        "topic": "Hidden gems in kyoto",
        "research_notes": "",
        "writer_notes": "",
        "expert_notes": "",
        "final_draft": "",
    }

    # Run the researcher agent independently
    result = research_agent(test_state)

    # Print out the output to inspect the generated research notes
    print("\n-- RESEARCH NOTES --\n")
    print(result["research_notes"])
