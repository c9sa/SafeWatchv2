# BUILD > FETCH > FORMAT > INSERT

# build_subreddit_url()
# Creates the Reddit JSON URL.

# fetch_subreddit_posts()
# Calls Reddit and gets raw post data.

# format_reddit_post()
# Converts Reddit format into your raw_posts format.

# fetch_and_store_posts()
# Fetches posts and inserts them into Supabase.

import time
from typing import Any, Optional

import requests

from services.db_readwrites import insert_raw_post


# Reddit needs a User-Agent header or requests may get blocked.
HEADERS = {
    "User-Agent": "SafeWatchFetcher/1.0"
}


# Builds the Reddit JSON URL for a subreddit.
# Used by fetch_subreddit_posts() before making the request.
def build_subreddit_url(
    subreddit: str,
    sort: str = "new",
    limit: int = 10,
) -> str:
    return f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"


# Converts one Reddit post into the raw_posts format.
# Used before inserting the post into Supabase.
def format_reddit_post(post_data: dict[str, Any]) -> dict[str, Optional[str]]:
    title = post_data.get("title") or ""
    body = post_data.get("selftext") or ""

    raw_text = f"{title}\n\n{body}".strip()

    permalink = post_data.get("permalink")
    source_url = f"https://www.reddit.com{permalink}" if permalink else None

    reddit_post_id = post_data.get("name") or post_data.get("id")

    created_utc = post_data.get("created_utc")
    timestamp_text = str(created_utc) if created_utc else None

    return {
        "source_platform": "reddit",
        "source_url": source_url,
        "raw_text": raw_text,
        "timestamp_text": timestamp_text,
        "reddit_post_id": reddit_post_id,
    }


# FETCH posts from Reddit but does not save them yet.
# **Used by fetch_and_store_posts().
def fetch_subreddit_posts(
    subreddit: str,
    sort: str = "new",
    limit: int = 10,
) -> list[dict[str, Optional[str]]]:
    url = build_subreddit_url(
        subreddit=subreddit,
        sort=sort,
        limit=limit,
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Reddit request failed with status {response.status_code}: "
            f"{response.text[:200]}"
        )

    payload = response.json()
    children = payload.get("data", {}).get("children", [])

    posts = []

    for child in children:
        post_data = child.get("data", {})

        # Skip pinned/mod posts because they are usually not real incidents.
        if post_data.get("stickied"):
            continue

        formatted_post = format_reddit_post(post_data)

        # Skip empty posts.
        if not formatted_post["raw_text"]:
            continue

        posts.append(formatted_post)

    return posts


# Fetches Reddit posts and inserts them into raw_posts.
# Used by scripts, FastAPI, or later pipeline triggers.
def fetch_and_store_posts(
    subreddit: str,
    sort: str = "new",
    limit: int = 10,
    sleep_seconds: float = 0.5,
) -> list[dict[str, Any]]:
    posts = fetch_subreddit_posts(
        subreddit=subreddit,
        sort=sort,
        limit=limit,
    )

    inserted_rows = []

    for post in posts:
        inserted = insert_raw_post(
            raw_text=post["raw_text"] or "",
            source_platform=post["source_platform"] or "reddit",
            source_url=post["source_url"],
            timestamp_text=post["timestamp_text"],
            reddit_post_id=post["reddit_post_id"],
        )

        if inserted is None:
            print("Skipped duplicate:", post["reddit_post_id"])
            continue

        print("Inserted:", inserted["reddit_post_id"])
        inserted_rows.append(inserted)

        # Small delay so we do not spam Reddit/Supabase.
        time.sleep(sleep_seconds)

    return inserted_rows