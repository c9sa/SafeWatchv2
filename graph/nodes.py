# Defines LangGraph node functions.
# Each function represents one step in the processing workflow.

from typing import Any

from agents.cleaner import run_cleaner
from agents.classifier import run_classifier
from schemas.state import SafeWatchState
from schemas.messages import AgentMessage

from services.db_readwrites import (
    get_raw_post,
    get_incident_by_raw_post_id,
    create_incident,
    update_incident,
    insert_agent_message,
)


# Loads the raw post from Supabase using raw_post_id.
def load_raw_post_node(state: SafeWatchState) -> dict[str, Any]:
    if state.raw_post_id is None:
        return {
            "status": "rejected",
            "decision_reason": "Missing raw_post_id.",
        }

    raw_post = get_raw_post(state.raw_post_id)

    return {
        "raw_post_id": raw_post["id"],
        "source_platform": raw_post.get("source_platform", "reddit"),
        "source_url": raw_post.get("source_url"),
        "raw_text": raw_post.get("raw_text"),
        "timestamp_text": raw_post.get("timestamp_text"),
        "status": "processing",
    }


# Checks whether this raw post already has an incident.
def check_existing_incident_node(state: SafeWatchState) -> dict[str, Any]:
    if state.raw_post_id is None:
        return {
            "status": "rejected",
            "decision_reason": "Missing raw_post_id.",
        }

    existing_incident = get_incident_by_raw_post_id(state.raw_post_id)

    if existing_incident is None:
        return {}

    return {
        "incident_id": existing_incident["id"],
        "status": "rejected",
        "decision_reason": "Incident already exists for this raw post.",
    }


# Creates a new incident row before agents run.
def create_incident_node(state: SafeWatchState) -> dict[str, Any]:
    if state.raw_post_id is None:
        return {
            "status": "rejected",
            "decision_reason": "Missing raw_post_id.",
        }

    incident = create_incident(
        raw_post_id=state.raw_post_id,
        status="processing",
    )

    return {
        "incident_id": incident["id"],
        "status": "processing",
    }


# Saves Cleaner + Classifier outputs and agent messages to Supabase.
def save_outputs_node(state: SafeWatchState) -> dict[str, Any]:
    if state.incident_id is None:
        return {
            "status": "rejected",
            "decision_reason": "Missing incident_id, cannot save outputs.",
        }

    # Convert invalid string null values from the LLM into real Python None.
    # Supabase timestamptz columns require None for SQL NULL, not "null" as text.
    normalized_time = state.normalized_time

    if isinstance(normalized_time, str) and normalized_time.strip().lower() in ["null", "none", ""]:
        normalized_time = None

    update_incident(
        incident_id=state.incident_id,
        updates={
            "cleaned_content": state.cleaned_content,
            "location_text": state.location_text,
            "normalized_time": normalized_time,
            "category": state.category,
            "authenticity_score": state.authenticity_score,
            "severity": state.severity,
            "status": "processing",
        },
    )

    for message in state.messages:
        if isinstance(message, dict):
            message = AgentMessage.model_validate(message)

        insert_agent_message(
            incident_id=state.incident_id,
            message=message,
        )

    return {
        "status": "processing",
    }


# Routes duplicate raw posts straight to END.
def route_after_existing_check(state: SafeWatchState) -> str:
    if state.decision_reason == "Incident already exists for this raw post.":
        return "end"

    return "create_incident"