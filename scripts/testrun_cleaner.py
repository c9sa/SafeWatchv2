# python -m scripts.testrun_cleaner

from agents.cleaner import run_cleaner
from schemas.state import SafeWatchState


state = SafeWatchState(
    raw_text="wah siao fight outside cck just now police came also",
    source_platform="reddit",
    source_url="https://reddit.com/test",
    timestamp_text=None,
)

result = run_cleaner(state)

print(result)