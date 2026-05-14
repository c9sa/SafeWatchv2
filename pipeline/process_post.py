from services.db_readwrites import (
    get_raw_post,
    get_incident_by_raw_post_id,
    create_incident,
    update_incident,
    insert_agent_message,
)
from agents.cleaner import run_cleaner
from schemas.state import SafeWatchState


# Processes one raw post through the Cleaner only.
# Used to connect raw_posts → Cleaner → incidents + agent_messages.
def process_raw_post_with_cleaner(raw_post_id: str) -> dict:
    # 1. Load raw post from Supabase
    raw_post = get_raw_post(raw_post_id)

    existing_incident = get_incident_by_raw_post_id(raw_post_id)

    # 2. Check if incident alr exists
    if existing_incident is not None:
        print("Skipping raw post. Incident already exists:", existing_incident["id"])
        return {
            "raw_post_id": raw_post_id,
            "incident_id": existing_incident["id"],
            "skipped": True,
            "reason": "Incident already exists for this raw post.",
        }

    # 3. Create incident row linked to raw post
    incident = create_incident(
        raw_post_id=raw_post["id"],
        status="processing",
    )

    # 4. Build initial pipeline state
    state = SafeWatchState(
        raw_post_id=raw_post["id"],
        incident_id=incident["id"],
        source_platform=raw_post.get("source_platform", "reddit"),
        source_url=raw_post.get("source_url"),
        raw_text=raw_post["raw_text"],
        timestamp_text=raw_post.get("timestamp_text"),
        status="processing",
    )

    # 5. Run Cleaner Agent
    cleaner_update = run_cleaner(state)

    # Convert invalid string null values from the LLM into real Python None.
    # Supabase timestamptz columns require None for SQL NULL, not "null" as text.
    normalized_time = cleaner_update.get("normalized_time")

    if isinstance(normalized_time, str) and normalized_time.strip().lower() in ["null", "none", ""]:
        normalized_time = None

    # 5. Update incident with Cleaner output
    updated_incident = update_incident(
        incident_id=incident["id"],
        updates={
            "cleaned_content": cleaner_update["cleaned_content"],
            "location_text": cleaner_update["location_text"],
            "normalized_time": normalized_time,
            "status": "processing",
        },
    )

    # 6. Save Cleaner message to agent_messages
    for message in cleaner_update["messages"]:
        insert_agent_message(
            incident_id=incident["id"],
            message=message,
        )

    # 7. Return useful debug output
    return {
        "raw_post_id": raw_post["id"],
        "incident_id": incident["id"],
        "cleaner_update": cleaner_update,
        "updated_incident": updated_incident,
    }