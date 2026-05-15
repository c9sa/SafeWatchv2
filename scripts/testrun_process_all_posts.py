# python -m scripts.testrun_process_all_posts

from services.db_readwrites import get_all_raw_posts
from pipeline.process_post import process_raw_post


if __name__ == "__main__":
    raw_posts = get_all_raw_posts()

    print(f"Found {len(raw_posts)} raw posts.")

    success_count = 0
    fail_count = 0

    for raw_post in raw_posts:
        raw_post_id = raw_post["id"]

        try:
            result = process_raw_post(raw_post_id)

            print("Processed:", result["raw_post_id"])
            print("Incident:", result["incident_id"])
            print("---")

            success_count += 1

        except Exception as e:
            print("Failed:", raw_post_id)
            print("Error:", e)
            print("---")

            fail_count += 1

    print("Finished processing all raw posts.")
    print("Success:", success_count)
    print("Failed:", fail_count)