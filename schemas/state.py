# Defines the shared LangGraph pipeline state passed between agents

from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
from schemas.messages import AgentMessage
from schemas.outputs import CategoryType, DecisionType, StatusType



class SafeWatchState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # CRAWLER output
    raw_post_id: Optional[str] = None
    source_platform: str = "reddit"
    source_url: Optional[str] = None
    raw_text: str
    timestamp_text: Optional[str] = None

    # Incident DB row
    incident_id: Optional[str] = None

    # CLEANER output
    cleaned_content: Optional[str] = None
    location_text: Optional[str] = None
    normalized_time: Optional[str] = None

    # CLASSIFIER output
    category: Optional[CategoryType] = None
    authenticity_score: Optional[float] = Field(default=None, ge=0, le=1)
    severity: Optional[float] = Field(default=None, ge=0, le=1)

    # DECISION output
    decision: Optional[DecisionType] = None
    status: StatusType = "queued"
    decision_reason: Optional[str] = None

    # Retry / Agent tracing
    retry_count: int = 0
    max_retries: int = 2
    messages: list[AgentMessage] = Field(default_factory=list)