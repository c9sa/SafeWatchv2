from openai import OpenAI

from prompts.cleaner_prompt import CLEANER_SYSTEM_PROMPT
from schemas.outputs import CleanerOutput
from schemas.messages import AgentMessage
from schemas.state import SafeWatchState


client = OpenAI()


# Runs the Cleaner Agent on raw Reddit text.
# Returns only the fields that should update the shared LangGraph state.
def run_cleaner(state: SafeWatchState) -> dict:
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": CLEANER_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
Raw post:
{state.raw_text}

Source URL:
{state.source_url}

Original timestamp text:
{state.timestamp_text}
""",
            },
        ],
        text_format=CleanerOutput,
    )

    cleaner_output = response.output_parsed

    return {
        "cleaned_content": cleaner_output.cleaned_content, # type: ignore
        "location_text": cleaner_output.location_text, # type: ignore
        "timestamp_text": cleaner_output.timestamp_text, # type: ignore
        "normalized_time": cleaner_output.normalized_time, # type: ignore
        "messages": [
            AgentMessage(
                agent="Cleaner",
                content="Cleaner extracted and normalized the raw post.",
                reasoning=cleaner_output.reasoning, # type: ignore
            )
        ],
    }