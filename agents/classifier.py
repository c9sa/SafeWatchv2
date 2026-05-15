from openai import OpenAI

from prompts.classifier_prompt import CLASSIFIER_SYSTEM_PROMPT
from schemas.outputs import ClassifierOutput
from schemas.messages import AgentMessage
from schemas.state import SafeWatchState


client = OpenAI()


def run_classifier(state: SafeWatchState) -> dict:
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": CLASSIFIER_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""

Cleaned Incident:
{state.cleaned_content}

Location:
{state.location_text}

Normalized Time:
{state.normalized_time}

Original raw post for backup:
{state.raw_text}
""",
            },
        ],
        text_format=ClassifierOutput,
    )

    classifier_output = response.output_parsed

    if classifier_output is None:
        return {
        "category": "other",
        "authenticity_score": 0.0,
        "severity": 0.0,
        "messages": [
            AgentMessage(
                agent="Classifier",
                content="Classifier failed to return valid structured output.",
                reasoning="Fallback values were used so the pipeline could continue.",
            )
        ],
    }

    return {
        "category": classifier_output.category,
        "authenticity_score": classifier_output.authenticity_score,
        "severity": classifier_output.severity,
        "messages": [
            AgentMessage(
                agent="Classifier",
                content="Classifier assigned category, authenticity score, and severity score.",
                reasoning=classifier_output.reasoning,
            )
        ],
    }