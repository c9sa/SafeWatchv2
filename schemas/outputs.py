# OUTPUT formats for ALL AGENTS

from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


CategoryType = Literal[
    "theft",
    "burglary",
    "robbery",
    "assault",
    "violent_crime",
    "vandalism",
    "scam_fraud",
    "identity_document_fraud",
    "harassment_threat",
    "sexual_offense",
    "suspicious_activity",
    "public_disorder",
    "regulatory_offence",
    "drug_offence",
    "traffic_transport_offence",
    "other",
]

DecisionType = Literal["publish", "reject", "needs_retry"]
StatusType = Literal["queued", "processing", "processed", "rejected"]


class CleanerOutput(BaseModel):
    # Output format for the Cleaner agent.
    model_config = ConfigDict(extra="forbid")

    cleaned_content: str
    location_text: Optional[str] = None
    timestamp_text: Optional[str] = None
    normalized_time: Optional[str] = None
    reasoning: str


class ClassifierOutput(BaseModel):
    # Output format for the Classifier agent.
    model_config = ConfigDict(extra="forbid")

    category: CategoryType
    authenticity_score: float = Field(ge=0, le=1)
    severity: float = Field(ge=0, le=1)
    reasoning: str


class DecisionOutput(BaseModel):
    # Output format for the Decision Agent.
    model_config = ConfigDict(extra="forbid")

    decision: DecisionType
    status: StatusType
    decision_reason: str