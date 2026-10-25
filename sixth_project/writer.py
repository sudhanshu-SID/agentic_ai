import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from states import AgencyState

load_dotenv(find_dotenv())

client = genai.Client(api_key = os.environ.get("GEMINI_API_KEY"))


def writer_agent(state: AgencyState) -> dict:

    """
    Worker Agent 2: The ScriptWriter
    Role:
        -Reads 'topic' and 'research_notes' from state.
        - Transform factual research into an enaging, video-oriented script with a good engaing hook.
        - Returns {'writer_notes': ...} to the clipboard.
    """
    topic = state.get("topic", "")
    research_notes = state.get("research_notes", "")

    if not research_notes:
        return {"writer_notes": "Error: No research notes provided to write from."}

    prompt = f"""
    You are a elite youtube/video scriptwriter and travel storyteller.
    Topic: {topic}
    verified Research Notes: {research_notes}
    
    TASK:
    Draft an engaging, video-ready narrative draft based on the research notes above.

    GUIDELINES:
    - Stron Hook: Catch the viewr in the first 5 seconds.
    - Story Arc: Flow through attractions, culture, and practical tips with smooth transitons.
    - Grounded in Facts: Do not invent new facts or locations not present in the reasearch notes.
    - Call to action / Conclusion.
    """
    response = client.models.generate_content(
        model = "gemini-3.8-flash",
        contents = prompt
    )

    print("[Writer]: We are working on the script...")

    return {
        "writer_notes": response.text
    }

if __name__ == "__main__":
    test_state: AgencyState = {
        "topic": "Hidden gems in kyoto",
        "research_notes": "Otagi Nenbutsu-ji has 1200 mossy stone statues...",
        "writer_notes": "",
        "expert_notes": "",
        "final_draft": "",
    }

    result = (writer_agent(test_state))
    print("\n", "---Writer Notes---\n")
    print("\n", result["writer_notes"])



    