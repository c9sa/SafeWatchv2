from agents.fetcher import fetch_and_store_posts


# python -m scripts.testrun_fetcher

if __name__ == "__main__":
    inserted_posts = fetch_and_store_posts(
        subreddit="SingaporeRaw",
        sort="new",
        limit=5,
    )

    print("\n-- SUMMARY --")
    print(f"Inserted {len(inserted_posts)} raw posts.")

    for post in inserted_posts:
        print(post["reddit_post_id"], post["source_url"])