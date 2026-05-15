from agents.classifier import run_classifier
from schemas.state import SafeWatchState

# python -m scripts.testrun_classifier

if __name__ == "__main__":
    state = SafeWatchState(
        raw_text="wah siao fight outside cq just now police came also",
        cleaned_content="There was a fight outside Clarke Quay just now, and police arrived.",
        location_text="Clarke Quay",
        timestamp_text="just now",
        normalized_time=None,
        status="processing",
    )

    result = run_classifier(state)

    print("Classifier test completed.")
    print("Category:", result["category"])
    print("Authenticity:", result["authenticity_score"])
    print("Severity:", result["severity"])
    print("Messages:", result["messages"])