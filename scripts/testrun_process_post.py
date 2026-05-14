# python -m scripts.testrun_process_post

from pipeline.process_post import process_raw_post_with_cleaner


if __name__ == "__main__":
    raw_post_id = input("Enter raw_post_id: ")

    result = process_raw_post_with_cleaner(raw_post_id)

    print("Cleaner pipeline completed.")
    print("Raw post ID:", result["raw_post_id"])
    print("Incident ID:", result["incident_id"])
    print("Cleaner output:", result["cleaner_update"])