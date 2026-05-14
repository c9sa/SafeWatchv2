from services.db_readwrites import insert_raw_post, create_incident
from schemas.messages import AgentMessage
from services.db_readwrites import insert_agent_message, update_incident


# Test DB operations - ISNERT, CREATE INCIDENT, UPDATE

raw_post = insert_raw_post(
    raw_text="Fight spotted near Clarke Quay last night. Police arrived.",
    source_platform="reddit",
    source_url="https://reddit.com/test",
    timestamp_text="last night",
)

print("Inserted raw post:", raw_post["id"])

incident = create_incident(raw_post_id=raw_post["id"])

print("Created incident:", incident["id"])

update_incident(
    incident_id=incident["id"],
    updates={
        "cleaned_content": "A fight was reported near Clarke Quay.",
        "location_text": "Clarke Quay",
        "category": "public_disorder",
        "authenticity_score": 0.7,
        "severity": 0.6,
        "status": "processed",
        "decision": "publish",
        "decision_reason": "Clear local safety incident with location and event details.",
    },
)

insert_agent_message(
    incident_id=incident["id"],
    message=AgentMessage(
        agent="Cleaner",
        content="Cleaner extracted the incident summary and location.",
        reasoning="The post mentioned Clarke Quay and a fight.",
    ),
)

print("DB test completed.")