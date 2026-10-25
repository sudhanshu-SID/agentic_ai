import os
import sys
from dotenv import load_dotenv, find_dotenv
from google import genai
from states import AgencyState

# Ensure console supports UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(find_dotenv())

client = genai.Client(api_key = os.environ.get("GEMINI_API_KEY"))


def writer_agent(state: AgencyState) -> dict:

    """
    Worker Agent 2: The ScriptWriter
    Role:
    Mode 1(INITIAL DRAFT):
        -Reads 'topic' and 'research_notes' from state.
        - Transform factual research into an enaging, video-oriented script with a good engaing hook.
        - Returns {'writer_notes': ...} to the clipboard.
    Mode 2(REVISION):
        - if 'expert_notes' exist, revise the existing draft to fix issues flagges by the Expert critic.
        - Returns {'writer_notes': ...} to the shared clipboard.
    """
    topic = state.get("topic", "")
    research_notes = state.get("research_notes", "")
    previous_draft = state.get("writer_notes", "")
    expert_notes = state.get("expert_notes", "")

    if not research_notes:
        return {"writer_notes": "Error: No research notes provided to write from."}

    if expert_notes:
        print("[Writer] [Revision Mode] Refining Reel script to Sankho Kun / Rohit CB standard...")

        prompt = f"""
        You are a top-tier cinematic travel filmmaker and viral reel scriptwriter, deeply inspired by the visual poetry and rhythm of Sankho Kun, Rohit CB, and Ajay Raj.

        Topic: {topic}
        Verified Research Notes:
        {research_notes}

        Previous Draft:
        {previous_draft}

        Expert Critic Feedback:
        {expert_notes}

        TASK:
        Revise the script draft to address EVERY critique point while keeping it strictly in high-retention Instagram Reel / Short format (30–75 seconds runtime, 120–180 spoken words max).

        REEL STRUCTURE:
        1. 🎣 0-3s Magnetic Hook: Contrarian statement, tension, or curiosity gap with [VISUAL] + [AUDIO/SFX]. Never start with generic greetings.
        2. 🎥 Sensory Core (3-45s): Visceral street food textures, aromas, sound of sizzling pans or mountain breezes, intimate local interactions.
        3. 🧘 Emotional Closer (45-60s): Soulful reflection + a seamless "Save this for your next trip" CTA.
        4. 🎬 Production Cues: Clear tags for [VISUAL], [SFX / AUDIO], and [VOICEOVER].
        Do NOT introduce facts absent from the verified research notes.
        """
    else:
        print("[Writer] [Draft Mode] Crafting cinematic travel reel (Sankho Kun / Rohit CB style)...")
        prompt = f"""
        You are a top-tier cinematic travel filmmaker and viral reel scriptwriter, deeply inspired by the visual poetry and rhythm of Sankho Kun, Rohit CB, and Ajay Raj.

        Topic: {topic}
        Verified Research Notes:
        {research_notes}

        TASK:
        Write a high-retention, cinematic Instagram Reel / Short script (30 to 75 seconds runtime, 120 to 180 spoken words max).

        CREATIVE GUIDELINES:
        1. 🎣 Scroll-Stopping Hook (0-3s):
           - Start mid-action, with a curiosity gap or contrarian observation (e.g. "If you come here just for X, you're missing the real soul...").
           - NO generic intros ("Hey guys", "Welcome back"). Jump straight into the story.
        2. 🎬 Production Cues:
           - Explicitly tag [VISUAL] (camera angle, macro shot, motion blur, slow zoom).
           - Explicitly tag [SFX / AUDIO] (ambient sounds, sizzling oil, wind, lo-fi beat drop).
           - Explicitly tag [VOICEOVER] (conversational, soulful, rhythmic).
        3. 🥟 Sensory & Tactile Storytelling:
           - Don't just list places; describe the steam rising off the food, the crunch, the hidden wooden door in the back alley.
        4. ⏱️ Pacing & Brevity:
           - Strictly 120 to 180 spoken words so the creator can deliver it smoothly within 30 to 75 seconds.
        5. 🧘 Outro:
           - A poetic takeaway followed by a clean, natural call-to-action ("Save this before you plan your trip").
        """
    try:
        response = client.models.generate_content(
        model = "gemini-3.8-flash",
        contents = prompt
        )

        print("[Writer]: We are working on the script...")

        return {
            "writer_notes": response.text
        }

    except Exception as e:
    # Graceful degradation: log the error and pass the writer's draft through as final draft so the pipeline doesn't break
        print(f"[Writer Error]: {e}")
        fallback = previous_draft if previous_draft else f"writing failed due to an error: {e}"
        
        return {
            "writer_notes": fallback
        }

if __name__ == "__main__":
    test_state: AgencyState = {
         "topic": "Hidden gems in Kyoto",
        "research_notes": "Otagi Nenbutsu-ji has 1,200 whimsical stone statues.",
        "writer_notes": "Hey guys! We are at Tokyo Tower!",
        "expert_notes": "You wrote about Tokyo Tower instead of Kyoto. Please focus on Otagi Nenbutsu-ji.",
        "revision_count": 0,
        "needs_revision": True,
        "final_draft": "",
    }

    result = (writer_agent(test_state))
    print("\n", "---Writer Notes---\n")
    print("\n", result["writer_notes"])



    