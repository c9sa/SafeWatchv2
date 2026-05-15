# Public entry point for processing one raw post.
# Actual workflow control is handled inside graph/workflow.py.

from typing import Any

from graph.workflow import graph
from schemas.state import SafeWatchState


# Triggers the LangGraph workflow for one raw post.
# Used by scripts, FastAPI endpoints, or future scheduled jobs.
def process_raw_post(raw_post_id: str) -> dict[str, Any]:
    initial_state = SafeWatchState(
        raw_post_id=raw_post_id,
    )

    result = graph.invoke(initial_state)
    return result


# Allows this file to be tested directly from the terminal.
if __name__ == "__main__":
    raw_post_id = input("Enter raw_post_id: ")

    result = process_raw_post(raw_post_id)

    print("Processing completed.")
    print(result)