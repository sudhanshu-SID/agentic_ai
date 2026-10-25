import os 
import json 
from dotenv import load_dotenv, find_dotenv
from google import genai
from pydantic import BaseModel 
from states import AgencyState

load_dotenv(find_dotenv())

# Initialize GenAI client using the GEMINI_API_KEY from environment
client = genai.Client(api_key = os.environ.get("GEMINI_API_KEY"))

# Pydantic schema enforcing structured JSON output for the expert review
class ExpertReview(BaseModel):
    critique: str
    needs_revision: bool 
    final_draft: str 

def expert_agent(state: AgencyState) -> dict:
    """
     Worker Agent 3: The expert critic & editor 
     Role: 
        - Reviews 'writer_notes' against 'research_notes' and 'topic'.
        - Evaluates factual fidelity, engagement, hooks, and tone.
        - If revision_count < 1 and changes are needed -> flags needs_revision = True.
        - If revision_count >=1 or draft is great -> finalize script into final_draft.
     """

    # Extract required inputs from the shared blackboard state
    topic = state.get("topic", "")
    research_notes = state.get("research_notes", "")
    writer_notes = state.get("writer_notes", "")
    revision_count = state.get("revision_count", 0)

    # Defensive check: ensure there is a draft to review before calling LLM
    if not writer_notes:
        return {
            "expert_notes": "Error: No draft available to critique.",
            "needs_revision": False,
            "final_draft": ""
        }
    
    # Cap loop at 1 revision cycle: only allow revision if revision_count < 1
    can_request_revision = (revision_count < 1)

    prompt = f""" 
    You are a world-class viral travel video director and editor, specializing in high-retention cinematic Instagram Reels and YouTube Shorts (in the style of Sankho Kun, Rohit CB, and Ajay Raj).

    Topic: {topic}
    Verified Research Notes:
    {research_notes}

    Writer's Script Draft: 
    {writer_notes}

    Current Revision Pass: {revision_count} 
    Can Request Revision: {can_request_revision}

    EVALUATION CRITERIA (Reel Standards: 30–75 Seconds):
    1. 🎣 3-Second Hook: Does it immediately seize attention with tension or contrarian curiosity? Reject any generic "Hey guys" or weak intros.
    2. ⏱️ Duration & Word Count: Is spoken narration strictly 120–180 words (suitable for a 30–75s reel)? Reject long-form essays or 7-8 min scripts!
    3. 🎥 Cinematic & Sensory Storytelling: Are there clear [VISUAL] and [SFX / AUDIO] tags? Does it describe taste, aroma, steam, and atmosphere rather than just listing spots?
    4. 🔍 Factual Fidelity: Did the writer hallucinate places or facts NOT in the verified research notes?

    INSTRUCTIONS:
    - In 'critique': Provide sharp, direct feedback on the hook, word count / timing, sensory cues, and flow.
    - In 'needs_revision': 
        - If 'Can Request Revision' is TRUE AND (script is too long, hook is weak, lacks sensory cues, or has factual errors) -> set to TRUE.
        - If 'Can Request Revision' is FALSE, OR the script already hits elite Reel standards -> set to FALSE.
    - In 'final_draft':
        - If 'needs_revision' is FALSE, produce the final, perfectly formatted publication-ready Reel script with all [VISUAL], [SFX], and [VOICEOVER] tags.
        - If 'needs_revision' is TRUE, leave this as an empty string (writer will revise next).
    """
    print(f" [Expert] Reviewing draft (Revision Pass: {revision_count})...")

    try:
        # Invoke Gemini with structured JSON output enforced by the ExpertReview schema
        response = client.models.generate_content(
            model = "gemini-3.8-flash",
            contents = prompt,
            config = {
                "response_mime_type": "application/json",
                "response_schema": ExpertReview,
            }
        )

        # Access the parsed Pydantic object directly from the SDK response
        review: ExpertReview = response.parsed

        print(f" [Expert] Review complete! Needs revision? -> {review.needs_revision}")

        # Return the updated dictionary keys corresponding to AgencyState
        return {
            "expert_notes": review.critique,
            "needs_revision": review.needs_revision,
            "final_draft": review.final_draft
        }

    except Exception as e:
        # Graceful degradation: log the error and pass the writer's draft through as final draft so the pipeline doesn't break
        print(f"⚠️ [Expert Error]: {e}")
        return {
            "expert_notes": f"Expert review encountered an error: {e}",
            "needs_revision": False,
            "final_draft": writer_notes
        }

if __name__ == "__main__":
    test_state: AgencyState = {
        "topic": "Hidden gems in Kyoto",
        "research_notes": "Otagi Nenbutsu-ji has 1,200 whimsical stone statues. Giou-ji is a quiet moss garden temple.",
        "writer_notes": "Hey guys! Today we are visiting Tokyo Tower and going shopping in Ginza!",  # Hallucinated / off-topic draft to trigger critique
        "expert_notes": "",
        "revision_count": 0,
        "needs_revision": False,
        "final_draft": "",

    }

    result = expert_agent(test_state)
    print("\n--- EXPERT REVIEW RESULT ---")
    print(f"Needs Revision: {result['needs_revision']}")
    print(f"Critique:\n{result['expert_notes']}")
    print(f"Final Draft:\n{result['final_draft']}")