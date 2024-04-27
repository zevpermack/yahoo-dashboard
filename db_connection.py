import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
# Initialize the db variable
db = None

# Connect to the Supabase database
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
db = create_client(url, key)
