#create Supabase connection

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_supabase_client() -> Client:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url:
        raise ValueError("Missing SUPABASE_URL in .env")

    if not supabase_key:
        raise ValueError("Missing SUPABASE_SERVICE_ROLE_KEY in .env")

    return create_client(supabase_url, supabase_key)