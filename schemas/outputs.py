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
    # Used to validate category, authenticity, severity, and reasoning.

    model_config = ConfigDict(extra="forbid")

    # Main incident category selected by the Classifier.
    category: CategoryType

    # How believable/specific the report is.
    # 0 = very weak/unreliable, 1 = highly specific/reliable.
    authenticity_score: float = Field(ge=0, le=1)

    # How serious the incident seems.
    # 0 = very minor, 1 = very severe.
    severity: float = Field(ge=0, le=1)

    # Short explanation for the chosen category and scores.
    reasoning: str


class DecisionOutput(BaseModel):
    # Output format for the Decision Agent.
    model_config = ConfigDict(extra="forbid")

    decision: DecisionType
    status: StatusType
    decision_reason: str