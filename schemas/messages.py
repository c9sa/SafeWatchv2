# Defines the standard format for agent messages, feedback, reasoning logs, and trace entries (trace not yet implmented)

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


# Allowed agent names in the system.
# Using Literal prevents typo names like "decision_agent" or "classifer".
AgentName = Literal[
    "Crawler",
    "Cleaner",
    "Classifier",
    "Decision Agent",
    "Retry Controller",
    "System",
]



#Normal Message Format
class AgentMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent: AgentName
    content: str
    reasoning: Optional[str] = None
    decision_reason: Optional[str] = None
    attempt_number: int = Field(default=1, ge=1)


#Msg format for Agent FEEDBACK to another agent
class FeedbackMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_agent: AgentName
    to_agent: AgentName
    feedback: str
    reason: Optional[str] = None
    attempt_number: int = Field(default=1, ge=1)


#Message format for REASONING
class ReasoningLog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent: AgentName
    reasoning: str
    evidence: Optional[list[str]] = Field(default_factory=list)
    attempt_number: int = Field(default=1, ge=1)

