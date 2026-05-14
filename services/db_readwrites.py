#ALLLLL database read and writes so agent nodes are not cluttered

from typing import Optional
from clients.supabase_client import get_supabase_client
from schemas.messages import AgentMessage
from typing import Any, Optional

supabase = get_supabase_client()


#INSERT CRAWLER output to DB
def insert_raw_post(
    raw_text: str,
    source_platform: str = "reddit",
    source_url: Optional[str] = None,
    timestamp_text: Optional[str] = None,
    reddit_post_id: Optional[str] = None,
) -> dict[str, Any] | None:
    """
    Insert original crawled post into raw_posts.
    Returns the inserted row.
    """
    data = {
        "source_platform": source_platform,
        "source_url": source_url,
        "raw_text": raw_text,
        "timestamp_text": timestamp_text,
        "reddit_post_id": reddit_post_id,
    }

    response = (
        supabase.table("raw_posts")
        .upsert(
            data,
            on_conflict="reddit_post_id",
            ignore_duplicates=True,
        )
        .execute()
    )

    if not response.data:
        return None

    return response.data[0] # type: ignore


#SELECT one raw post using ID
#Load the raw post before processing it
def get_raw_post(raw_post_id: str) -> dict:
    """
    Fetch one raw post by ID.
    """
    response = (
        supabase.table("raw_posts")
        .select("*")
        .eq("id", raw_post_id)
        .single()
        .execute()
    )

    return response.data # type: ignore

#SELECT ALLLL raw post using ID
#Load the raw post before processing it
def get_all_raw_posts() -> list[dict]:
    response = (
        supabase.table("raw_posts")
        .select("*")
        .execute()
    )

    return response.data  # type: ignore


#CREATE and INSERT an incident based on a raw_post
def create_incident(raw_post_id: str, status: str = "processing") -> dict:
    """
    Create incident row linked to a raw post.
    At first, most fields are empty.
    Agents will update it later.
    """
    data = {
        "raw_post_id": raw_post_id,
        "status": status,
    }

    response = (
        supabase.table("incidents")
        .insert(data)
        .execute()
    )

    return response.data[0] # type: ignore


# SELECT existing incident linked to a raw_post_id.
# Used to avoid creating duplicate incidents when reprocessing raw posts.
def get_incident_by_raw_post_id(raw_post_id: str) -> dict | None:
    response = (
        supabase.table("incidents")
        .select("*")
        .eq("raw_post_id", raw_post_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]  # type: ignore


#UPDATE exisitng incident with CLEANER/CLASSIFIER/DECISION results
#Used after each agent produces new incident information
def update_incident(incident_id: str, updates: dict) -> dict:
    """
    Update incident after cleaner/classifier/decision runs.
    """
    response = (
        supabase.table("incidents")
        .update(updates)
        .eq("id", incident_id)
        .execute()
    )

    return response.data[0] # type: ignore


#INSERT one agent message into agent_messages
#Used after each agent runs
def insert_agent_message(
    incident_id: str,
    message: AgentMessage,
) -> dict:
    """
    Save one agent message for frontend timeline.
    """
    data = {
        "incident_id": incident_id,
        "agent": message.agent,
        "content": message.content,
        "reasoning": message.reasoning,
        "decision_reason": message.decision_reason,
        "attempt_number": message.attempt_number,
    }

    response = (
        supabase.table("agent_messages")
        .insert(data)
        .execute()
    )

    return response.data[0] # type: ignore