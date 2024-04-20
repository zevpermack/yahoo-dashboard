import os
from supabase import create_client, Client
from local_db_connect import local_connect

# Initialize the db variable
db = None
# Check if we're running in development mode
if os.getenv('DEVELOPMENT'):
    # Connect to the local database
    db = local_connect()
else:
    # Connect to the Supabase database
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    db = create_client(url, key)
