from typing import TypedDict

class AgencyState(TypedDict):
    topic: str
    research_notes: str
    writer_notes: str
    expert_notes: str
    revision_count:int
    needs_revision: bool
    final_draft: str