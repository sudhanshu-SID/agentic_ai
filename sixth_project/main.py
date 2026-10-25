import sys 
from states import AgencyState 
from researcher import research_agent 
from writer import writer_agent 
from expert import expert_agent  

# Ensure console supports UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_agency(topic: str) -> AgencyState:

    """ 
    Main Orchestrator Pipeline 
    Coordinates the sequential worker execution and conditional feedback loop.
     """

    print("\n" + "=" *50)
    print(f" STARTING TRAVEL CONTENT AGENCY PIPELINE")
    print(f" topic: {topic}")
    print("=" *50 + "\n")

    state: AgencyState = {
        "topic": topic,
        "research_notes": "",
        "writer_notes": "",
        "expert_notes": "",
        "revision_count": 0,
        "needs_revision": False,
        "final_draft": "",
    }

    research_update = research_agent(state)
    state.update(research_update)

    writer_update = writer_agent(state)
    state.update(writer_update)

    expert_update = expert_agent(state)
    state.update(expert_update)

    if state.get("needs_revision") and state.get("revision_count", 0) < 1:
        print("\n" + "-"*40)
        print("[pipeline manager] Expert flagged revisions needed!")
        print(f"Critique: \n {state['expert_notes']}")
        print("-"*40 + "\n")

        state["revision_count"] +=1

        revised_writer_update = writer_agent(state)
        state.update(revised_writer_update)

        final_expert_update = expert_agent(state)
        state.update(final_expert_update)

    print("\n" + "="*50)
    print("PIPELINE EXECUTION COMPLETED")
    print("="*50 + "\n")
        
    return state

if __name__ == "__main__":
    topic = "Hidden gems and street food secret in MANALI,HIMACHAL PRADESH, India"

    final_state = run_agency(topic)

    print("\n FINAL DELIVERED SCRIPT \n")
    print(final_state.get("final_draft")  or final_state.get("writer_notes"))